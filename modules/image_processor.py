import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

class ImageProcessor:
    def __init__(self, model_id="Salesforce/blip-image-captioning-base"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        try:
            self.processor = BlipProcessor.from_pretrained(model_id)
            self.model = BlipForConditionalGeneration.from_pretrained(model_id).to(self.device)
        except Exception as e:
            print(f"Failed to load image processing model: {e}")
            self.processor = None
            self.model = None

    def process_image(self, image_path: str) -> str:
        """
        Accepts an image path, loads it using PIL, and generates a descriptive caption using BLIP.
        """
        if not self.processor or not self.model:
            return "Error: Image processing model not loaded."

        try:
            raw_image = Image.open(image_path).convert('RGB')
        except Exception as e:
            return f"Error loading image: {str(e)}"

        try:
            inputs = self.processor(raw_image, return_tensors="pt").to(self.device)
            out = self.model.generate(**inputs, max_new_tokens=50)
            caption = self.processor.decode(out[0], skip_special_tokens=True)
            return caption
        except Exception as e:
            return f"Error generating caption: {str(e)}"
