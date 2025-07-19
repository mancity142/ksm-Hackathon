from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import os

app = Flask(__name__)

# === CONFIGURE GEMINI API ===
GOOGLE_API_KEY = "AIzaSyDy3Cf96QgeW8eLFumryvR5q4dPzfjG4eY"  # 🔁 Replace with your actual Gemini API key
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name="models/gemini-2.5-pro")

# === ROUTE: Home Page ===
@app.route("/")
def home():
    return render_template("index.html")

# === ROUTE: Get Movie Script ===
@app.route("/get_script", methods=["POST"])
def get_script():
    data = request.get_json()
    movie_name = data.get("movie", "").strip()
    if not movie_name:
        return jsonify({"error": "Movie name is required."})

    formatted_name = movie_name.title().replace(" ", "-")
    url = f"https://imsdb.com/scripts/{formatted_name}.html"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            return jsonify({"error": "Movie not found on IMSDB."})

        soup = BeautifulSoup(response.text, "html.parser")
        script_tag = soup.find("td", class_="scrtext")
        if not script_tag:
            return jsonify({"error": "Script not found on the page."})

        script = script_tag.get_text(separator="\n", strip=True)
        return jsonify({"script": script})
    except Exception as e:
        return jsonify({"error": f"Failed to fetch script: {str(e)}"})

# === ROUTE: Analyze with Gemini ===
@app.route("/analyze_script", methods=["POST"])
def analyze_script():
    data = request.get_json()
    script = data.get("script", "").strip()
    if not script:
        return jsonify({"error": "Script is empty."})

    try:
        prompt = f"Analyze the following movie script and give a short summary, mood, genre, and key characters:\n\n{script[:10000]}"
        response = model.generate_content(prompt)
        return jsonify({"analysis": response.text})
    except Exception as e:
        return jsonify({"error": f"Gemini API Error: {str(e)}"})

# === ROUTE: Tag Emotions of Scenes ===
@app.route("/tag_emotions", methods=["POST"])
def tag_emotions():
    data = request.get_json()
    scenes = data.get("scenes", [])

    if not scenes:
        return jsonify({"error": "No scenes provided for tagging."})

    results = []

    for i, scene in enumerate(scenes):
        try:
            prompt = f"""
You are an emotion analysis expert using Plutchik’s Wheel of Emotions and Ekman’s Basic Emotions.
Analyze the following movie scene and provide:
1. Dominant Emotion(s)
2. Justification
3. Characters involved (if identifiable)

Scene {i + 1}:
\"\"\"
{scene.strip()[:3000]}
\"\"\"
"""
            response = model.generate_content(prompt)
            results.append({
                "scene": scene[:200] + "...",
                "analysis": response.text
            })
        except Exception as e:
            results.append({
                "scene": scene[:200] + "...",
                "analysis": f"Error: {str(e)}"
            })

    return jsonify({"emotion_results": results})

# === Run the App ===
if __name__ == "__main__":
    app.run(debug=True)
