import globals


def populate_lists(group_array):
    globals.image_captioning_containers = group_array[0]
    globals.ocr_containers = group_array[1]
    globals.object_detection_containers = group_array[2]
    globals.scene_recognition_containers = group_array[3]
    globals.image_recognition_containers = group_array[4]
    globals.image_search_containers = group_array[5]
    globals.face_recognition_containers = group_array[6]
    globals.sound_classification_containers = group_array[7]
    globals.audio_fingerprinting_containers = group_array[8]
    globals.speech_to_text_containers = group_array[9]
    globals.entity_recognition_containers = group_array[10]
    globals.search_containers = group_array[11]