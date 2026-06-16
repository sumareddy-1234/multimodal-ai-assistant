import os
import torch
from TTS.api import TTS

class TTSProcessor:
    def __init__(self, model_name="tts_models/en/ljspeech/fast_pitch"):
        # Coqui TTS uses device configuration
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        try:
            # Using a fast, lightweight model to ensure it runs without taking too much memory/time
            self.tts = TTS(model_name=model_name).to(self.device)
        except Exception as e:
            print(f"Failed to load TTS model: {e}")
            self.tts = None

    def synthesize_speech(self, text: str, output_path="output.wav") -> str:
        """
        Converts text to speech and saves it to a file.
        Returns the path to the generated audio file.
        """
        if not self.tts:
            return None
        
        if not text:
            return None

        try:
            # Ensure the output directory exists
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            
            # Fast pitch doesn't require speaker_wav, so simple tts_to_file works well
            self.tts.tts_to_file(text=text, file_path=output_path)
            return output_path
        except Exception as e:
            print(f"Error during TTS synthesis: {e}")
            return None
