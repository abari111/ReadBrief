import pyttsx3
from pathlib import Path
from openai import OpenAI

def text_to_speech(text, path="output_audio.wav"):
    client = OpenAI()

    # speech_file_path = Path(__file__).parent / "speech.mp3"
    speech_file_path = path
    response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input=text
    )

    response.stream_to_file(speech_file_path)

def speech_to_text(text, path="output_audio.wav"):
    engine = pyttsx3.init()
    
    engine.save_to_file(text, path )
    engine.runAndWait()

if __name__=="__main__":
    with open('abari.txt', 'r') as fp:
        text = fp.read()
    text_to_speech(text)