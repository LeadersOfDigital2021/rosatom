from pydub import AudioSegment
from pydub.silence import split_on_silence
from pathlib import Path


sound_file = AudioSegment.from_wav(str(Path(Path.cwd().parent, 'example', '2021-02-26 СБПиБ  Оперативный совет.wav')))
sound_file_dir = str(Path(Path.cwd().parent, 'example', 'chunk'))
audio_chunks = split_on_silence(sound_file,
                                min_silence_len=500,
                                silence_thresh=-16
                                )

for i, chunk in enumerate(audio_chunks):
    out_file = sound_file_dir+f"chunk{i}.wav"
    print("exporting", out_file)
    chunk.export(out_file, format="wav")
