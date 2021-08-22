from celery import shared_task
from .models import Meeting, PartitionTranscript
from moviepy.editor import VideoFileClip
from pathlib import Path
from django.core.files import File
import json
import os
import wave
from vosk import Model, KaldiRecognizer, SetLogLevel

@shared_task
def video2audio(meeting_id: int) -> Meeting:
    """ Получаем из видео файла аудио дорожку
    (кодек PCMs16LE, моно, дискритизация: 8000Гц, битность: 16, скорость: 1.2) """
    meeting = Meeting.objects.get(pk=meeting_id)
    video_path = Path(meeting.video_file.path)
    audio_path = Path(video_path.parent.parent, 'audio', str(video_path.stem)+'.wav')
    audio_path_mp3 = Path(video_path.parent.parent, 'audio', str(video_path.stem)+'.mp3')
    audio_url = audio_path.name
    audio_url_mp3 = audio_path_mp3.name
    video_path = str(video_path)
    audio_path = str(audio_path)
    audio_path_mp3 = str(audio_path_mp3)
    try:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(
            audio_path,
            fps=8000,
            nbytes=2,
            codec='pcm_s16le',
            ffmpeg_params=['-ac', '1', '-filter:a', 'atempo=1.2'])
        video.audio.write_audiofile(
            audio_path_mp3,
            ffmpeg_params=['-ac', '1', '-filter:a', 'atempo=1.2']
        )
        video.close()
        meeting.status = 1
        af = open(audio_path, 'rb')
        meeting.audio_file.save(audio_url, File(af))
        af.close()
        af = open(audio_path_mp3, 'rb')
        meeting.audio_file_mp3.save(audio_url_mp3, File(af))
        af.close()
        meeting.save()
        audio2text.apply_async(args=[meeting_id])
        return meeting
    except Exception as e:
        print(f"video2audio error: {e}")


@shared_task
def audio2text(meeting_id: int) -> Meeting:
    """ Транскрибация аудио в текст с помощью VOKS """
    model = str(Path(Path.cwd().parent, 'model'))
    meeting = Meeting.objects.get(pk=meeting_id)
    audio_path = meeting.audio_file.path
    print(f"{audio_path=}")
    SetLogLevel(0)
    Model_path = str(Path(Path.cwd().parent, 'model'))
    if not os.path.exists(Model_path):
        print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        exit (1)

    wf = wave.open(audio_path, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print ("Audio file must be WAV format mono PCM.")
        exit (1)

    model = Model(Model_path)
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    while True:
        data = wf.readframes(8196)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            time_result = result.get('result', None)
            if time_result is not None:
                start_time = time_result[0].get('start', None)
                end_time = time_result[-1].get('end', None)
                text = result.get('text', None)
                part_trascript = PartitionTranscript(
                    text=text,
                    start_time=float(start_time),
                    end_time=float(end_time),
                    meeting=meeting
                )
                part_trascript.save()
                meeting.status = 2
                meeting.save()
    return meeting
