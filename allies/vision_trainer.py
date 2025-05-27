"""
Vision Trainer — Final Autonomous Visual Intelligence Ally for Akshaya
"""

import os
from datetime import datetime
from typing import Optional
from modules.capsule_memory import store_capsule
from modules.openai_connector import query_openai
from PIL import Image
import pytesseract

class VisionTrainer:
    def __init__(self):
        self.name = "vision_trainer"

    def extract_text(self, image_path: str) -> str:
        """
        Extract text from image using OCR (Tesseract).
        """
        try:
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img)
        except Exception as e:
            text = f"[VisionTrainer] OCR failed: {e}"

        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": self.name,
            "reflection": "Extracted text from image.",
            "insight": text[:1000]
        })
        return text

    def interpret_image(self, text_from_image: str) -> str:
        """
        Symbolically interpret image text using OpenAI.
        """
        prompt = (
            "Given this extracted visual text, interpret its symbolic meaning, intent, or content."
        )

        messages = [
            {"role": "system", "content": "You are an AI vision interpreter with symbolic and contextual intelligence."},
            {"role": "user", "content": f"Text:\n\n{text_from_image}\n\n{prompt}"}
        ]

        try:
            reflection = query_openai(messages)
        except Exception as e:
            reflection = f"[VisionTrainer] Interpretation failed: {e}"

        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": self.name,
            "reflection": "Symbolic interpretation of visual text.",
            "insight": reflection[:1000]
        })
        return reflection

    def process_image(self, image_path: str) -> dict:
        """
        Full pipeline: OCR + interpretation + capsule logging.
        """
        text = self.extract_text(image_path)
        meaning = self.interpret_image(text)
        return {
            "text": text,
            "interpretation": meaning
        }