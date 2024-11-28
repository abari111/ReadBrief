import os
import sys

import shutil
from playsound import playsound
from pydub import AudioSegment
from pydub.playback import play
import simpleaudio as sa
import argparse
from dotenv import load_dotenv

from docs_processing import extract_book_chapters
from text_to_speech import speech_to_text
from utils import generate_text, get_chap

# Books_path
# Book_name
# audio_name
# chap_name
parser = argparse.ArgumentParser()
parser.add_argument("--path", type=str, help="book path", default="data/ia_emb.pdf" )

args = parser.parse_args()
pdf_path = args.path

books_path = "books"
book_name = os.path.join(books_path, pdf_path.split('/')[-1])
tmp_folder = os.path.join(book_name ,"chapters")
tmp_audio = os.path.join(book_name ,"audio_chap")
chap = "chap_1.txt"

chaps = extract_book_chapters(pdf_path, tmp_folder)
audio_chaps = {}
with open(os.path.join(tmp_folder, chap)) as f:
    text = f.read()
if not os.path.exists(books_path):
    os.mkdir(books_path)
if not os.path.exists(book_name):
    os.mkdir(book_name)
if not os.path.exists(tmp_audio):
    os.mkdir(tmp_audio)
else:
    dirs = os.listdir(tmp_audio)
    for file_name in dirs:
        audio_chaps[get_chap(file_name)] = os.path.join(tmp_audio, file_name)


# prompt = f"Resume le chapitre suivant en quelques paragraphes et dans un texte\
#     qui permet de le transcrire en audio facilement. Renvoie uniquement le resumé: {text}"
# text = generate_text(prompt=prompt)
# speech_to_text(text)

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
    
    if not (ans in audio_chaps):
        # prompt = f"Resume le chapitre suivant en quelques paragraphes et dans un texte\
        # qui permet de le transcrire en audio facilement. Renvoie uniquement le resumé: {text}"
        # text = generate_text(prompt=prompt)
        file_name = f"chap_{ans}.wav"
        audio_path=os.path.join(tmp_audio, file_name)
        speech_to_text(text, path=audio_path)
        audio_chaps[ans] = audio_path
    print("============Playing==============")
    wave_obj = sa.WaveObject.from_wave_file(audio_chaps[ans])
    play_obj = wave_obj.play()
    play_obj.wait_done()