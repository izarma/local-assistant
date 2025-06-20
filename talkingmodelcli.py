import ollama
import time
import pyttsx3

# Initialize model name
model_name = 'gemma3:1b'

# Initialize the text-to-speech engine: retrive and assign voice
tts_engine = pyttsx3.init()
voices = tts_engine.getProperty('voices')
assistant_voice = voices[0].id  # Replace with the index of the desired voice for Assistant 1

def chat_between_two_models():
    # Set separate starting prompts for each assistant
    system_prompt = "You are Nakli Jarvis, an helpful ai voice assistant that helps in remembering things and managing tasks: try to keep your replies concise and to the point. Do not output symbols or emojis."
    
    # Initialize the conversation histories with their starting prompts
    messages = [{'role': 'user', 'content': system_prompt}]
    
    # Start the conversation loop with Assistant 1 as the first responder
    current_active_label = 'Nakli-Jarvis'

    while True:
        if current_active_label == 'Nakli-Jarvis':
            # Get the response from model_name_1 with its message history
            response = ollama.chat(model=model_name, messages=messages)
            response_content = response['message']['content']
            
            # Print and speak the model's response
            print(f"Nakli-Jarvis: {response_content}")
            tts_engine.setProperty('voice', assistant_voice)
            tts_engine.say(response_content)
            tts_engine.runAndWait()
            
            # Append the response to messages_1 as an assistant message
            messages.append({'role': 'assistant', 'content': response_content})

            # Switch to User for the next response
            current_active_label = 'User'
        
        else:  # User
            user_input = input("You: ")
            if user_input.lower() in ("exit", "quit"):
                break
            messages.append({'role': 'user', 'content': user_input})

            # Switch back to Assistant 1 for the next response
            current_active_label = 'Nakli-Jarvis'

def main():
    chat_between_two_models()

if __name__ == "__main__":
    main()
