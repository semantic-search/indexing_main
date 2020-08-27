# Utility Scripts for pdf encrypt check, images and text extraction
from PyPDF2 import PdfFileReader
import uuid
import subprocess
import os
import re
from pathlib import Path
class PdfUtils:
    def check(self, file):
        with open(file, 'rb') as pdf_data:
            pdf_reader_obj = PdfFileReader(pdf_data)
            if pdf_reader_obj.isEncrypted:
                return True
            else:
                return False
    def extract_text_and_images(self, file):
        text_file = "text_files/" + str(uuid.uuid4()) + ".txt"
        image_folder = "images/" + str(uuid.uuid4()) + "/"
        os.mkdir(image_folder)
        """Extract text"""
        subprocess.call(["./Services/pdftotext", file, text_file])
        """Extract images"""
        subprocess.call(["./Services/pdfimages", "-j", file, image_folder])
        """TODO: check if the txt contains any unknown character and remove it"""
        with open(text_file, encoding="utf8", errors='ignore') as raw:
            raw_text = raw.read()
        text_with_escape_sequence = raw_text.replace("\n", " ")
        clean_text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', text_with_escape_sequence)
        images = []
        for path in Path(image_folder).rglob('*.jpg'):
            images.append(path.name)
        images_list = []
        for image in images:
            images_list.append(image_folder+str(image))
        """Remove txt files"""
        os.remove(text_file)
        final_response = {
            "text": clean_text,
            "images": images_list,
            "images_folder": image_folder
        }
        return final_response