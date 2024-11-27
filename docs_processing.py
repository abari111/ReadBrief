
import os

import pdfplumber
import re


def extract_epub():
    pass 

def pdf_to_text(file_path, out_dir):
    file_name = file_path.split("/")[-1]
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()

def extract_book_chapters(file_path, out_dir):
    file_name = file_path.split("/")[-1]
    
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    chaps = []
    chapter_text = ""
    chapter_number = 0
    chapter_pattern = re.compile(r"^Chapitre\s+\d+", re.IGNORECASE)  # Motif pour détecter les chapitres

    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            
            if text:
                lines = text.splitlines()
                for line in lines:
                    if chapter_pattern.match(line):
                        if chapter_text:
                            output_path = f"{out_dir}/chap_{chapter_number}.txt"
                            chaps.append(f"{out_dir}/chap_{chapter_number}.txt")
                            with open(output_path, 'w', encoding='utf-8') as f:
                                f.write(chapter_text)
                            print(f"Chapitre {chapter_number} extracted {output_path}")
                        chapter_number += 1
                        chapter_text = line + "\n"
                    else:
                        chapter_text += line + "\n"
        if chapter_text:
            output_path = f"{out_dir}/chap_{chapter_number}.txt"
            chaps.append(f"{out_dir}/chap_{chapter_number}.txt")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(chapter_text)
            print(f"Chapter {chapter_number} extracted and saved in {output_path}")
    return chaps
