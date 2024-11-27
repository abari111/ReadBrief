import os

import shutil
from playsound import playsound
from pydub import AudioSegment
from pydub.playback import play
import simpleaudio as sa
import argparse

from docs_processing import extract_book_chapters
from text_to_speech import speech_to_text
from utils import generate_text


parser = argparse.ArgumentParser()
parser.add_argument("--path", type=str, help="book path", default="data/ia_emb.pdf" )

args = parser.parse_args()

pdf_path = args.path
tmp_folder = "chapitres_output"
chap = "chap_1.txt"

chaps = extract_book_chapters(pdf_path, tmp_folder)
print(chaps)

with open(os.path.join(tmp_folder, chap)) as f:
    text = f.read()

prompt = f"Resume le chapitre suivant en quelques paragraphes et dans un texte\
    qui permet de le transcrire en audio facilement. Renvoie uniquement le resumé: {text}"
text = generate_text(prompt=prompt)
speech_to_text(text)

display = """
        1- chapitre 1
        2- chapitre 2
        3- chapitre 3
        4- ......
        0- to quit
"""
while True:
    print(display)
    ans = int(input("Input : "))
    if ans == 0:
        shutil.rmtree(tmp_folder)
        break
    with open(chaps[ans -1]) as f:
        text = f.read()
    prompt = f"Resume le chapitre suivant en quelques paragraphes et dans un texte\
    qui permet de le transcrire en audio facilement. Renvoie uniquement le resumé: {text}"
    text = generate_text(prompt=prompt)
    speech_to_text(text)
    print("============Playing==============")
    wave_obj = sa.WaveObject.from_wave_file("output_audio.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()