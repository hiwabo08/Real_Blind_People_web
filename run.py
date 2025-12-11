# from App import create_app

# app= create_app()

# if __name__=="__main__":
#     app.run(debug=True,port=5000)




# from flask import Flask, render_template, request, jsonify
# import os
# from dotenv import load_dotenv
# import google.generativeai as genai
# from routes.model import analyze_video

# app = Flask(__name__)

# # Load Gemini API key
# load_dotenv()
# genai.configure(api_key=os.getenv("AIzaSyA-pKwWpXu2EZkaPh5D-RSvIReGWKuIzXA"))

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/api/video-analysis", methods=["POST"])
# def video_analysis():
#     file = request.files.get("video")
#     if not file:
#         return jsonify({"error": "No video provided"}), 400

#     # Simulate analysis (or real Gemini call)
#     result = analyze_video(file)
#     return jsonify(result)

# @app.route("/api/live-stream", methods=["GET"])
# def live_stream():
#     # Simulate repeated 5-sec AI updates
#     simulated_frame = analyze_video(None, simulate_live=True)
#     return jsonify(simulated_frame)

# if __name__ == "__main__":
#     app.run(debug=True)







from flask import Flask, render_template, Response, request, jsonify

import base64
import requests
import json
from App import create_app

app = create_app()

GEMINI_API_KEY = "AIzaSyA-pKwWpXu2EZkaPh5D-RSvIReGWKuIzXA"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + GEMINI_API_KEY

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/analyze_frame', methods=['POST'])
# def analyze_frame():
#     try:
#         data = request.json['image']
#         img_data = base64.b64decode(data.split(',')[1])

#         # Send image to Gemini for description
#         response = requests.post(
#             GEMINI_URL,
#             headers={"Content-Type": "application/json"},
#             json={
#                 "contents": [
#                     {"parts": [{"text": "Describe objects and environment in this image for blind people emotionally."},
#                                {"inline_data": {"mime_type": "image/jpeg", "data": data.split(',')[1]}}]}
#                 ]
#             }
#         )

#         result = response.json()
#         text_output = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No result")
#         return jsonify({"description": text_output})

#     except Exception as e:
#         return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
