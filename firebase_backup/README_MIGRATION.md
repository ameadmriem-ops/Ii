# 📋 دليل إعداد وترحيل Firebase لمشروع MY MOVIE

تم أخذ نسخة احتياطية كاملة من جميع الملفات المرتبطة بـ Firebase في هذا المجلد (`firebase_backup/`).

---

## 1. قائمة الإعدادات القديمة التي يجب استبدالها بالمشروع الجديد

| الإعداد | القيمة القديمة (المشروع السابق) | مكان الملف |
| :--- | :--- | :--- |
| **Project ID** | `hamza-4b70c` | `strings.xml` + `index.html` |
| **Android App ID** | `1:595903053058:android:3745c8d9876284a4d4561b` | `strings.xml` |
| **Web App ID** | `1:595903053058:web:3745c8d9876284a4d4561b` | `index.html` |
| **API Key** | `AIzaSyB_9ZOotR4uZtYYn08OSIZXJczM-WC0MM8` | `strings.xml` + `index.html` |
| **Sender ID (Project Number)** | `595903053058` | `strings.xml` + `index.html` |
| **Auth Domain** | `hamza-4b70c.firebaseapp.com` | `index.html` |
| **Storage Bucket** | `hamza-4b70c.firebasestorage.app` | `index.html` |

---

## 2. هيكل البيانات في Cloud Firestore (مجموعة `movies`)
التطبيق يعتمد على مجموعة رئيسية واحدة باسم **`movies`** في Firestore.
كل وثيقة (Document) داخل المجموعة تمثل عملاً/فيلماً أو مسلسلاً وتحتوي على الحقول التالية:
* `title` (نص): اسم العمل أو الفيلم
* `poster` (نص): رابط صورة البوستر
* `episodes` (مصفوفة Array): قائمة الحلقات أو روابط البث:
  * `title`: اسم الحلقة أو السيرفر
  * `videoLink`: رابط الفيديو (M3U8 أو MP4 أو Pixeldrain)
  * `altUrl`: رابط الموقع البديل
  * `date`: تاريخ الإضافة
* `createdAt` (Timestamp): تاريخ إضافة العمل
* `category` (اختياري): تصنيف العمل

### قواعد أمان Firestore المطلوبة للمشروع الجديد (Firestore Rules):
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /movies/{movieId} {
      allow read: if true; // القراءة متاحة لجميع مستخدمي التطبيق
      allow write: if true; // أو تقييدها للمسؤولين حسب الرغبة
    }
  }
}
```

---

## 3. حمولة إشعارات FCM المدعومة بالتطبيق (Notification Payload)
عند إرسال إشعار عبر Firebase Cloud Messaging، يدعم التطبيق الحقول التالية في الـ Data Payload:
* `title`: عنوان الإشعار
* `message`: نص رسالة الإشعار
* `targetPage`: الصفحة المراد فتحها ("details" أو "home")
* `contentId`: معرّف الوثيقة في Firestore (`firebaseId`)
* `contentTitle`: اسم الفيلم للبحث عنه تلقائياً إذا لم يتوفر الـ ID
* `episodeNumber`: رقم الحلقة لتشغيلها مباشرة
* `action`: "play" (تشغيل فوري في ExoPlayer) أو "details" (فتح صفحة الحلقات)
* `imageUrl`: رابط صورة البوستر الكبير في الإشعار
* المواضيع المدعومة (Topics): `all_users` و `anime_updates`
