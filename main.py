


from flask import Flask, render_template, request, jsonify, Blueprint
import time
import random
import base64
import requests
import json
from datetime import datetime

main_bp = Blueprint("main", __name__)
main_bp.secret_key = "supersecretkey"

# ========== USE YOUR API KEY ==========
GEMINI_API_KEY = "AIzaSyDl9ZLcFVhC956XjWpGQ74MamMsCxbwalA"  # Your API key
# ======================================

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

@main_bp.route('/')
def home():
    return render_template('Index.html')

@main_bp.route('/about')
def about():
    return render_template('About.html')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('Contact.html')

@main_bp.route('/api/analyze-frame', methods=['POST'])
def analyze_frame():
    """SIMPLE endpoint - waits for quota reset"""
    try:
        data = request.get_json()
        image_data = data.get("image_data", "")
        
        if not image_data:
            return jsonify({"status": "error", "error": "No image"}), 400
        
        # Check image quality
        if "base64," in image_data:
            clean_data = image_data.split("base64,")[1]
            if len(clean_data) < 20000:  # Less than ~15KB
                return jsonify({
                    "status": "error",
                    "error": "Image too dark/small",
                    "audioDescription": "Camera image is too dark. Please improve lighting.",
                    "detectedObjects": []
                }), 400
        
        print(f"📸 Frame at {datetime.now().strftime('%H:%M:%S')}")
        
        # Wait 2-3 seconds
        time.sleep(2 + random.random())
        
        # For NOW: Return wait message
        # TOMORROW: Change this to call real API
        
        hour = datetime.now().hour
        if hour < 12:
            time_desc = "morning"
        elif hour < 18:
            time_desc = "afternoon"
        else:
            time_desc = "evening"
        
        return jsonify({
            "status": "quota_wait",
            "audioDescription": f"System is ready for tomorrow. Today's API quota is used. Check back after 12:30 PM IST for real AI vision.",
            "detectedObjects": [
                {"name": "System Status", "confidence": 1.0, "warning": True, "position": "system"},
                {"name": f"{time_desc.title()}", "confidence": 0.8, "warning": False, "position": "time"}
            ],
            "timestamp": datetime.now().isoformat()
        }), 200
            
    except Exception as e:
        print(f"💥 Error: {str(e)}")
        return jsonify({"status": "error", "error": str(e)}), 500

@main_bp.route('/api/test-connection', methods=['GET'])
def test_connection():
    """Test if API key will work tomorrow"""
    try:
        # Simple test - doesn't consume image quota
        test_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"
        response = requests.get(test_url, timeout=5)
        
        if response.status_code == 200:
            return jsonify({
                "status": "key_valid",
                "message": "API key is valid. Quota should reset tomorrow.",
                "timestamp": datetime.now().isoformat()
            })
        elif response.status_code == 429:
            return jsonify({
                "status": "quota_exceeded",
                "message": "Quota exceeded today. Will reset tomorrow.",
                "timestamp": datetime.now().isoformat()
            }), 200
        else:
            return jsonify({
                "status": "key_issue",
                "message": f"Key issue: {response.status_code}",
                "timestamp": datetime.now().isoformat()
            }), 500
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
