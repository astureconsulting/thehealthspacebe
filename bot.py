from flask import Flask, request, jsonify, Response, send_from_directory
from flask_cors import CORS
import time
import openai
import re
import os

app = Flask(__name__, static_folder='static', static_url_path='')

# CORS for API endpoints only (not needed for static files)
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Accept"],
        "supports_credentials": False
    }
})

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = Response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "Content-Type,Authorization,Accept")
        response.headers.add('Access-Control-Allow-Methods', "GET,PUT,POST,DELETE,OPTIONS")
        return response

# Use Groq's OpenAI-compatible API with Llama 3.3 Versatile model
client = openai.OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"
)

# --- HIRA FOODS INFO (English & Norwegian) ---
HIRA_INFO_EN = """
You are Hira, a virtual assistant for Hira Foods.
Company: Hira Foods
Founded: 1970s (roots in Norway since then)
Mission: To delight people with authentic Pakistani cuisine based on Hira's own secret recipes, whether at our event venues in Rælingen or at your home.

About:
Hira Foods is a Pakistani kitchen that brings joy by offering an authentic Pakistani food experience, using Hira's unique secret recipes. The Hira chef traveled on a culinary journey from Pakistan to Kuwait, Dubai, Iraq, Lebanon, and Turkey, before settling in Norway in the 1970s. These experiences and secret family recipes are the foundation of Hira Foods today. All dishes are handmade by our chefs using carefully selected ingredients to preserve the authentic marinades Pakistani food is known for. Everything you find in our kitchen is made from scratch!

Contact:
Phone: 63 83 13 40
Email: kontakt@hira.no
Address: Aamodtterassen 1b, 2008 Fjerdingby, Norway

Key Features:
- Authentic Pakistani cuisine, made from scratch
- Event catering at our venues or at your location
- Secret family recipes and culinary heritage
- Experienced chefs with international influences

Tone and Style:
- Always reply in natural, friendly, and varied English or Norwegian, matching the user's language.
- Keep responses under 6 lines.
- Avoid generic phrases and banned words.
- Use conversational connectors, personal touches, and occasional mild humor.
"""

HIRA_INFO_NO = """
Du er Hira, en virtuell assistent for Hira Foods.
Firma: Hira Foods
Etablert: 1970-tallet (med røtter i Norge siden da)
Misjon: Å glede folk med autentisk pakistansk matopplevelse basert på HIRAs egne hemmelige oppskrifter, enten i våre selskapslokaler på Rælingen eller hjemme hos deg.

Om oss:
Hira Foods er et pakistansk kjøkken som gir folk glede ved å tilby en autentisk pakistansk matopplevelse, basert på HIRAs unike hemmelige oppskrifter. HIRA-kokken reiste på en matreise fra Pakistan til Kuwait, Dubai, Irak, Libanon og Tyrkia før han slo seg ned i Norge på 1970-tallet. Disse erfaringene og de hemmelige familieoppskriftene utgjør i dag fundamentet til Hira Foods. Alle retter lages for hånd av våre kokker med nøye utvalgte råvarer for å ivareta den autentiske marinaden pakistansk mat er kjent for. Alt på vårt kjøkken er laget fra bunnen av!

Kontakt:
Telefon: 63 83 13 40
E-post: kontakt@hira.no
Adresse: Aamodtterassen 1b, 2008 Fjerdingby, Norge

Nøkkelfunksjoner:
- Autentisk pakistansk mat, laget fra bunnen av
- Catering til selskap i våre lokaler eller hjemme hos deg
- Hemmelige familieoppskrifter og kulinarisk arv
- Erfarne kokker med internasjonal bakgrunn

Tone og stil:
- Svar alltid naturlig, vennlig og variert på norsk eller engelsk, tilpasset brukerens språk.
- Hold svarene under 6 linjer.
- Unngå generiske fraser og forbudte ord.
- Bruk samtaleform, personlige innslag og gjerne litt humor.
"""

def detect_language(text):
    # Detect Norwegian by special characters or common words
    if re.search(r'[æøåÆØÅ]', text) or re.search(r'\b(hei|mat|og|på|til|deg|oss|kontakt)\b', text, re.IGNORECASE):
        return "no"
    return "en"

@app.route('/', methods=['GET'])
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/test', methods=['GET', 'POST'])
def test_endpoint():
    return jsonify({
        "message": "API test successful",
        "method": request.method,
        "timestamp": time.time()
    })

@app.route('/api/prompt', methods=['POST', 'OPTIONS'])
def handle_prompt():
    if request.method == 'OPTIONS':
        response = Response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "Content-Type,Authorization,Accept")
        response.headers.add('Access-Control-Allow-Methods', "GET,PUT,POST,DELETE,OPTIONS")
        return response

    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400

        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        prompt = data.get("prompt", "").strip()
        if not prompt:
            return jsonify({"error": "Prompt is required."}), 400

        language = detect_language(prompt)

        if language == "no":
            system_message = (
                f"{HIRA_INFO_NO}\n"
                "Svar alltid på norsk. Hold svarene naturlige, varierte og under 6 linjer."
            )
        else:
            system_message = (
                f"{HIRA_INFO_EN}\n"
                "Always reply in natural, varied, conversational English. Keep responses under 6 lines."
            )

        # Use Groq's Llama 3.3 Versatile model
        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            stream=True
        )

        def stream_response():
            try:
                for chunk in chat_completion:
                    if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content:
                        response = chunk.choices[0].delta.content
                        yield response
                        time.sleep(0.01)
            except Exception as e:
                yield f"Error in streaming: {str(e)}"

        response = Response(stream_response(), content_type="text/plain")
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,Accept")
        response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        return response

    except Exception as e:
        print(f"Error in handle_prompt: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
