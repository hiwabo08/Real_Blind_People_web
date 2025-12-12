


from App import create_app

app = create_app()

if __name__ == '__main__':
    print("🚀 Starting VisionAssist Server...")
    print("📡 API Endpoints:")
    print("   - /api/analyze-frame  (POST) - Analyze webcam frames")
    print("   - /api/system-status  (GET)  - Check system health")
    print("   - /api/test-gemini    (GET)  - Test Gemini API")
    print("   - /api/ping           (GET)  - Basic health check")
    print("\n🌐 Server running on: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
