from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import time
import openai
import re
import os

app = Flask(__name__)

# Fixed CORS configuration for Railway
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Accept"],
        "supports_credentials": False
    }
})

# Add OPTIONS handler for preflight requests
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = Response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "Content-Type,Authorization,Accept")
        response.headers.add('Access-Control-Allow-Methods', "GET,PUT,POST,DELETE,OPTIONS")
        return response

client = openai.OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"
)

ALMASSA_INFO_AR = """
شركة المساعي هي شركة رائدة في مجال التكنولوجيا والحلول الرقمية المتكاملة. 

العنوان: 
الرياض، المملكة العربية السعودية
الحي الدبلوماسي، شارع الأمير سلطان
برج المساعي، الطابق 12

خدماتنا التفصيلية:
1. تطوير التطبيقات:
   - تطبيقات الويب المتكاملة
   - تطبيقات الجوال 
   - أنظمة إدارة علاقات العملاء 
   - أنظمة تخطيط موارد المؤسسات 

2. التجارة الإلكترونية:
   - متاجر إلكترونية متكاملة
   - حلول الدفع الإلكتروني
   - أنظمة إدارة المخزون
   - تكامل مع منصات التسويق الرقمي

3. تصميم وتجربة المستخدم:
   - تصميم واجهات المستخدم 
   - تحسين تجربة المستخدم 
   - تصميم الهوية البصرية
   - تصميم الشعارات والمواد التسويقية

4. البنية التحتية والسحابة:
   - حلول الاستضافة السحابية
   - إدارة الخوادم والسيرفرات
   - حلول النسخ الاحتياطي
   - البنية التحتية كخدمة 

5. الأمن السيبراني:
   - اختبار الاختراق
   - حلول الحماية من الاختراقات
   - أنظمة كشف التسلل
   - تدقيق أمن المعلومات

6. الذكاء الاصطناعي والبيانات:
   - تحليلات الأعمال
   - تعلم الآلة
   - معالجة اللغات الطبيعية
   - حلول الرؤية الحاسوبية

عملاؤنا يشملون:
- الوزارات والهيئات الحكومية
- الشركات الكبرى والمتوسطة
- المؤسسات المالية والبنوك
- المؤسسات التعليمية
- شركات التجزئة الكبرى

تواصل معنا: 
البريد الإلكتروني: info@almassait.com
الهاتف:  966125124965   
"""

ALMASSA_INFO_EN = """
Almassa is a leading provider of integrated digital technology solutions.

Address:
Riyadh, Saudi Arabia
Diplomatic Quarter, Prince Sultan Road
Almassa Tower, 12th Floor

Our Detailed Services:
1. Application Development:
   - Comprehensive web applications
   - Mobile apps (iOS & Android)
   - Customer Relationship Management (CRM)
   - Enterprise Resource Planning (ERP)

2. E-Commerce Solutions:
   - Complete online stores
   - Electronic payment solutions
   - Inventory management systems
   - Digital marketing platform integration

3. UI/UX Design:
   - User Interface design
   - User Experience optimization
   - Visual identity design
   - Logo and marketing material design

4. Cloud Infrastructure:
   - Cloud hosting solutions
   - Server management
   - Backup solutions
   - Infrastructure as a Service (IaaS)

5. Cybersecurity:
   - Penetration testing
   - Intrusion protection solutions
   - Intrusion detection systems
   - Information security audits

6. AI & Data Solutions:
   - Business analytics
   - Machine learning
   - Natural language processing
   - Computer vision solutions

Our Client Groups Include:
- Government ministries and agencies
- Large and medium enterprises
- Financial institutions and banks
- Educational institutions
- Major retail corporations

Contact Us:
Email: info@almassait.com
Phone: +966125124965
Website: https://almassait.com/
"""

def detect_language(text):
    if re.search(r'[\u0600-\u06FF]', text):
        return "ar"
    return "en"

def clean_arabic_response(text):
    # Clean the Arabic response while keeping email and phone intact
    cleaned_text = re.sub(r'(?<![a-zA-Z0-9@.\-+])[^\u0600-\u06FF\s@.\-+0-9](?![a-zA-Z0-9@.\-+])', '', text)
    return cleaned_text

# Add a health check endpoint
@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        "message": "Almassa AI API is running!", 
        "status": "success",
        "version": "1.0"
    })

# Add a test endpoint
@app.route('/api/test', methods=['GET', 'POST'])
def test_endpoint():
    return jsonify({
        "message": "API test successful",
        "method": request.method,
        "timestamp": time.time()
    })

@app.route('/api/prompt', methods=['POST', 'OPTIONS'])
def handle_prompt():
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        response = Response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "Content-Type,Authorization,Accept")
        response.headers.add('Access-Control-Allow-Methods', "GET,PUT,POST,DELETE,OPTIONS")
        return response

    try:
        # Get JSON data with error handling
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
            
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        prompt = data.get("prompt", "").strip()

        if not prompt:
            return jsonify({"error": "Prompt is required."}), 400

        language = detect_language(prompt)

        if language == "ar":
            system_message = (
                f"أنت مساعد مفيد متخصص في {ALMASSA_INFO_AR}. "
                "يرجى الرد فقط باللغة العربية، ولا تستخدم أي كلمات أو عبارات من لغات أخرى. "
                "مهم جدًا: يجب عليك ذكر البريد الإلكتروني (info@almassait.com) ورقم الهاتف ( 966125124965+ ) بدون ترجمة أو تعديل، "
                "أي أن البريد الإلكتروني ورقم الهاتف يجب أن يبقيا مكتوبين بنفس الشكل الإنجليزي كما هما في النص، "
                "ولا تغيرهما أو تكتبهما بالعربية، باقي الرد يكون عربي فقط."
            )
        else:
            system_message = f"You are a helpful assistant specializing in {ALMASSA_INFO_EN}. Please respond only in English."

        # Test with non-streaming first
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
                        if language == "ar":
                            response = clean_arabic_response(response)
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
        print(f"Error in handle_prompt: {str(e)}")  # Server-side logging
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# Error handlers
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
