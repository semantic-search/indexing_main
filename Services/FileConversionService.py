import requests
import uuid
import os
import cairosvg
import subprocess
import globals


class FileConvert:
    def convert_doc(self, file, target_extension):
        target_file = "Services/converted_files/" + str(uuid.uuid4()) + "." + target_extension
        url = globals.UNOCONV_SERVER + target_extension
        file_to_convert = [('file', open(file, 'rb'))]
        response = requests.request("POST", url, files=file_to_convert)
        with open(target_file, 'wb') as file_obj:
            file_obj.write(response.content)
        return target_file


    def convert_audio(self, source_format, file):
        target_file = "Services/converted_files/" + str(uuid.uuid4()) + ".wav"
        if source_format == "wav":
            subprocess.call(["sox",  file, "-r", "16000", "-c", "1", target_file])
        elif source_format == "mp3":
            subprocess.call(["sox",  file, "-r", "16000", "-c", "1", target_file])
        elif source_format == "m4a":
            subprocess.call(["ffmpeg", "-i", file, "-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000", target_file])
        elif source_format == "aiff":
            subprocess.call(["sox",  file, "-r", "16000", "-c", "1", target_file])
        os.remove(file)
        return target_file


    def convert_video(self, source_format, file):
        target_file = "Services/converted_files/" + str(uuid.uuid4()) + ".wav"
        try:
            if source_format == "mp4":
                subprocess.call(["ffmpeg", "-i", file, "-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000", target_file])
            elif source_format == "mkv":
                subprocess.call(["ffmpeg", "-i", file, "-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000", target_file])
            elif source_format == "avi":
                subprocess.call(["ffmpeg", "-i", file, "-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000", target_file])
            elif source_format == "webm":
                subprocess.call(["ffmpeg", "-i", file, "-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000", target_file])
            os.remove(file)
        except:
            os.remove(file)
        return target_file


    def convert_svg(self, file):
        target_file = "Services/converted_files/" + str(uuid.uuid4()) + ".png"
        cairosvg.svg2png(url=file, write_to=target_file)
        os.remove(file)
        return target_file
