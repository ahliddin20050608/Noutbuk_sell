# 🤖 Botni Doimiy Ishga Tushirish Ko'rsatmasi

## 📋 Variant 1: Windows Task Scheduler (Tavsiya etiladi)

### Qadam 1: Task Scheduler ni ochish
1. Windows + R tugmalarini bosing
2. `taskschd.msc` yozing va Enter bosing

### Qadam 2: Yangi vazifa yaratish
1. O'ng tomonda "Create Basic Task" ni bosing
2. Name: `Telegram Bot`
3. Description: `Telegram botni doimiy ishlab turishi uchun`
4. Next > bosing

### Qadam 3: Trigger sozlash
1. "When the computer starts" ni tanlang
2. Next > bosing

### Qadam 4: Action sozlash
1. "Start a program" ni tanlang
2. Next > bosing
3. Program/script: `C:\Users\Asus\Desktop\BOT_TELEGRAM\start_bot_forever.bat`
   (yoki o'z papkangizga moslashtiring)
4. Start in: `C:\Users\Asus\Desktop\BOT_TELEGRAM`
5. Finish bosing

### Qadam 4: Qo'shimcha sozlamalar
1. Task Scheduler da yaratilgan vazifani o'ng tugma bilan bosing
2. "Properties" ni tanlang
3. "General" tabida:
   - ✅ "Run whether user is logged on or not" belgilang
   - ✅ "Run with highest privileges" belgilang
4. "Settings" tabida:
   - ✅ "Allow task to be run on demand" belgilang
   - ✅ "Run task as soon as possible after a scheduled start is missed" belgilang
   - ✅ "If the task fails, restart every:" belgilang va 1 daqiqa qo'ying
   - "Attempt to restart up to:" 3 marta
5. OK bosing

---

## 📋 Variant 2: NSSM (Windows Service sifatida)

### Qadam 1: NSSM ni yuklab olish
1. https://nssm.cc/download saytidan NSSM ni yuklab oling
2. Zip faylni ochib, `nssm.exe` ni `C:\Windows\System32\` ga ko'chiring

### Qadam 2: Service yaratish
PowerShell ni Administrator sifatida ochib quyidagi buyruqlarni bajaring:

```powershell
cd C:\Users\Asus\Desktop\BOT_TELEGRAM

nssm install TelegramBot "C:\Users\Asus\Desktop\BOT_TELEGRAM\env\Scripts\python.exe" "C:\Users\Asus\Desktop\BOT_TELEGRAM\main.py"

nssm set TelegramBot AppDirectory "C:\Users\Asus\Desktop\BOT_TELEGRAM"

nssm set TelegramBot Description "Telegram Bot Service"

nssm set TelegramBot Start SERVICE_AUTO_START

nssm start TelegramBot
```

### Service ni boshqarish:
```powershell
nssm start TelegramBot      # Ishga tushirish
nssm stop TelegramBot       # To'xtatish
nssm restart TelegramBot    # Qayta ishga tushirish
nssm remove TelegramBot      # O'chirish
```

---

## 📋 Variant 3: PM2 (Process Manager)

### Qadam 1: PM2 ni o'rnatish
```bash
npm install -g pm2
```

### Qadam 2: PM2 da botni ishga tushirish
```bash
cd C:\Users\Asus\Desktop\BOT_TELEGRAM
pm2 start main.py --name telegram-bot --interpreter env\Scripts\python.exe
pm2 save
pm2 startup
```

### PM2 buyruqlari:
```bash
pm2 list              # Barcha processlarni ko'rish
pm2 logs telegram-bot # Loglarni ko'rish
pm2 restart telegram-bot # Qayta ishga tushirish
pm2 stop telegram-bot    # To'xtatish
pm2 delete telegram-bot  # O'chirish
```

---

## 📋 Variant 4: Oddiy Batch Script (Test uchun)

1. `start_bot_forever.bat` faylini ikki marta bosib ishga tushiring
2. Bot doimiy ishlab turadi
3. Kompyuter qayta ishga tushganda avtomatik ishga tushmaydi (Task Scheduler kerak)

---

## ⚠️ Muhim Eslatmalar

1. **.env fayl**: `.env` faylida `TOKEN` bo'lishi kerak
2. **Virtual Environment**: `env` papkasi mavjud bo'lishi kerak
3. **Python**: Python 3.8+ o'rnatilgan bo'lishi kerak
4. **wkhtmltopdf**: PDF yaratish uchun `C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe` o'rnatilgan bo'lishi kerak

---

## 🔍 Botni Tekshirish

Bot ishlab turganini tekshirish uchun:
1. Telegram da botga xabar yuboring
2. Javob kelsa, bot ishlayapti ✅
3. Javob kelmasa, loglarni tekshiring

---

## 📝 Loglar

Agar bot xatolik bilan to'xtasa:
- `start_bot_forever.bat` faylida xatoliklar ko'rinadi
- PM2 ishlatilsa: `pm2 logs telegram-bot`
- Task Scheduler da "History" tabida xatoliklarni ko'rish mumkin

---

## 🚀 Eng Yaxshi Variant

**Windows uchun eng yaxshi variant: Windows Task Scheduler**
- Oson sozlash
- Kompyuter qayta ishga tushganda avtomatik ishga tushadi
- Xatolik bo'lsa avtomatik qayta ishga tushadi
- Qo'shimcha dastur o'rnatish shart emas

