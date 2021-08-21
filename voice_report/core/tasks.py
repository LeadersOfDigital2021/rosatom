from celery import shared_task
from .models import Transcript
from moviepy.editor import VideoFileClip
from pathlib import Path
from django.core.files import File
import asyncio
import json
import websockets
import sys
import os
import wave
from vosk import Model, KaldiRecognizer, SetLogLevel


@shared_task
def video2audio(transcript_id: int) -> Transcript:
    """ Получаем из видео файла аудио дорожку
    (кодек PCMs16LE, моно, дискритизация: 8000Гц, битность: 16, скорость: 1.2) """
    transcript = Transcript.objects.get(pk=transcript_id)
    video_path = Path(transcript.video_file.path)
    audio_path = Path(video_path.parent.parent, 'audio', str(video_path.stem)+'.wav')
    audio_url =  audio_path.name
    video_path = str(video_path)
    audio_path = str(audio_path)
    try:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(
            audio_path,
            fps=8000,
            nbytes=2,
            codec='pcm_s16le',
            ffmpeg_params=['-ac', '1', '-filter:a', 'atempo=1.2'])
        video.close()
        transcript.status = 1
        af = open(audio_path, 'rb')
        transcript.audio_file.save(audio_url, File(af))
        af.close()
        transcript.save()
        audio2text.apply_async(args=[transcript_id])
        return transcript
    except Exception as e:
        print(f"video2audio error: {e}")


@shared_task
def audio2text(transcript_id: int) -> Transcript:
    """ Транскрибация аудио в текст с помощью VOKS-API """
    model = str(Path(Path.cwd().parent, 'model'))
    transcript = Transcript.objects.get(pk=transcript_id)
    audio_path = transcript.audio_file.path
    wf = wave.open(audio_path, "rb")
    print(f"{wf.getnchannels()=}")
    print(f"{wf.getsampwidth()=}")
    print(f"{wf.getcomptype()=}")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        exit(1)
    model = Model(model)
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    while True:
        data = wf.readframes(8196)
        # if len(data) == 0:
        #     break
        rec.AcceptWaveform(data)
        res = rec.Result()
        print(res)
        answer = json.loads(res)
        fragment = answer.get('text', False)
        if fragment and fragment != "":
            print(fragment)
            transcript.text = transcript.text + '\n' + fragment
        rec.FinalResult()
        transcript.status = 2
        transcript.save()
        return transcript
