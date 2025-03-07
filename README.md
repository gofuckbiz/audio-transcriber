# Транскрибатор

Проект для транскрибирования видео и аудио в текст.

## Зависимости

Проект использует следующие библиотеки:

- SpeechRecognition==3.8.1
- moviepy==1.0.3
- pydub==0.25.1
- tqdm==4.67.1
- noisereduce==3.0.2
- scipy==1.14.1
- numpy==2.0.2
- openai-whisper==20231117

### Установка зависимостей

pip install -r requirements.txt или  pip install SpeechRecognition==3.8.1 moviepy==1.0.3 pydub==0.25.1 tqdm==4.67.1 noisereduce==3.0.2 scipy==1.14.1 numpy==2.0.2

### Установка FFmpeg Ubuntu
sudo apt update
sudo apt install ffmpeg
ffmpeg -version

### Установка FFmpeg Windows10
1. https://ffmpeg.org/download.html
2. Распакуй на диск C:/ffmpeg
3. Перейди в поиск windows , набери : "переменные среды и нажми на первое" , далее жмешь внизу на "переменные среды" там ищешь "Path" тыкаешь туда и копируешь путь до ffmpeg/bin и добавляешь в Path
4. ffmpeg -version



### Запуск
python main.py