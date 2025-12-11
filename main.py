# from flask import Flask, render_template, request, jsonify, Blueprint
# import requests
# import base64
# import time

# main_bp = Blueprint("main", __name__)
# main_bp.secret_key = "supersecretkey"  # for flash messages

# # ---------------------------
# # Your Gemini API key (add here)
# # ---------------------------
# GEMINI_API_KEY = "AIzaSyA-pKwWpXu2EZkaPh5D-RSvIReGWKuIzXA"  # 🔑 Replace with your key if needed

# # ---------------------------
# # Home, About, Contact routes
# # ---------------------------
# @main_bp.route('/')
# def home():
#     return render_template('index.html')

# @main_bp.route('/about')
# def about():
#     return render_template('About.html')

# @main_bp.route('/contact', methods=['GET', 'POST'])
# def contact():
#     # Your existing email form logic here
#     return render_template('Contact.html')


# # ---------------------------
# # Live Video Frame Analysis
# # ---------------------------
# # @main_bp.route('/api/analyze-frame', methods=['POST'])
# # def analyze_frame_endpoint():
# #     """
# #     Receives a video frame (base64) and sends it to Gemini AI for dynamic analysis.
# #     Returns detected objects + description.
# #     """
# #     try:
# #         data = request.json
# #         image_data = data.get("image_data")
# #         prompt_text = "Describe what the blind user is seeing and warn about obstacles."

# #         if not image_data:
# #             return jsonify({"error": "No image data received"}), 400

# #         # -------------------------
# #         # Prepare the payload for Gemini
# #         # -------------------------
# #         # image_data is base64, remove the "data:image/jpeg;base64," prefix if exists
# #         if image_data.startswith("data:image"):
# #             image_data = image_data.split(",")[1]

# #         payload = {
# #             "prompt": prompt_text,
# #             "image_base64": image_data
# #         }

# #         headers = {
# #             "Authorization": f"Bearer {GEMINI_API_KEY}",
# #             "Content-Type": "application/json"
# #         }

# #         # -------------------------
# #         # Call Gemini API
# #         # -------------------------
# #         response = requests.post(
# #             "https://api.openai.com/v1/vision/describe",  # Replace with correct Gemini endpoint
# #             headers=headers,
# #             json=payload,
# #             timeout=10
# #         )

# #         if response.status_code != 200:
# #             return jsonify({"error": f"AI API error: {response.text}"}), 500

# #         ai_result = response.json()

# #         # Example structure returned by Gemini (adjust if different)
# #         description = ai_result.get("description", "No description returned")
# #         detected_objects = ai_result.get("objects", [])

# #         # -------------------------
# #         # Add small delay to avoid API overload (2 sec)
# #         # -------------------------
# #         time.sleep(2)

# #         return jsonify({
# #             "status": "ok",
# #             "prompt_used": prompt_text,
# #             "audioDescription": description,
# #             "detectedObjects": detected_objects
# #         }), 200

# #     except Exception as e:
# #         print("Error in /api/analyze-frame:", e)
# #         return jsonify({"error": "Internal server error"}), 500











# @main_bp.route('/api/analyze-frame', methods=['POST'])
# def analyze_frame_endpoint():
#     try:
#         data = request.json
#         image_data = data.get("image_data")
#         prompt_text = "Describe what the blind user is seeing and warn about obstacles."

#         if not image_data:
#             return jsonify({"error": "No image data received"}), 400

#         if image_data.startswith("data:image"):
#             image_data = image_data.split(",")[1]

#         payload = {
#             "prompt": prompt_text,
#             "image_base64": image_data
#         }

#         headers = {
#             "Authorization": f"Bearer {GEMINI_API_KEY}",
#             "Content-Type": "application/json"
#         }

#         response = requests.post(
#             "https://api.openai.com/v1/vision/describe",  # check endpoint
#             headers=headers,
#             json=payload,
#             timeout=10
#         )

#         print("Gemini API status:", response.status_code)
#         print("Gemini API response:", response.text)

#         response.raise_for_status()  # Raise error if status code not 2xx

#         ai_result = response.json()
#         description = ai_result.get("description", "No description returned")
#         detected_objects = ai_result.get("objects", [])

#         time.sleep(2)  # 2 sec delay

#         return jsonify({
#             "status": "ok",
#             "prompt_used": prompt_text,
#             "audioDescription": description,
#             "detectedObjects": detected_objects
#         }), 200

#     except requests.exceptions.RequestException as re:
#         print("Requests error:", re)
#         return jsonify({"error": "Error calling Gemini API"}), 500
#     except Exception as e:
#         print("General error:", e)
#         return jsonify({"error": "Internal server error"}), 500















from flask import Flask, render_template, request, jsonify, Blueprint
import time
import random

main_bp = Blueprint("main", __name__)
main_bp.secret_key = "supersecretkey"  # for flash messages

# ---------------------------
# Home, About, Contact routes
# ---------------------------
@main_bp.route('/')
def home():
    return render_template('index.html')

@main_bp.route('/about')
def about():
    return render_template('About.html')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    # Your existing email form logic here
    return render_template('Contact.html')


# ---------------------------
# MOCK AI RESPONSES for testing dynamic output
# ---------------------------
LIVE_MOCK_RESPONSES = [
    {
        "detectedObjects": [
            {"name": "mug on desk", "confidence": 0.95, "warning": False},
            {"name": "keyboard", "confidence": 0.92, "warning": False}
        ],
        "audioDescription": "I see a mug on the desk to your right. The keyboard is centered."
    },
    {
        "detectedObjects": [
            {"name": "doorway", "confidence": 0.88, "warning": False},
            {"name": "small box on floor", "confidence": 0.75, "warning": True}
        ],
        "audioDescription": "You are facing a doorway. Warning: There is a small box on the floor straight ahead."
    },
    {
        "detectedObjects": [
            {"name": "chair", "confidence": 0.90, "warning": False},
            {"name": "laptop", "confidence": 0.93, "warning": False}
        ],
        "audioDescription": "A chair is in front of you. The laptop is on the table slightly to your left."
    }
]

STATIC_PROMPT = "Describe what the blind user is seeing and warn about obstacles."


# ---------------------------
# Live Video Frame Analysis Endpoint
# ---------------------------
@main_bp.route('/api/analyze-frame', methods=['POST'])
def analyze_frame_endpoint():
    try:
        data = request.json
        image_data = data.get("image_data")

        if not image_data:
            return jsonify({"error": "No image data received"}), 400

        # Simulate AI delay 2-3 seconds
        time.sleep(2 + random.random())

        # Pick a random mock response to simulate dynamic output
        response = random.choice(LIVE_MOCK_RESPONSES)

        return jsonify({
            "status": "ok",
            "prompt_used": STATIC_PROMPT,
            "audioDescription": response["audioDescription"],
            "detectedObjects": response["detectedObjects"]
        }), 200

    except Exception as e:
        print("Error in /api/analyze-frame:", e)
        return jsonify({"error": "Internal server error"}), 500





















