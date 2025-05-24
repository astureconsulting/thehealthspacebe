from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import time
import openai
import re
import os
app = Flask(__name__)
CORS(app)
port = int(os.environ.get('PORT', 8000))
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
    # Use a non-greedy match to preserve the email and phone numbers
    cleaned_text = re.sub(r'(?<![a-zA-Z0-9@.\-+])[^\u0600-\u06FF\s@.\-+0-9](?![a-zA-Z0-9@.\-+])', '', text)
    return cleaned_text

@app.route('/api/prompt', methods=['POST'])
def handle_prompt():
    data = request.get_json()
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

    try:
        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
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
                        # Clean the Arabic response while keeping email and phone intact
                        response = clean_arabic_response(response)
                    yield response
                    time.sleep(0.01)

        return Response(stream_response(), content_type="text/plain")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @app.route('/')
# def serve_react():
#     try:
#         return send_from_directory('../frontend/build', 'index.html')
#     except:
#         return jsonify({"message": "Lion Pro Dev API is running!", "status": "success"})

# @app.route('/<path:path>')
# def serve_static_files(path):
#     try:
#         return send_from_directory('../frontend/build', path)
#     except:
#         return send_from_directory('../frontend/build', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))