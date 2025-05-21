from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, jsonify, Response
from store import Post, PostStore
from supabase import create_client, Client
import os
from colorama import Fore, Style
from validate_email import validate_email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date
from werkzeug.utils import secure_filename
import uuid
app = Flask(__name__)
secret_key = os.urandom(24)
app.secret_key = secret_key
# تهيئة Supabase
passwordloca = "abdelaadime"
usernamelocal = "lahrour_1902"
url = 'https://biytrshphtxlywabygcc.supabase.co'
key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJpeXRyc2hwaHR4bHl3YWJ5Z2NjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0MTE5MjIwMiwiZXhwIjoyMDU2NzY4MjAyfQ.SpTXTAV_hylt0pFFEsofIT6aMdAZTcTPtxjauuV4vlA'
supabase: Client = create_client(url, key)
post_store = PostStore()
app.current_id = 2
# تحميل المنشورات من Supabase عند بدء التشغيل
def load_posts():
    try:
        response = supabase.table('lahrour').select('*').execute()
        posts = response.data
        for post in posts:
            new_post = Post(
                id=post['id'],
                public_url=post['public_url'],
                date=post['date'],
                body=post['body'],
               
                photo_url=post['photo_url'],
                page=post['page'],
                title=post['title']
            )
            post_store.add(new_post)
            app.current_id = max(app.current_id, new_post.id + 1)
    except Exception as e:
        print("Error loading posts:", e)
load_posts()

@app.route('/')
def home():
    posts = [post for post in post_store.get_all() if post.page == 'index']
    return render_template('index.html', posts=posts)

@app.route('/sw.js',methods=["GET","POST"])
def service_worker():
    from flask import make_response
    response = make_response(send_from_directory('.',path='sw.js'))
    response.headers['Content-Type'] = 'application/javascript'
    response.headers['Service-Worker-Allowed'] = '/'
    return response

@app.route("/message", methods=["POST"])
def subscribe():
    email = request.form.get("Email")
    if email:
        # حفظ البريد الإلكتروني في قاعدة البيانات
        data = {"email": email}
        response = supabase.table("emails").insert(data).execute()
        print(response.data)
    return redirect(request.referrer)  # إعادة المستخدم إلى الصفحة السابقة
@app.route('/sitemap.xml')
def sitemap():
    sitemap_ = '''
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
<!--  created with Free Online Sitemap Generator www.xml-sitemaps.com  -->
<url>
<loc>https://abou-talib.vercel.app/</loc>
<lastmod>2025-04-08T18:19:44+00:00</lastmod>
<priority>1.00</priority>
</url>
<url>
<loc>https://abou-talib.vercel.app/sport</loc>
<lastmod>2025-04-08T18:19:44+00:00</lastmod>
<priority>0.80</priority>
</url>
<url>
<loc>https://abou-talib.vercel.app/takafa</loc>
<lastmod>2025-04-08T18:19:44+00:00</lastmod>
<priority>0.80</priority>
</url>
<url>
<loc>https://abou-talib.vercel.app/arabec</loc>
<lastmod>2025-04-08T18:19:44+00:00</lastmod>
<priority>0.80</priority>
</url>
<url>
<loc>https://abou-talib.vercel.app/news</loc>
<lastmod>2025-04-08T18:19:44+00:00</lastmod>
<priority>0.80</priority>
</url>
<url>
<loc>https://abou-talib.vercel.app/login</loc>
<lastmod>2025-04-08T18:19:44+00:00</lastmod>
<priority>0.80</priority>
</url>
<url>
<loc>https://abou-talib.vercel.app/contact</loc>
<lastmod>2025-04-08T18:19:44+00:00</lastmod>
<priority>0.80</priority>
</url>
</urlset>
'''
    return Response(sitemap_, mimetype='application/xml')
@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, 'robots.txt')
@app.route('/takafa')
def takafa():
    posts = [post for post in post_store.get_all() if post.page == 'takafa']
    return render_template('takafa.html', posts=posts)
@app.route('/sport')
def sport():
    posts = [post for post in post_store.get_all() if post.page == 'sport']
    return render_template('index1.html', posts=posts)
