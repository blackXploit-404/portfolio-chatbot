import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
CORS(app)

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ ERROR: GEMINI_API_KEY not found in .env file")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# Load "About Me" data
def load_about_me():
    try:
        with open("about_me.txt", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "Bot: No information available."

about_me_data = load_about_me()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        # Pass "About Me" data as context
        prompt = f"{about_me_data}\n\nUser: {user_message}\nBot:"
        
        response = model.generate_content(prompt)
        return jsonify({"response": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
