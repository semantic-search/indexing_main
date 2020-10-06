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
import glob
import exifread
import requests
import json


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


    def extractor(self, starts_with, file, file_name):
        new_directory = "Services/images/" + str(uuid.uuid4())
        # unique folder created
        os.mkdir(new_directory)
        new_file = new_directory + "/" + file_name
        shutil.copy2(file, new_file)
        # copy this file to this directory
        archive = ZipFile(new_file)
        images_list = []
        for image_file in archive.namelist():
            if image_file.startswith(starts_with):
                image = archive.extract(member=image_file, path=new_directory)
                images_list.append(image)
        os.remove(new_file)
        final_response = {
            "images": images_list,
            "images_folder": new_directory
        }
        return final_response


    def extract_images_docs(self, file, extension, file_name):
        if extension == 'pptx':
            startswith = 'ppt/media'
            images_response = self.extractor(file=file, starts_with=startswith, file_name=file_name)
            return images_response
        elif extension == 'xlsx':
            startswith = 'xl/media'
            images_response = self.extractor(file=file, starts_with=startswith, file_name=file_name)
            return images_response
        elif extension == 'docx':
            startswith = 'word/media'
            images_response = self.extractor(file=file, starts_with=startswith, file_name=file_name)
            return images_response
        elif extension == "epub":
            starts_with = 'EPUB/images'
            images_response = self.extractor(file=file, starts_with=starts_with, file_name=file_name)
            return images_response
        elif extension == "odt":
            starts_with = 'Pictures'
            images_response = self.extractor(file=file, starts_with=starts_with, file_name=file_name)
            return images_response


    def extract_images_pdf(self, file):
        image_folder = "Services/images/" + str(uuid.uuid4()) + "/"
        os.mkdir(image_folder)
        images = []
        """Extract images"""
        subprocess.call(["./Services/pdfimages", "-j", file, image_folder])
        for path in Path(image_folder).rglob('*.jpg'):
            images.append(path.name)
        images_list = []
        for image in images:
            images_list.append(image_folder + str(image))
        for file in glob.glob(image_folder + '*.*'):
            if file not in images_list:
                os.remove(file)


        final_response = {
            "images": images_list,
            "images_folder": image_folder
        }
        return final_response


    def exif_to_location(self, image):
        print(image)
        img_obj = open(image, 'rb')
        latitude_ref = None
        latitude = None
        longitude_ref = None
        longitude = None
        tags = exifread.process_file(img_obj, details=False)
        for key, value in tags.items():
            if str(key) == "GPS GPSLatitudeRef":
                latitude_ref = str(value)
            elif str(key) == "GPS GPSLatitude":
                latitude = eval(str(value))
            elif str(key) == "GPS GPSLongitudeRef":
                longitude_ref = str(value)
            elif str(key) == "GPS GPSLongitude":
                longitude = eval(str(value))
        print(latitude_ref)
        print(longitude_ref)
        if latitude is None:
            return None
        else:
            latitude = latitude[0] + float(latitude[1]) / 60 + float(latitude[2]) / 3600
            longitude = longitude[0] + float(longitude[1]) / 60 + float(longitude[2]) / 3600

            if latitude_ref == "W" or latitude_ref == "S":
                latitude = -latitude
            elif longitude_ref == "W" or longitude_ref == "S":
                longitude = -longitude
            print(latitude, longitude)
            url = "https://nominatim.openstreetmap.org/reverse?format=jsonv2&"+"lat="+str(latitude)+"&lon="+str(longitude)
            print(url)
            response = requests.request("GET", url)
            pic_location_data = dict()
            location_data = json.loads(response.text)
            pic_location_data["location_category"] = location_data["category"]
            pic_location_data["location_type"] = location_data["type"]
            pic_location_data["location_name"] = location_data["name"]
            pic_location_data["location_address"] = location_data["address"]
            return pic_location_data