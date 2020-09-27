import globals
import yaml


def parse(yaml_file):
    with open(yaml_file) as f:
        config_dict = yaml.safe_load(f)
    for key, val in config_dict.items():
        if key == "Image":
            for key1, val1 in val.items():
                if key1 == "Image_Captioning":
                    globals.image_captioning_containers = val1
                elif key1 == "Ocr":
                    globals.ocr_containers = val1
                elif key1 == "Object_Detection":
                    globals.object_detection_containers = val1
                elif key1 == "Scene_Recognition":
                    globals.scene_recognition_containers = val1
                elif key1 == "Image_Recognition":
                    globals.image_recognition_containers = val1
                elif key1 == "Image_Search":
                    globals.image_search_containers = val1
                elif key1 == "Face_Recognition":
                    globals.face_recognition_containers = val1
        elif key == "Audio":
            for key1, val1 in val.items():
                if key1 == "Sound_Classification":
                    globals.sound_classification_containers = val1
                elif key1 == "Audio_Fingerprinting":
                    globals.audio_fingerprinting_containers = val1
                elif key1 == "Speech_To_Text":
                    globals.speech_to_text_containers = val1
        elif key == "Entity":
            globals.entity_recognition_containers = val
        elif key == "Search":
            globals.search_containers = val


