import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import librosa

class AudioProcessor:
    def __init__(self, model_id="openai/whisper-base"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        try:
            self.processor = WhisperProcessor.from_pretrained(model_id)
            self.model = WhisperForConditionalGeneration.from_pretrained(model_id).to(self.device)
            self.model.config.forced_decoder_ids = None
        except Exception as e:
            print(f"Failed to load audio processing model: {e}")
            self.processor = None
            self.model = None

    def process_audio(self, audio_path: str) -> str:
        """
        Accepts an audio file path, loads it, and transcribes it using Whisper.
        """
        if not self.processor or not self.model:
            return "Error: Audio processing model not loaded."

        try:
            # Whisper expects 16000Hz sampling rate
            speech, sampling_rate = librosa.load(audio_path, sr=16000)
        except Exception as e:
            return f"Error loading audio file: {str(e)}"

        try:
            input_features = self.processor(speech, sampling_rate=16000, return_tensors="pt").input_features.to(self.device)
            predicted_ids = self.model.generate(input_features, max_new_tokens=255)
            transcription = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
            return transcription.strip()
        except Exception as e:
            return f"Error during transcription: {str(e)}"
