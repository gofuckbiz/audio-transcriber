import speech_recognition as sr
import time
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import os
from tqdm import tqdm
from utils import get_temp_audio_path
import noisereduce as nr
from scipy.io import wavfile
import numpy as np

def extract_audio_from_video(video_path, audio_path):
    """Извлекает аудио из видеофайла и сохраняет его в указанный путь."""
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)

def preprocess_audio(audio_segment):
    """Предобработка аудио: шумоподавление и нормализация."""
    temp_wav = get_temp_audio_path("temp_preprocess.wav")
    audio_mono = audio_segment.set_channels(1)
    audio_mono.export(temp_wav, format="wav")
    

    sample_rate, data = wavfile.read(temp_wav)
    print(f"Sample rate: {sample_rate}, Data shape: {data.shape}, Data type: {data.dtype}")
    
    # Убеждаемся, что данные одномерные (моно)
    if len(data.shape) > 1:
        data = data[:, 0]  # Берём первый канал, если вдруг осталось больше
    elif len(data.shape) == 0:
        raise ValueError("Аудиоданные имеют некорректный формат (скаляр)")
    
    # Применяем шумоподавление
    reduced_noise = nr.reduce_noise(y=data, sr=sample_rate)
    wavfile.write(temp_wav, sample_rate, reduced_noise.astype(data.dtype))
    
    # Нормализация громкости
    audio_clean = AudioSegment.from_file(temp_wav).normalize()
    os.remove(temp_wav)
    return audio_clean

def transcribe_audio(audio_path):
    """Распознает речь из аудиофайла и возвращает текст."""
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_file(audio_path)
    
    
    audio = preprocess_audio(audio)
    
    chunk_length_ms = 30000  # 30 секунд
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    full_text = ""

    for i in tqdm(range(len(chunks)), desc="Распознавание аудио"):
        chunk_path = get_temp_audio_path(f"chunk_{i}.wav")
        chunks[i].export(chunk_path, format="wav")
        with sr.AudioFile(chunk_path) as source:
            audio_data = recognizer.record(source)
            max_attempts = 3
            for attempt in range(max_attempts):
                try:
                    text = recognizer.recognize_google(audio_data, language="ru-RU")
                    full_text += text + " "
                    break
                except sr.UnknownValueError:
                    print(f"Часть {i}: не удалось распознать речь")
                    break
                except sr.RequestError as e:
                    print(f"Часть {i}: ошибка запроса Google (попытка {attempt + 1}/{max_attempts}); {e}")
                    if attempt < max_attempts - 1:
                        time.sleep(5)
                    else:
                        print(f"Часть {i}: пропущена из-за лимита")
        os.remove(chunk_path)
    return full_text

def save_text_to_file(text, file_path):
    """Сохраняет текст в указанный файл."""
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)

def transcribe_media(media_path, output_text_path):
    """Основная функция для транскрибации медиафайла."""
    if media_path.endswith((".mp4", ".avi", ".mov")):
        audio_path = get_temp_audio_path("temp_audio.wav")
        extract_audio_from_video(media_path, audio_path)
    elif media_path.endswith((".wav", ".mp3", ".flac")):
        audio_path = media_path
    else:
        raise ValueError("Неподдерживаемый формат файла")

    text = transcribe_audio(audio_path)
    save_text_to_file(text, output_text_path)

    if media_path.endswith((".mp4", ".avi", ".mov")):
        os.remove(audio_path)