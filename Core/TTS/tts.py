# Core/TTS/tts.py
import edge_tts
import sounddevice as sd
import soundfile as sf

class TTSEngine:
    def __init__(
            self,
            voice: str,
            rate: str,
            volume: str,
            pitch: str,
            save_path: str
            ):
        self.voice = voice
        self.rate = rate
        self.volume = volume
        self.pitch = pitch
        self.save_path = save_path
    
    async def synthesize(self, text: str):
        await edge_tts.Communicate(
            text,
            voice=self.voice,
            rate=self.rate,
            volume=self.volume,
            pitch=self.pitch
        ).save(self.save_path)

    def play(self):
        data, samplerate = sf.read(self.save_path)
        sd.play(data, samplerate)
        sd.wait()