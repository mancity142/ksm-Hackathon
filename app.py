from flask import Flask, render_template, request
import openai
import google.generativeai as genai
import os

app = Flask(__name__)

# --- API KEYS ---
GOOGLE_API_KEY = "AIzaSyB6dPCXjUXmbvmZTYAP3dSs_0vh8qrTaCc"
OPENAI_API_KEY = "your-openai-api-key"

# --- Configure APIs ---
genai.configure(api_key=GOOGLE_API_KEY)
openai.api_key = OPENAI_API_KEY
gemini_model = genai.GenerativeModel('models/gemini-2.5-pro')


# --- Routes ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']

    # Step 1: Generate Scene with Gemini
    gemini_response = gemini_model.generate_content(f"Describe a detailed visual scene: {prompt}")
    scene_text = gemini_response.text.strip()

    # Step 2: Generate Image with DALL·E
    openai_response = openai.Image.create(
        prompt=scene_text,
        n=1,
        size="512x512"
    )
    image_url = openai_response['data'][0]['url']

    return render_template('index.html', original=prompt, scene_text=scene_text, image_url=image_url)


if __name__ == '__main__':
    app.run(debug=True)
