import globals


def populate_lists(group_array):
    globals.image_tasks = group_array[0]
    globals.audio_task = group_array[1]
    globals.image_captioning_containers = group_array[2]
    globals.ocr_containers = group_array[3]
    globals.object_detection_containers = group_array[4]
    globals.scene_recognition_containers = group_array[5]
    globals.image_recognition_containers = group_array[6]
    globals.image_search_containers = group_array[7]
    globals.face_recognition_containers = group_array[8]
    globals.sound_classification_containers = group_array[9]
    globals.audio_fingerprinting_containers = group_array[10]
    globals.speech_to_text_containers = group_array[11]
    globals.entity_recognition_containers = group_array[12]
    globals.search_containers = group_array[13]