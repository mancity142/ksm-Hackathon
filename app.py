from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import google.generativeai as genai
from elevenlabs import generate, save, set_api_key
import os

app = Flask(__name__)
CORS(app)

# ===== SET YOUR API KEYS =====
GEMINI_API_KEY = "AIzaSyAIKCVr85N7ncr7aV2KvfafoJWGfbBo4a8"
ELEVENLABS_API_KEY = "sk_0139e6138d8d624ccbfb297e0462a5186d60e356b6c37276"

# ===== INIT GEMINI API =====
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name="models/gemini-2.5-pro")

# ===== INIT ELEVENLABS API =====
set_api_key(ELEVENLABS_API_KEY)

# ===== MOCK SCRIPT DATABASE =====
script_db = {
    "inception": "DOM COBB: What is the most resilient parasite? A bacteria? A virus? An intestinal worm? An idea.",
    "titanic": "ROSE: I’ll never let go, Jack. I promise.",
    "the matrix": "MORPHEUS: What if I told you that everything you know is a lie?"
}

# ===== ROUTES =====

@app.route("/get_script", methods=["POST"])
def get_script():
    data = request.get_json()
    movie = data.get("movie", "").lower()

    if movie in script_db:
        return jsonify({"script": script_db[movie]})
    else:
        return jsonify({"error": "Script not found."}), 404

@app.route("/analyze_script", methods=["POST"])
def analyze_script():
    data = request.get_json()
    script = data.get("script", "")

    if not script:
        return jsonify({"error": "Script missing."}), 400

    prompt = f"""Analyze and rewrite this movie scene to reflect a completely different emotional tone. 
Change the mood from sad to happy, adjust dialogues accordingly, and retain core characters.\n\nScene:\n{script}"""

    try:
        response = model.generate_content(prompt)
        revised_script = response.text.strip()
        return jsonify({"analysis": revised_script})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/tts", methods=["POST"])
def text_to_speech():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided for TTS."}), 400

    try:
        audio = generate(text=text, voice="Rachel", model="eleven_multilingual_v2")
        output_path = "output.mp3"
        save(audio, output_path)
        return send_file(output_path, mimetype="audio/mpeg")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
