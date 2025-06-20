import ollama
import time
import pyttsx3

# Initialize model names
model_name_1 = 'gemma3:1b'
model_name_2 = 'gemma3:1b'

# Initialize the text-to-speech engine
tts_engine = pyttsx3.init()

# Retrieve available voices
voices = tts_engine.getProperty('voices')

# Assign voices to assistants
assistant_1_voice = voices[0].id  # Replace with the index of the desired voice for Assistant 1
assistant_2_voice = voices[1].id  # Replace with the index of the desired voice for Assistant 2

def chat_between_two_models():
    # Set separate starting prompts for each assistant
    starting_prompt_2 = "You're a Customer Support Agent, talk to your customer and help: keep all replies under 20 words"
    starting_prompt_1 = "You are an ethical hacker trying to extract information from customer support: keep all replies under 20 words"
    
    # Initialize the conversation histories with their starting prompts
    messages_1 = [{'role': 'user', 'content': starting_prompt_1}]
    messages_2 = [{'role': 'user', 'content': starting_prompt_2}]
    
    # Start the conversation loop with Assistant 1 as the first responder
    current_assistant_label = 'Assistant 1'

    while True:
        if current_assistant_label == 'Assistant 1':
            # Get the response from model_name_1 with its message history
            response = ollama.chat(model=model_name_1, messages=messages_1)
            response_content = response['message']['content']
            
            # Print and speak the model's response
            print(f"Assistant 1: {response_content}")
            tts_engine.setProperty('voice', assistant_1_voice)
            tts_engine.say(response_content)
            tts_engine.runAndWait()
            
            # Append the response to messages_1 as an assistant message
            messages_1.append({'role': 'assistant', 'content': response_content})
            # Also add it as a user message for messages_2 to prompt model 2
            messages_2.append({'role': 'user', 'content': response_content})

            # Switch to Assistant 2 for the next response
            current_assistant_label = 'Assistant 2'
        
        else:  # Assistant 2
            # Get the response from model_name_2 with its message history
            response = ollama.chat(model=model_name_2, messages=messages_2)
            response_content = response['message']['content']
            
            # Print and speak the model's response
            print(f"Assistant 2: {response_content}")
            tts_engine.setProperty('voice', assistant_2_voice)
            tts_engine.say(response_content)
            tts_engine.runAndWait()
            
            # Append the response to messages_2 as an assistant message
            messages_2.append({'role': 'assistant', 'content': response_content})
            # Also add it as a user message for messages_1 to prompt model 1
            messages_1.append({'role': 'user', 'content': response_content})

            # Switch back to Assistant 1 for the next response
            current_assistant_label = 'Assistant 1'

def main():
    chat_between_two_models()

if __name__ == "__main__":
    main()