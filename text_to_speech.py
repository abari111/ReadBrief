import pyttsx3

def speech_to_text(text, path="output_audio.wav"):
    engine = pyttsx3.init()
    
    engine.save_to_file(text, path )
    engine.runAndWait()
