import textract
import re
import uuid
import subprocess
import os
import re
from pathlib import Path
import chardet
import shutil
from zipfile import ZipFile


class FileExtract:
    def extract_text_docs(self, file):
        text = textract.process(file)
        text = text.decode('utf-8')
    # Decodes text
        text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    # Removes \n \r \t
        text = re.sub(' +', ' ', text)
    # Removes extra white spaces
        return text


    def extractor(self, starts_with, file):
        new_directory = "Services/images/" + str(uuid.uuid4())
        # unique folder created
        os.mkdir(new_directory)
        new_file = new_directory + "/" + str(file)
        shutil.copy2(file, new_file)
        # copy this file to this directory
        archive = ZipFile(new_file)
        images_array = []
        for image_file in archive.namelist():
            if image_file.startswith(starts_with):
                print(image_file)
                image = archive.extract(member=image_file, path=new_directory)
                images_array.append(image)
        os.remove(new_file)
        return images_array


    def extract_images_docs(self, file, extension):
        if extension == 'pptx':
            startswith = 'ppt/media'
            images_list = self.extractor(file=file, starts_with=startswith)
            return images_list
        elif extension == 'xlsx':
            startswith = 'xl/media'
            images_list = self.extractor(file=file, starts_with=startswith)
            return images_list
        elif extension == 'docx':
            startswith = 'word/media'
            images_list = self.extractor(file=file, starts_with=startswith)
            return images_list


    def extract_images_epub(self, file):
        images_list = self.extractor(file=file, starts_with='EPUB/images')
        return images_list


    def extract_images_odt(self, file):
        images_list = self.extractor(file=file, starts_with='Pictures')
        return images_list


    def extract_text_pdf(self, file):
        text_file = "Services/text_files/" + str(uuid.uuid4()) + ".txt"
        """Extract text"""
        subprocess.call(["./Services/pdftotext", file, text_file])

        """TODO: check if the txt contains any unknown character and remove it"""
        with open(text_file, 'rb') as raw:
            raw_text = raw.read()
        encoding_dict = chardet.detect(raw_text)
        text = raw_text.decode(encoding_dict["encoding"])
        text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', text)
        text = re.sub(' +', ' ', text)
        """Remove txt files"""
        os.remove(text_file)
        return text


    def extract_images_pdf(self, file):
        image_folder = "Services/images/" + str(uuid.uuid4()) + "/"
        os.mkdir(image_folder)
        images = []
        """Extract images"""
        subprocess.call(["./Services/pdfimages", "-j", file, image_folder])
        for path in Path(image_folder).rglob('*.jpg'):
            images.append(path.name)
        """TODO: remove rest files"""
        images_list = []
        for image in images:
            images_list.append(image_folder+str(image))
        final_response = {
            "images": images_list,
            "images_folder": image_folder
        }
        return final_response