@app.route('/news')
def news():
    posts = [post for post in post_store.get_all() if post.page == 'news']
    return render_template('news.html', posts=posts)
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    try:
        error = None
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            message = request.form['message']
            classe = request.form['class']
            # إعداد البريد الإلكتروني
            sender_email = "abdelaadime2@gmail.com"
            sender_password = "fyks ibwp lnbo mtvl"  # استبدلها بكلمة مرور البريد الإلكتروني
            recipient_email = "lahrour269@gmail.com"
            subject = "Contact Form Submission"
            body = f"""
            Name: {name}<br>
            Email: {email}<br>
            Class: {classe}<br>
            Message: {message}
            """
            # إرسال البريد الإلكتروني
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_email, msg.as_string())
            print("Email sent successfully!")
            print(Fore.YELLOW ,f"Name: {name}, Email: {email}, Message: {message}")  # تتبع البيانات المرسلة
            return redirect(request.referrer)  # إعادة المستخدم إلى الصفحة السابقة
    except Exception as e:
        print("Error during contact:", e)
    return render_template('contact.html', error=error)
@app.route('/arabec')
def arabec():
    posts = [post for post in post_store.get_all() if post.page == 'arabec']
    return render_template('arabec.html', posts=posts)
@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        error = None
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            print(f"Username: {username}, Password: {password}")  # تتبع اسم المستخدم وكلمة المرور
            if username == 'abdelaadime' and password =='lahrour_1902':
                session["logged_in"] = True
                return redirect(url_for("post_add"))
            else:
                error="اسم المستخدم أو كلمة المرور غير صحيحة"
    except Exception as e:
        print("Error during login:", e)
    return render_template("login.html", error=error)

@app.route('/post_add', methods=['GET', 'POST'])
def post_add():
    try:
        error = None
        print(f"Session logged_in: {session.get('logged_in')}")  # تتبع حالة الجلسة
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        public_url = None
        if request.method == "POST":
            file = request.files.get('image')
            if file:
                file.seek(0, os.SEEK_END)
                file_length = file.tell()
                print("file_length", file_length)
                file.seek(0, 0)
                if file_length > 500 * 1024:  # 500 كيلوبايت
                    error = "حجم الملف كبير جداً. يجب أن يكون أقل من 500 كيلوبايت."
                # تغيير اسم الملف إلى اسم فريد باستخدام uuid
                file_extension = os.path.splitext(file.filename)[1]
                new_filename = f"{uuid.uuid4()}{file_extension}"
                # تحميل الملف مباشرةإلى Supabase Storage
                file_content = file.read()
                upload_response = supabase.storage.from_("images").upload(new_filename, file_content)
                bucket_url = "https://biytrshphtxlywabygcc.supabase.co/storage/v1/object/public/images//"
                public_url = (bucket_url + new_filename)
            # إنشاء المنشور الجديد
            selected_page = request.form['page']
            new_post = Post(
                id=app.current_id,
                public_url=public_url,  # حفظ الرابط بدلاً من الملف نفسه
                photo_url=request.form['photo_url'],
                title=request.form['title'],
                body=request.form['body'],
                page=selected_page,
                date=date.today()  # تعيين التاريخ الحالي بدون الوقت
            )
            post_store.add(new_post)
            app.current_id += 1

            # حفظ البيانات في Supabase
            data = {
                "photo_url": new_post.photo_url,
                "title": new_post.title,
                "public_url": new_post.public_url,
                "body": new_post.body,
                "date": new_post.date.isoformat(),
                "page": new_post.page
            }
            supabase.table('lahrour').insert(data).execute()
            send_email(new_post.title)
            return redirect(url_for(selected_page))
    except Exception as e :
        print('ereur',e)
    return render_template('post-add.html',error=error)

def send_email(title):
    print(title)
    try:
        # جلب قائمة المستلمين من قاعدة البيانات
        response = supabase.table("emails").select("email").execute()
        recipients = [user["email"] for user in response.data if user["email"] and validate_email(user["email"])]
        print(f"Found {len(recipients)} valid recipients.")

        if not recipients:
            print("No valid recipients found.")
            return

        # إعداد البريد الإلكتروني
        sender_email = "abdelaadime2@gmail.com"
        sender_password = "fyks ibwp lnbo mtvl"  # كلمة المرور من متغيرات البيئة
        subject = f"New Post: {title}"
        body = f"""
        <h1>{title}</h1>
        <p>Check out our latest post on the website!</p>
        """

        # إعداد الرسالة
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['Subject'] = subject
        msg['Bcc'] = ", ".join(recipients)  # استخدام Bcc لإرسال جماعي
        msg.attach(MIMEText(body, 'html'))

        # الإرسال في اتصال واحد
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print(f"Emails sent successfully to {len(recipients)} recipients")

    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    except Exception as e:
        print(e)

if __name__ == '__main__':
    app.run()
