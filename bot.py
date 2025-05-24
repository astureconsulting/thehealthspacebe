from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import time
import openai
import re
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
CONFIG = {
    "GROQ_API_KEY": os.getenv("GROQ_API_KEY", "your-default-key-here"),
    "MODEL": "llama-3.3-70b-versatile",
    "DEFAULT_PORT": 8080,
    "STREAM_DELAY": 0.01
}

# Initialize OpenAI client
client = openai.OpenAI(
    api_key=CONFIG["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

# Company information (moved to separate files would be better in production)
COMPANY_INFO = {
    "ar": ALMASSA_INFO_AR,  # Your Arabic text here
    "en": ALMASSA_INFO_EN   # Your English text here
}

def detect_language(text):
    """Detect if text is Arabic or English"""
    return "ar" if re.search(r'[\u0600-\u06FF]', text) else "en"

def clean_arabic_response(text):
    """Clean Arabic response while preserving contact info"""
    return re.sub(r'(?<![a-zA-Z0-9@.\-+])([^\u0600-\u06FF\s@.\-+0-9])(?![a-zA-Z0-9@.\-+])', '', text)

@app.route('/api/prompt', methods=['POST'])
def handle_prompt():
    """Handle chat prompts with streaming response"""
    try:
        data = request.get_json()
        if not data or "prompt" not in data:
            return jsonify({"error": "Prompt is required."}), 400

        prompt = data["prompt"].strip()
        if not prompt:
            return jsonify({"error": "Prompt cannot be empty."}), 400

        language = detect_language(prompt)
        system_message = (
            f"أنت مساعد مفيد متخصص في {COMPANY_INFO['ar']}. "
            "الردود بالعربية فقط مع الحفاظ على معلومات التواصل بالإنجليزية" 
            if language == "ar" else 
            f"You are a helpful assistant specializing in {COMPANY_INFO['en']}. "
            "Respond only in English."
        )

        chat_completion = client.chat.completions.create(
            model=CONFIG["MODEL"],
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            stream=True
        )

        def stream_response():
            for chunk in chat_completion:
                if chunk.choices[0].delta.content:
                    response = chunk.choices[0].delta.content
                    if language == "ar":
                        response = clean_arabic_response(response)
                    yield response
                    time.sleep(CONFIG["STREAM_DELAY"])

        return Response(stream_response(), mimetype="text/plain")

    except Exception as e:
        app.logger.error(f"Error processing prompt: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    port = int(os.getenv("PORT", CONFIG["DEFAULT_PORT"]))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true"
    )