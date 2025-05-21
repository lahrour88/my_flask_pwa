# تطبيق Flask

هذا مشروع تطبيق ويب مبني باستخدام إطار عمل Flask.

## الرسم التخطيطي للمشروع

يمكنك مشاهدة الرسم التخطيطي للمشروع من خلال [GitDiagram](https://gitdiagram.com/)

## المتطلبات

- Python 3.x
- Flask
- SQLAlchemy
- Flask-Login
- Flask-WTF

## التثبيت

1. قم بتثبيت المتطلبات باستخدام pip:
```bash
pip install -r requirements.txt
```

2. قم بتشغيل التطبيق:
```bash
python app.py
```

## الميزات

- نظام تسجيل الدخول وإدارة المستخدمين
- واجهة مستخدم سهلة الاستخدام
- قاعدة بيانات SQLite للتخزين
- نماذج تفاعلية باستخدام Flask-WTF

## هيكل المشروع

```
flask-app/
├── app.py
├── requirements.txt
├── static/
│   └── css/
│       └── style.css
└── templates/
    ├── base.html
    ├── index.html
    └── login.html
```

## المساهمة

نرحب بمساهماتكم! يرجى اتباع الخطوات التالية:

1. قم بعمل Fork للمشروع
2. قم بإنشاء فرع جديد (`git checkout -b feature/amazing-feature`)
3. قم بعمل Commit للتغييرات (`git commit -m 'إضافة ميزة جديدة'`)
4. قم بعمل Push للفرع (`git push origin feature/amazing-feature`)
5. قم بفتح طلب Pull Request

## الترخيص

هذا المشروع مرخص تحت رخصة MIT. 