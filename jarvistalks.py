import ollama
import time
import pyttsx3
import speech_recognition as sr

# Initialize model name
# model_name = 'huihui_ai/deepseek-r1-abliterated:8b'
model_name = 'gemma3:1b'

# Initialize the text-to-speech engine: retrive and assign voice
tts_engine = pyttsx3.init()
voices = tts_engine.getProperty('voices')
assistant_voice = voices[0].id  # Replace with the index of the desired voice for Assistant 1

# Initialize the recognizer
keyword = "hello"
end_keywords = "bye"
r = sr.Recognizer()

def talk_with_jarvis():
    # Set separate starting prompts for each assistant
    system_prompt = "You are Bhai, an helpful ai voice assistant that helps in remembering things and managing tasks: try to keep your replies concise and to the point. Do not output symbols or emojis especially no *"
    # Initialize the conversation histories with their starting prompts
    messages = [{'role': 'user', 'content': system_prompt}]
    conversation_active = False
    while True:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.2)
                if not conversation_active:
                    (messages, conversation_active) = wake_word_detection(r, source, keyword, tts_engine, messages, conversation_active)
                else:
                    print("in coversation")
                    audio = r.listen(source)
                    try:
                        command = r.recognize_google(audio).lower()
                        print(f"Heard: {command}")
                        if end_word_detection(command, messages, conversation_active): # any(kw in command.lower() for kw in end_keywords):
                            continue
                        messages.append({'role': 'user', 'content': command})
                        # Query Ollama with conversation history
                        response = ollama.chat(model=model_name, messages=messages)
                        response_content = response['message']['content']
                        if '</think>' in response_content:
                            response_content = response_content.split('</think>', 1)[1].strip()
                        else:
                            response_content = response_content
                        # Print and speak Ollama's response
                        print(f"Bhai: {response_content}")
                        tts_engine.setProperty('voice', assistant_voice)
                        tts_engine.say(response_content)
                        tts_engine.runAndWait()
                        # Add assistant reply to conversation history
                        messages.append({'role': 'assistant', 'content': response_content})
                    except sr.UnknownValueError:
                        print("Could not understand command.")
                    except sr.RequestError as e:
                        print(f"Could not request results; {e}")

        except KeyboardInterrupt:
            break

def wake_word_detection(r, source, keyword, tts_engine, messages, conversation_active):
    # Listen for a short phrase (for hotword detection)
    audio = r.listen(source, phrase_time_limit=2)
    text = ""
    try:
        text = r.recognize_google(audio).lower()
        print(f"Heard: {text}")
        if keyword in text:
            tts_engine.setProperty('voice', assistant_voice)
            tts_engine.say("Yes?")
            tts_engine.runAndWait()
            messages.append({'role':'user','content':text})
            conversation_active = True
            return (messages, conversation_active)
    except sr.UnknownValueError:
        pass
    return (messages, conversation_active)

def end_word_detection(command, messages, conversation_active):
    if end_keywords in command.lower(): # any(kw in command.lower() for kw in end_keywords):
        tts_engine.say("Goodbye!")
        tts_engine.runAndWait()
        print("Ending conversation.")
        with open("conversation.txt", "w", encoding="utf-8") as f:
            for msg in messages[1:]:
                f.write(f"{msg['role']}: {msg['content']}\n")
        with open("conversation_history.txt", "a", encoding="utf-8") as hf:
            for msg in messages[1:]:
                hf.write(f"{msg['role']}: {msg['content']}\n")
                hf.write("\n")
        conversation_active = False
        messages.clear()
        return True
    else:
        return False

def main():
    talk_with_jarvis()

if __name__ == "__main__":
    main()
