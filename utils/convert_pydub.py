from pydub import AudioSegment


def convert_to_waw(path):
    audio = AudioSegment.from_ogg(path)
    audio.export('voice.wav', format='wav')


