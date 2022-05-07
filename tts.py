from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import tempfile


def play_tts(text: str):
    tts = gTTS(text, lang="pt", tld="com.br")
    with tempfile.TemporaryDirectory() as tmpdirname:
        file = f"{tmpdirname}\\tmp.mp3"
        tts.save(file)
        song = AudioSegment.from_mp3(file)
        play(song)
