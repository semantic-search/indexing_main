import magic
import globals
from PyPDF2 import PdfFileReader
import subprocess


class FileCheck:
    def check_mime_type(self, file=False, extension=False):
        file_extension = None
        if extension:
            mime_type = extension
        else:
            mime_type = magic.from_file(file, mime=True)
        for key, val in globals.MIME_TYPES_DOCUMENTS.items():
            if str(mime_type) == val:
                file_extension = key
                group = "document"
                break
        for key, val in globals.MIME_TYPES_LEGACY_DOCUMENTS.items():
            if str(mime_type) == val:
                file_extension = key
                group = "legacy_document"
                break
        for key, val in globals.MIME_TYPES_AUDIO.items():
            if str(mime_type) == val:
                file_extension = key
                group = "audio"
                break
        for key, val in globals.MIME_TYPES_IMAGES.items():
            if str(mime_type) == val:
                file_extension = key
                group = "image"
                break
        for key, val in globals.MIME_TYPES_VIDEO.items():
            if str(mime_type) == val:
                file_extension = key
                group = "video"
                break
        if file_extension:
            mime_dict = {
                "extension": file_extension,
                "group": group
            }
            return mime_dict
        else:
            return None


    def check_pdf_encrypted(self, file):
        with open(file, 'rb') as pdf_data:
            pdf_reader_obj = PdfFileReader(pdf_data)
            if pdf_reader_obj.isEncrypted:
                return True
            else:
                return False
