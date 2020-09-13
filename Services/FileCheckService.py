import magic
import globals
from PyPDF2 import PdfFileReader
import subprocess


class FileCheck:
    def check_mime_type(self, file):
        file_extension = None
        mime_type = magic.from_file(file, mime=True)
        for key, val in globals.MIME_TYPES_DOCUMENTS:
            if str(mime_type) == val:
                file_extension = key
                break
        for key, val in globals.MIME_TYPES_LEGACY_DOCUMENTS:
            if str(mime_type) == val:
                file_extension = key
                break
        for key, val in globals.MIME_TYPES_AUDIO:
            if str(mime_type) == val:
                file_extension = key
                break
        for key, val in globals.MIME_TYPES_IMAGES:
            if str(mime_type) == val:
                file_extension = key
                break
        for key, val in globals.MIME_TYPES_VIDEO:
            if str(mime_type) == val:
                file_extension = key
                break
        if file_extension:
            return file_extension
        else:
            return None


    def check_pdf_encrypted(self, file):
        with open(file, 'rb') as pdf_data:
            pdf_reader_obj = PdfFileReader(pdf_data)
            if pdf_reader_obj.isEncrypted:
                return True
            else:
                return False


    def check_video_audio(self, file):
        video_data = subprocess.check_output(["ffprobe", "-i", file, "-show_streams",
                                              "-select_streams", "a", "-loglevel", "error"])
        video_data = video_data.decode("utf8")

        if len(video_data) == 0:
            return True
        else:
            return False
