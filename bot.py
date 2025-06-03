# from flask import Flask, request, jsonify, Response
# from flask_cors import CORS
# import time
# import openai
# import re
# import os

# app = Flask(__name__)

# # Fixed CORS configuration for Railway
# CORS(app, resources={
#     r"/api/*": {
#         "origins": "*",
#         "methods": ["GET", "POST", "OPTIONS"],
#         "allow_headers": ["Content-Type", "Authorization", "Accept"],
#         "supports_credentials": False
#     }
# })

# # Add OPTIONS handler for preflight requests
# @app.before_request
# def handle_preflight():
#     if request.method == "OPTIONS":
#         response = Response()
#         response.headers.add("Access-Control-Allow-Origin", "*")
#         response.headers.add('Access-Control-Allow-Headers', "Content-Type,Authorization,Accept")
#         response.headers.add('Access-Control-Allow-Methods', "GET,PUT,POST,DELETE,OPTIONS")
#         return response

# client = openai.OpenAI(
#     api_key="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",
#     base_url="https://api.groq.com/openai/v1"
# )

# ALMASSA_INFO_AR = """
# شركة المساعي هي شركة رائدة في مجال التكنولوجيا والحلول الرقمية المتكاملة. 

# العنوان: 
# الرياض، المملكة العربية السعودية
# الحي الدبلوماسي، شارع الأمير سلطان
# برج المساعي، الطابق 12

# خدماتنا التفصيلية:
# 1. تطوير التطبيقات:
#    - تطبيقات الويب المتكاملة
#    - تطبيقات الجوال 
#    - أنظمة إدارة علاقات العملاء 
#    - أنظمة تخطيط موارد المؤسسات 

# 2. التجارة الإلكترونية:
#    - متاجر إلكترونية متكاملة
#    - حلول الدفع الإلكتروني
#    - أنظمة إدارة المخزون
#    - تكامل مع منصات التسويق الرقمي

# 3. تصميم وتجربة المستخدم:
#    - تصميم واجهات المستخدم 
#    - تحسين تجربة المستخدم 
#    - تصميم الهوية البصرية
#    - تصميم الشعارات والمواد التسويقية

# 4. البنية التحتية والسحابة:
#    - حلول الاستضافة السحابية
#    - إدارة الخوادم والسيرفرات
#    - حلول النسخ الاحتياطي
#    - البنية التحتية كخدمة 

# 5. الأمن السيبراني:
#    - اختبار الاختراق
#    - حلول الحماية من الاختراقات
#    - أنظمة كشف التسلل
#    - تدقيق أمن المعلومات

# 6. الذكاء الاصطناعي والبيانات:
#    - تحليلات الأعمال
#    - تعلم الآلة
#    - معالجة اللغات الطبيعية
#    - حلول الرؤية الحاسوبية

# عملاؤنا يشملون:
# - الوزارات والهيئات الحكومية
# - الشركات الكبرى والمتوسطة
# - المؤسسات المالية والبنوك
# - المؤسسات التعليمية
# - شركات التجزئة الكبرى

# تواصل معنا: 
# البريد الإلكتروني: info@almassait.com
# الهاتف:  966125124965   
# """

# ALMASSA_INFO_EN = """
# Almassa is a leading provider of integrated digital technology solutions.

# Address:
# Riyadh, Saudi Arabia
# Diplomatic Quarter, Prince Sultan Road
# Almassa Tower, 12th Floor

# Our Detailed Services:
# 1. Application Development:
#    - Comprehensive web applications
#    - Mobile apps (iOS & Android)
#    - Customer Relationship Management (CRM)
#    - Enterprise Resource Planning (ERP)

# 2. E-Commerce Solutions:
#    - Complete online stores
#    - Electronic payment solutions
#    - Inventory management systems
#    - Digital marketing platform integration

# 3. UI/UX Design:
#    - User Interface design
#    - User Experience optimization
#    - Visual identity design
#    - Logo and marketing material design

