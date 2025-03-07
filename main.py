import os
from transcriber import transcribe_media

def main():
    # Папки для входных и выходных данных
    data_dir = "data"
    output_dir = "output"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    supported_extensions = (".mp4", ".avi", ".mov", ".wav", ".mp3", ".flac")
    media_files = [f for f in os.listdir(data_dir) if f.lower().endswith(supported_extensions)]
    
    if not media_files:
        print("В папке data нет поддерживаемых медиафайлов!")
        return
    
    # Задайте модель Whisper (например, "base" или "small", "medium", "large")
    model_name = "base"
    
    for i, media_file in enumerate(media_files, start=1):
        media_path = os.path.join(data_dir, media_file)
        output_text_path = os.path.join(output_dir, f"transcription_{i}.txt")
        
        print(f"Обработка файла {i}/{len(media_files)}: {media_file}")
        try:
            transcribe_media(media_path, output_text_path, model_name)
            print(f"Транскрипция сохранена в {output_text_path}")
        except Exception as e:
            print(f"Ошибка при обработке {media_file}: {e}")

if __name__ == "__main__":
    main()
