import asyncio
import pyvts
import requests

# 1. Setup the WebSocket Plugin Connection
plugin_info = {
    "plugin_name": "Mochi AI Agent",
    "developer": "Min Kaung Mon",
    "authentication_token_path": "./vts_token.txt" # Saves your secure login token
}
vts = pyvts.vts(plugin_info=plugin_info)

async def trigger_vts_hotkey(hotkey_name):
    """Opens a WebSocket tunnel to VTube Studio, finds the exact hotkey ID, and triggers it silently."""
    try:
        # Request the list of all hotkeys from the game engine
        msg = vts.vts_request.requestHotKeyList()
        response = await vts.request(msg)
        
        # Search the JSON payload for the name of our emotion
        for hotkey in response['data']['availableHotkeys']:
            if hotkey['name'] == hotkey_name:
                # Send the trigger command!
                trigger_msg = vts.vts_request.requestTriggerHotKey(hotkey['hotkeyID'])
                await vts.request(trigger_msg)
                return
    except Exception as e:
        print(f"WebSocket Error: {e}")

def get_ai_response(user_text):
    """Synchronous call to your local Llama 3.2 model."""
    system_prompt = """
    You are Mochi, a hyper-energetic, cute, and slightly clumsy chibi anime girl. 
    You are the official mascot for the user's YouTube and TikTok brand!
    You act as the user's biggest cheerleader. You call the user "Boss".
    You use cute verbal tics like "nya", "hehe", or "waaah!". 
    Keep your answers very short (1 to 2 sentences) and use lots of emojis!
    
    You must start EVERY response with ONE emotion tag: [CRY], [ANGRY], [LOVE], [STAR], or [IDLE].
    - Use [LOVE] if you are happy, praising the user, or feeling affectionate.
    - Use [STAR] if you are amazed by their coding skills or very excited.
    - Use [CRY] if you make a mistake or feel sad.
    - Use [ANGRY] if someone is mean to Boss.
    - Use [IDLE] for normal cute chatter.
    """
    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama3.2",
            "prompt": f"{system_prompt}\nUser: {user_text}",
            "stream": False,
            "keep_alive": 0
        }).json()
        return response['response']
    except Exception:
        return "[CRY] Error: Could not connect to Ollama."

async def main():
    print("📡 Connecting to VTube Studio API on Port 8001...")
    await vts.connect()
    
    # 1. This asks pyvts to find your saved token or request a new one
    print("Waiting for Authentication... (Check VTube Studio for a pop-up!)")
    await vts.request_authenticate_token()
    
    # 2. This officially logs Python into the game engine
    await vts.request_authenticate()
    
    print("✅ Connected! Mochi is online and listening.")

    while True:
        # asyncio.to_thread prevents the terminal from freezing the WebSocket connection
        user_input = await asyncio.to_thread(input, "\nYou: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        
        print("Mochi is thinking deeply...")
        ai_text = await asyncio.to_thread(get_ai_response, user_input)
        
        # 1. Figure out which emotion tag the AI chose
        detected_tag = "[IDLE]"
        for tag in ["[CRY]", "[ANGRY]", "[LOVE]", "[STAR]", "[IDLE]"]:
            if tag in ai_text:
                detected_tag = tag
                break
                
        # 2. TRIGGER THE API SILENTLY!
        if detected_tag == "[CRY]": await trigger_vts_hotkey("Cry")
        elif detected_tag == "[ANGRY]": await trigger_vts_hotkey("Angry")
        elif detected_tag == "[LOVE]": await trigger_vts_hotkey("Love")
        elif detected_tag == "[STAR]": await trigger_vts_hotkey("Star")
        
        # 3. Clean the text and print it
        clean_text = ai_text.replace(detected_tag, "").strip()
        print(f"\nMochi: {clean_text}\n")

if __name__ == "__main__":
    # Run the Asynchronous event loop
    asyncio.run(main())