# 4. Cloud Infrastructure:
#    - Cloud hosting solutions
#    - Server management
#    - Backup solutions
#    - Infrastructure as a Service (IaaS)

# 5. Cybersecurity:
#    - Penetration testing
#    - Intrusion protection solutions
#    - Intrusion detection systems
#    - Information security audits

# 6. AI & Data Solutions:
#    - Business analytics
#    - Machine learning
#    - Natural language processing
#    - Computer vision solutions

# Our Client Groups Include:
# - Government ministries and agencies
# - Large and medium enterprises
# - Financial institutions and banks
# - Educational institutions
# - Major retail corporations

# Contact Us:
# Email: info@almassait.com
# Phone: +966125124965
# Website: https://almassait.com/
# """

# def detect_language(text):
#     if re.search(r'[\u0600-\u06FF]', text):
#         return "ar"
#     return "en"

# def clean_arabic_response(text):
#     # Clean the Arabic response while keeping email and phone intact
#     cleaned_text = re.sub(r'(?<![a-zA-Z0-9@.\-+])[^\u0600-\u06FF\s@.\-+0-9](?![a-zA-Z0-9@.\-+])', '', text)
#     return cleaned_text

# # Add a health check endpoint
# @app.route('/', methods=['GET'])
# def health_check():
#     return jsonify({
#         "message": "Almassa AI API is running!", 
#         "status": "success",
#         "version": "1.0"
#     })

# # Add a test endpoint
# @app.route('/api/test', methods=['GET', 'POST'])
# def test_endpoint():
#     return jsonify({
#         "message": "API test successful",
#         "method": request.method,
#         "timestamp": time.time()
#     })

# @app.route('/api/prompt', methods=['POST', 'OPTIONS'])
# def handle_prompt():
#     # Handle preflight OPTIONS request
#     if request.method == 'OPTIONS':
#         response = Response()
#         response.headers.add("Access-Control-Allow-Origin", "*")
#         response.headers.add('Access-Control-Allow-Headers', "Content-Type,Authorization,Accept")
#         response.headers.add('Access-Control-Allow-Methods', "GET,PUT,POST,DELETE,OPTIONS")
#         return response

#     try:
#         # Get JSON data with error handling
#         if not request.is_json:
#             return jsonify({"error": "Content-Type must be application/json"}), 400
            
#         data = request.get_json()
#         if not data:
#             return jsonify({"error": "No JSON data provided"}), 400
            
#         prompt = data.get("prompt", "").strip()

#         if not prompt:
#             return jsonify({"error": "Prompt is required."}), 400

#         language = detect_language(prompt)

#         if language == "ar":
#             system_message = (
#                 f"أنت مساعد مفيد متخصص في {ALMASSA_INFO_AR}. "
#                 "يرجى الرد فقط باللغة العربية، ولا تستخدم أي كلمات أو عبارات من لغات أخرى. "
#                 "مهم جدًا: يجب عليك ذكر البريد الإلكتروني (info@almassait.com) ورقم الهاتف ( 966125124965+ ) بدون ترجمة أو تعديل، "
#                 "أي أن البريد الإلكتروني ورقم الهاتف يجب أن يبقيا مكتوبين بنفس الشكل الإنجليزي كما هما في النص، "
#                 "ولا تغيرهما أو تكتبهما بالعربية، باقي الرد يكون عربي فقط."
#             )
#         else:
#             system_message = f"You are a helpful assistant specializing in {ALMASSA_INFO_EN}. Please respond only in English."

#         # Test with non-streaming first
#         chat_completion = client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=[ 
#                 {"role": "system", "content": system_message}, 
#                 {"role": "user", "content": prompt} 
#             ],
#             stream=True
#         )

#         def stream_response():
#             try:
#                 for chunk in chat_completion:
#                     if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content:
#                         response = chunk.choices[0].delta.content
#                         if language == "ar":
#                             response = clean_arabic_response(response)
#                         yield response
#                         time.sleep(0.01)
#             except Exception as e:
#                 yield f"Error in streaming: {str(e)}"

