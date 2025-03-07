import os
import whisper
from moviepy.editor import VideoFileClip
from pydub import AudioSegment

def get_temp_audio_path(filename):
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    return os.path.join(temp_dir, filename)

def extract_audio_from_video(video_path, audio_path):
    """Извлекает аудио из видеофайла и сохраняет его по указанному пути."""
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)

def convert_audio_format(input_path, output_path, target_sample_rate=16000):
    """
    Конвертирует аудио в формат WAV с указанной частотой дискретизации и моно-каналом.
    Это улучшает качество транскрипции модели Whisper.
    """
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_frame_rate(target_sample_rate).set_channels(1)
    audio.export(output_path, format="wav")

def transcribe_audio_whisper(audio_path, model_name="base"):
    """
    Загружает модель Whisper и выполняет транскрипцию аудиофайла.
    Параметр model_name можно задавать как "tiny", "base", "small", "medium", "large".
    """
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path)
    return result["text"]

def save_text_to_file(text, file_path):
    """Сохраняет транскрибированный текст в указанный файл."""
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)

def transcribe_media(media_path, output_text_path, model_name="base"):
    """
    Основная функция для транскрипции медиафайла с использованием OpenAI Whisper.
    Поддерживаются видео (.mp4, .avi, .mov) и аудио файлы (.wav, .mp3, .flac).
    Если обрабатывается видео, сначала извлекается аудио.
    Затем аудио конвертируется в формат WAV (моно, 16 кГц) и передаётся в Whisper.
    """
    # Если это видео, извлекаем аудио во временный WAV-файл
    if media_path.lower().endswith((".mp4", ".avi", ".mov")):
        temp_audio_path = get_temp_audio_path("temp_audio.wav")
        extract_audio_from_video(media_path, temp_audio_path)
        input_audio_path = temp_audio_path
    elif media_path.lower().endswith((".wav", ".mp3", ".flac")):
        input_audio_path = media_path
    else:
        raise ValueError("Неподдерживаемый формат файла: " + media_path)
    
    # Конвертируем аудио 
    processed_audio_path = get_temp_audio_path("processed_audio.wav")
    convert_audio_format(input_audio_path, processed_audio_path)
    
    print(f"Начало транскрипции с Whisper для файла: {media_path}")
    transcription = transcribe_audio_whisper(processed_audio_path, model_name=model_name)
    
    save_text_to_file(transcription, output_text_path)
    
    # Удаляем временные файлы, если они были уже ранее созданы
    if media_path.lower().endswith((".mp4", ".avi", ".mov")) and os.path.exists(temp_audio_path):
        os.remove(temp_audio_path)
    if os.path.exists(processed_audio_path):
        os.remove(processed_audio_path)

if __name__ == "__main__":
    # Папка с медиафайлами
    media_folder = "data"
    # Папка для сохранения транскрибаций
    output_folder = "transcriptions"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Поддерживаемые расширения файлов
    supported_extensions = (".mp4", ".avi", ".mov", ".wav", ".mp3", ".flac")
    
    for filename in os.listdir(media_folder):
        if filename.lower().endswith(supported_extensions):
            media_file = os.path.join(media_folder, filename)
            output_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")
            try:
                transcribe_media(media_file, output_file, model_name="base")
                print(f"Транскрипция для {filename} сохранена в {output_file}")
            except Exception as e:
                print(f"Ошибка при обработке файла {filename}: {e}")
