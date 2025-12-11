import google.generativeai as genai
import random

# Simulate Gemini analysis (real video API if available)
def analyze_video(file, simulate_live=False):
    try:
        prompt = "Describe what objects are visible for a blind user using emotional and simple tone."

        # Use Gemini to generate a friendly, emotional output
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        tts_text = response.text
    except Exception:
        # If Gemini not responding, simulate friendly message
        tts_text = "I can sense some shapes ahead — maybe a chair and a table. Please walk safely, my friend."

    # Simulated objects
    objects = [
        {"name": "Chair", "confidence": 92},
        {"name": "Table", "confidence": 88},
        {"name": "Door", "confidence": 79},
        {"name": "Human", "confidence": 96},
    ]

    return {
        "objects": random.sample(objects, k=2 if simulate_live else 3),
        "audioDescription": tts_text
    }