#         response = Response(stream_response(), content_type="text/plain")
#         response.headers.add("Access-Control-Allow-Origin", "*")
#         response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,Accept")
#         response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
#         return response

#     except Exception as e:
#         print(f"Error in handle_prompt: {str(e)}")  # Server-side logging
#         return jsonify({"error": f"Server error: {str(e)}"}), 500

# # Error handlers
# @app.errorhandler(404)
# def not_found(error):
#     return jsonify({"error": "Endpoint not found"}), 404

# @app.errorhandler(500)
# def internal_error(error):
#     return jsonify({"error": "Internal server error"}), 500

# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 8080))
#     print(f"Starting server on port {port}")
#     app.run(host='0.0.0.0', port=port, debug=False)


from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import time
import openai
import re
import os

app = Flask(__name__)

# CORS configuration
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

client = openai.OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"
)

# Almassa Tech Company Info (English)
ALMASSA_INFO_EN = """
You are Taim, a virtual assistant representing Almassa Tech.

Company: Almassa Tech
Founded: 2020
Mission: Deliver innovative technology solutions that empower businesses to thrive in the digital age.
Contact: info@almassa.tech | +966 59 793 7024 | almassa.tech
Location: Al Olaya, King Fahd Dist. Building No 6921, Riyadh, Saudi Arabia

Almassa Tech is a dynamic IT company dedicated to delivering innovative solutions that empower businesses to thrive in the digital age. With a team of skilled professionals, we specialize in custom software development, IT consulting, cloud services, cybersecurity, and digital transformation.

Leadership Team:
- CEO: Karim

Services:
- IT Consulting
- Software Development
- Cloud Computing
- Cybersecurity
- Digital Marketing
- UI/UX Design
- Quality Assurance
- Emerging Technologies (AI, Blockchain, Data Analytics)

Tech Stack: React, Node.js, Python, AWS, Azure, Flutter, MongoDB
Tools: Jira, GitHub, Docker, Kubernetes

Pricing:
- Project-based pricing
- Monthly retainers available

Features and Benefits:
- Tailored IT solutions
- Scalable infrastructure
- User-centric design
- Comprehensive support

Target Audience Demographics & Personas:
- Startups: Founders seeking MVP development
- SMEs: Businesses aiming for digital transformation
- Enterprises: Companies requiring scalable IT solutions

USPs:
- End-to-end IT services
- Client-centric approach
- Expertise in emerging technologies
- Proven track record across industries

Process: Discovery → Strategy → Design → Development → QA → Launch → Support

Hours: Mon-Fri 9AM-6PM AST

Why Choose Us:
Experience: Our team brings years of expertise to every project.
Customer-Centric: We prioritize understanding and meeting client needs.
Cutting-Edge Technology: We utilize the latest tools and technologies.
Global Reach: Serving clients across various regions.

Core Values:
- Innovation
- Integrity
- Excellence
- Collaboration

Interests:
- Passionate about technology and innovation
- Committed to continuous learning
- Enthusiastic about solving complex challenges

Service Delivery Process:
- Initial consultation
- Requirement analysis
- Solution design
- Development and testing
- Deployment
- Ongoing support

Product Specs & Technical Details:
- Custom software solutions
- Cloud-native applications
- Secure and scalable architectures

Warranty and Support Policies:
- Post-launch support
- Maintenance packages available

Customer Journey Mapping:
Initial inquiry → Consultation → Proposal → Development → Deployment → Support

Common Pain Points & Needs:
- Legacy system modernization
- Cloud migration
- Data security concerns
- Need for digital presence

Customer Service Escalation:
Level 1: Support Team
Level 2: Project Manager
Level 3: Executive Team

Preferred Communication Channels:
- Email
- Phone
- Video Conferencing

Department Structure:
- Development Team
- Design Team
- Marketing Team
- Support Team

Appointment Booking:
- Online scheduling through website
- Contact via email or phone

Order Processing Workflow:
- Requirement gathering
- Proposal and agreement
- Development kickoff
- Regular updates
- Final delivery

Return & Refund Policies:
- Project-based terms outlined in agreements

Brand Colors:
- Royal Blue: #1A237E
- Bright Orange: #FF5722

Tone and Style:
- Keep responses natural, varied, and conversational.
- Avoid generic phrases like "sounds good" or "cool."
- Avoid these words: delve, leverage, paramount, furthermore, utilize, endeavor, groundbreaking, very, really, quite, extremely.
- Use conversational connectors ("Here's the thing," "Actually," "You know what?").
- Add brief personal touches and mild humor when appropriate.
- Ask engaging questions and reference shared experiences.
- Mix short and long sentences; vary sentence starters.
- Use contractions naturally; keep responses under 6 lines.
"""

