# 🚀 DEPLOY TO RENDER WITH POSTGRESQL

## ✅ Your Local PostgreSQL Works!

Database: ecoplan
Password: Pvbn@7738

---

## 🎯 Deploy Steps (5 minutes)

### 1️⃣ Create PostgreSQL on Render

1. Go to **https://render.com** dashboard
2. Click **"New +"** → **"PostgreSQL"**
3. Fill in:
   - Name: `ecoplan-db`
   - Database: `ecoplan`
   - User: `ecoplan_user`
   - Region: Same as web service
   - Instance Type: **Free**
4. Click **"Create Database"**
5. Wait 1 minute for creation

### 2️⃣ Get Database URL

1. Click on your PostgreSQL database
2. Copy **"Internal Database URL"**
   - Format: `postgresql://user:pass@host:port/dbname`

### 3️⃣ Update Web Service Environment

1. Go to your **web service** (ecoplan)
2. Click **"Environment"** tab
3. Add/Update these variables:

```
DATABASE_URL=<paste Internal Database URL from step 2>
GEOAPIFY_API_KEY=7c65c75f74714a81ba775f7102e0dbdb
OPENWEATHER_API_KEY=ee991cefa6ba7ab9b97b2ab62f1b4a92
```

4. Click **"Save Changes"**

### 4️⃣ Deploy

Render will auto-redeploy in 2-3 minutes.

---

## ✅ What Happens Automatically

1. App connects to PostgreSQL
2. Creates all tables automatically
3. Ready to use!

---

## 🔍 Check Logs

Go to web service → Logs → Look for:
```
[OK] Database tables initialized successfully
Running on http://0.0.0.0:10000
```

---

## 🎉 Done!

Your app will be live with persistent PostgreSQL!

Test at: `https://your-app.onrender.com`

---

**Everything on Render now! 🚀**
