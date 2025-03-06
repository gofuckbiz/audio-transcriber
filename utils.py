import os

def get_temp_audio_path(filename):
    """Возвращает путь к временному аудиофайлу в папке temp/."""
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    return os.path.join(temp_dir, filename)