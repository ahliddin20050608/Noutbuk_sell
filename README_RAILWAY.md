# 🚂 Railway ga Deploy Qilish Ko'rsatmasi

## 📋 Qadam 1: Railway Account yaratish

1. https://railway.app saytiga kiring
2. "Start a New Project" tugmasini bosing
3. GitHub yoki Email orqali ro'yxatdan o'ting

---

## 📋 Qadam 2: Yangi Project yaratish

1. Railway dashboard da "New Project" tugmasini bosing
2. "Deploy from GitHub repo" ni tanlang (yoki "Empty Project")
3. Agar GitHub dan deploy qilsangiz:
   - GitHub repository ni tanlang
   - "Deploy Now" tugmasini bosing

---

## 📋 Qadam 3: Environment Variables sozlash

1. Project dashboard da "Variables" tabiga o'ting
2. Quyidagi variable ni qo'shing:

```
TOKEN=your_telegram_bot_token_here
```

**Muhim:** `your_telegram_bot_token_here` o'rniga o'z bot tokeningizni yozing!

---

## 📋 Qadam 4: Settings sozlash

1. Project dashboard da "Settings" tabiga o'ting
2. "Root Directory" bo'sh qoldiring (yoki `/` qo'ying)
3. "Build Command" bo'sh qoldiring (Railway avtomatik aniqlaydi)
4. "Start Command": `python main.py`

---

## 📋 Qadam 5: Deploy

1. Railway avtomatik deploy qiladi
2. "Deployments" tabida deploy jarayonini kuzatishingiz mumkin
3. Muvaffaqiyatli deploy bo'lgandan keyin bot ishga tushadi

---

## ⚠️ Muhim Eslatmalar

### 1. PDF yaratish (wkhtmltopdf)

Railway da `wkhtmltopdf` o'rnatish qiyin. Agar PDF yaratish kerak bo'lsa:

**Variant 1:** PDF yaratishni o'chirib tashlang yoki alternativ ishlating

**Variant 2:** Railway da buildpack qo'shing (qiyin)

**Variant 3:** PDF yaratishni boshqa servisga ko'chiring (masalan, Cloudinary, AWS Lambda)

### 2. Database

- SQLite Railway da ishlaydi, lekin har safar restart bo'lganda ma'lumotlar yo'qolishi mumkin
- Production uchun PostgreSQL yoki boshqa cloud database ishlatish tavsiya etiladi

### 3. Images

- `images/` papkasidagi rasmlar Railway ga yuklanadi
- Lekin katta fayllar uchun Cloud Storage (S3, Cloudinary) ishlatish yaxshi

---

## 🔍 Deploy ni Tekshirish

1. Railway dashboard da "Deployments" tabiga o'ting
2. Eng so'nggi deployment ni tanlang
3. "Logs" tugmasini bosing
4. Quyidagi xabarni ko'rish kerak:
   ```
   BOT ISHGA TUSHDI...
   ```

---

## 🐛 Xatoliklarni Tuzatish

### Xatolik: "TOKEN not found"
- Environment Variables da `TOKEN` qo'shilganligini tekshiring
- Variable nomi katta harf bilan `TOKEN` bo'lishi kerak

### Xatolik: "Module not found"
- `requirements.txt` da barcha kutubxonalar borligini tekshiring
- Railway avtomatik `pip install -r requirements.txt` ni bajaradi

### Xatolik: "PDF generation failed"
- PDF yaratish funksiyalarini vaqtincha o'chirib tashlang
- Yoki alternativ yechim ishlating

---

## 📝 Railway CLI (Ixtiyoriy)

Agar Railway CLI ishlatmoqchi bo'lsangiz:

```bash
# Railway CLI o'rnatish
npm i -g @railway/cli

# Login qilish
railway login

# Project ga ulanish
railway link

# Environment variable qo'shish
railway variables set TOKEN=your_token_here

# Deploy
railway up
```

---

## 🚀 Production uchun Tavsiyalar

1. **Database:** PostgreSQL yoki MySQL ishlating (SQLite o'rniga)
2. **Logging:** Railway da logs avtomatik saqlanadi
3. **Monitoring:** Railway dashboard da metrics ko'rish mumkin
4. **Backup:** Database ni muntazam backup qiling
5. **Environment Variables:** Barcha maxfiy ma'lumotlarni environment variables da saqlang

---

## 📞 Yordam

Agar muammo bo'lsa:
1. Railway dashboard da "Logs" ni tekshiring
2. GitHub Issues da muammo yozing
3. Railway Discord serveriga murojaat qiling

---

## ✅ Muvaffaqiyatli Deploy!

Agar barcha qadamlarni to'g'ri bajarsangiz, bot Railway da ishlab turadi va 24/7 mavjud bo'ladi!

