import asyncio
import websockets
import json
import sys, os
from datetime import datetime
from pathlib import Path
from moviepy.editor import VideoFileClip

text = []
BASE_PATH = Path.cwd()
EXAMPLE_PATH = str(Path(BASE_PATH.parent, 'example'))


def get_videofile_names(dir: str) -> list:
    """ Получаем список видеофайлов без расширения """
    lFiles = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith('.mp4'):
                lFiles.append(str(Path(root, file[:-4])))
    return lFiles


def video2audio(filename: str):
    """ Получаем из видео файла аудио дорожку
    (кодек PCMs16LE, моно, дискритизация: 8000Гц, битность: 16, скорость: 1.2) """
    video_path = filename + '.mp4'
    audio_path = filename + '.wav'
    try:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(
            audio_path,
            fps=8000,
            nbytes=2,
            codec='pcm_s16le',
            ffmpeg_params=['-ac', '1', '-filter:a', 'atempo=1.2'])
        video.close()
    except Exception as e:
        print(f"video2audio error: {e}")


async def sound2text(uri_server: str, filename: str) -> list:
    """ Транскрибация аудио в текст с помощью VOKS-API """
    text = []
    video_path = filename + '.mp4'
    audio_path = filename + '.wav'
    async with websockets.connect(uri_server) as websocket:
        wf = open(audio_path, "rb")
        while True:
            data = wf.read(8192)
            if len(data) == 0:
                break
            await websocket.send(data)
            answer = json.loads(await websocket.recv())
            fragment = answer.get('text', False)
            if fragment and fragment!="":
                text.append(fragment)
        await websocket.send('{"eof" : 1}')
        await websocket.recv()
        return text


def text2file(filename: str, text: list):
    """ Сохраняем результат в тексовый файл
    Примечание: функция только в тестовом режиме, чтобы повторно не осуществлять транскрибацию """
    text_path = filename + '.txt'
    with open(text_path, 'w') as f:
        for fragment in text:
            f.writelines(f"{fragment}\n")


if __name__ == '__main__':
    # замеряем скорость работы транскрибации
    start_time = datetime.now()
    files = get_videofile_names(EXAMPLE_PATH)
    print(f"Start time: {start_time}")
    for file in files:
        video2audio(str(file))
        text = asyncio.get_event_loop().run_until_complete(sound2text('ws://localhost:2700', str(file)))
        print(text)
        text2file(str(file), text)
        break
    print(f"End time: {datetime.now()}")
    print(datetime.now() - start_time)