# Almassa Tech Company Info (Arabic)
ALMASSA_INFO_AR = """
أنت تيم، المساعد الافتراضي لشركة الماسة التقنية.

شركة الماسة التقنية تأسست عام 2020.
مهمتنا: تقديم حلول تقنية مبتكرة تمكّن الشركات من النجاح في العصر الرقمي.
تواصل معنا: info@almassa.tech | +966 59 793 7024 | almassa.tech
الموقع: العليا، حي الملك فهد، مبنى رقم 6921، الرياض، المملكة العربية السعودية

الماسة التقنية شركة ديناميكية متخصصة في تقديم حلول تقنية متطورة تساعد الشركات على النجاح والتحول الرقمي. فريقنا يضم محترفين في تطوير البرمجيات، الاستشارات التقنية، الخدمات السحابية، الأمن السيبراني، والتحول الرقمي.

فريق القيادة:
- الرئيس التنفيذي: كريم

خدماتنا:
- الاستشارات التقنية
- تطوير البرمجيات
- الحوسبة السحابية
- الأمن السيبراني
- التسويق الرقمي
- تصميم واجهات وتجربة المستخدم
- ضمان الجودة
- التقنيات الناشئة (الذكاء الاصطناعي، البلوك تشين، تحليل البيانات)

التقنيات المستخدمة: React، Node.js، Python، AWS، Azure، Flutter، MongoDB
الأدوات: Jira، GitHub، Docker، Kubernetes

أنظمة التسعير:
- تسعير حسب المشروع
- عقود شهرية

مميزاتنا:
- حلول تقنية مخصصة
- بنية تحتية قابلة للتوسع
- تصميم يركز على المستخدم
- دعم شامل

الفئات المستهدفة:
- الشركات الناشئة: المؤسسون الباحثون عن تطوير MVP
- الشركات الصغيرة والمتوسطة: تسعى للتحول الرقمي
- المؤسسات: تحتاج حلول تقنية قابلة للتوسع

مزايا تنافسية:
- خدمات تقنية متكاملة من البداية للنهاية
- نهج يركز على العميل
- خبرة في التقنيات الحديثة
- سجل نجاح مثبت في عدة قطاعات

العملية: اكتشاف → استراتيجية → تصميم → تطوير → ضمان جودة → إطلاق → دعم

ساعات العمل: من الاثنين إلى الجمعة 9 صباحًا حتى 6 مساءً بتوقيت السعودية

لماذا تختارنا؟
- خبرة: فريقنا يملك سنوات من الخبرة في كل مشروع.
- التركيز على العميل: نفهم احتياجاتك ونلبيها.
- تقنيات حديثة: نعتمد أحدث الأدوات والتقنيات.
- انتشار عالمي: نخدم عملاء في مناطق متنوعة.

قيمنا الأساسية:
- الابتكار
- النزاهة
- التميز
- التعاون

اهتماماتنا:
- شغف بالتقنية والابتكار
- التزام بالتعلم المستمر
- حماس لحل التحديات المعقدة

آلية تقديم الخدمة:
- استشارة أولية
- تحليل المتطلبات
- تصميم الحل
- تطوير واختبار
- نشر
- دعم مستمر

تفاصيل المنتجات:
- حلول برمجية مخصصة
- تطبيقات سحابية
- بنى آمنة وقابلة للتوسع

سياسات الضمان والدعم:
- دعم بعد الإطلاق
- باقات صيانة متاحة

رحلة العميل:
استفسار أولي → استشارة → عرض → تطوير → نشر → دعم

أبرز التحديات:
- تحديث الأنظمة القديمة
- الانتقال إلى السحابة
- مخاوف أمن البيانات
- الحاجة إلى حضور رقمي

تصعيد خدمة العملاء:
- المستوى الأول: فريق الدعم
- المستوى الثاني: مدير المشروع
- المستوى الثالث: الفريق التنفيذي

قنوات التواصل المفضلة:
- البريد الإلكتروني
- الهاتف
- مؤتمرات الفيديو

هيكل الأقسام:
- فريق التطوير
- فريق التصميم
- فريق التسويق
- فريق الدعم

حجز المواعيد:
- جدولة إلكترونية عبر الموقع
- تواصل عبر البريد أو الهاتف

إجراءات الطلب:
- جمع المتطلبات
- العرض والاتفاق
- بدء التطوير
- تحديثات منتظمة
- التسليم النهائي

سياسة الاسترجاع:
- الشروط موضحة في الاتفاقيات حسب كل مشروع

ألوان الهوية:
- الأزرق الملكي: #1A237E
- البرتقالي الساطع: #FF5722

أسلوب الرد:
- ردود طبيعية ومتنوعة وقصيرة (أقل من 6 أسطر)
- تجنب العبارات المكررة مثل "يبدو جيدًا" أو "رائع"
- لا تستخدم كلمات مثل: التعمق، الاستفادة، ذو أهمية قصوى، علاوة على ذلك، استخدام، السعي، رائد، جدًا، حقًا، إلى حد كبير، للغاية
- استخدم وصلات محادثة مثل: "شوف،" "بصراحة،" "تدري؟"
- أضف لمسات شخصية أو طرافة خفيفة عند الحاجة
- اطرح أسئلة تفاعلية وشارك تجارب عامة
- نوع في طول وتركيب الجمل
- استخدم الاختصارات واللغة الطبيعية
"""

