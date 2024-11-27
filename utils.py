import os
import time 
import sys
from io import BytesIO
import requests
from dotenv import load_dotenv

from openai import OpenAI
from PIL import Image
from typing import Set, Dict
from pathlib import Path


from magika import Magika 

def check_file_ext(file_path: str) -> str:
    """
    Check files extensions
    """
    with open(file_path,'rb') as file:
        file = file.read()
    
    model = Magika()
    res = model.identify_bytes(file)

    return res.output.ct_label

load_dotenv()

def setUp():
    load_dotenv()
    client = OpenAI()
    return client

def generate_text(prompt:str, temperature:float=None) ->str:
    client = setUp()
    if temperature is None:
        response = client.chat.completions.create(
                            model='gpt-3.5-turbo',
                            messages=[{'role': 'user', 'content': prompt}])
        return response.choices[0].message.content
    
    response = client.chat.completions.create(
                            model='gpt-3.5-turbo',
                            messages=[{'role': 'user', 'content': prompt}], temperature=0)
    return response.choices[0].message.content

if __name__=="__main__":
    file_ext = check_file_ext("spinQuant")
    print(file_ext)