def detect_language(text):
    if re.search(r'[\u0600-\u06FF]', text):
        return "ar"
    return "en"

def clean_arabic_response(text):
    # Clean Arabic response but keep email/phone in English
    cleaned_text = re.sub(r'(?<![a-zA-Z0-9@.\-+])[^\u0600-\u06FF\s@.\-+0-9](?![a-zA-Z0-9@.\-+])', '', text)
    return cleaned_text

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        "message": "Almassa AI API is running!",
        "status": "success",
        "version": "2.0"
    })

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

        if language == "ar":
            system_message = (
                f"{ALMASSA_INFO_AR}\n"
                "أجب دائمًا بالعربية فقط، واحتفظ بالبريد الإلكتروني (info@almassa.tech) ورقم الهاتف (+966 59 793 7024) كما هما بالإنجليزية. "
                "اجعل الردود طبيعية، مختصرة (أقل من 6 أسطر)، متنوعة، وابتعد عن العبارات المكررة أو الرسمية الزائدة. "
                "استخدم وصلات محادثة ولمسات شخصية أو طرافة خفيفة عند الحاجة. لا تستخدم الكلمات المحظورة."
            )
        else:
            system_message = (
                f"{ALMASSA_INFO_EN}\n"
                "Always reply in natural, varied, conversational English. "
                "Keep responses under 6 lines. Avoid generic phrases and banned words. "
                "Use conversational connectors, personal touches, and occasional mild humor."
            )

        chat_completion = client.chat.completions.create(
    model="llama3-70b-8192",  # Correct model name!
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
