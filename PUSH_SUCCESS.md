# ✅ CODE PUSHED TO GITHUB!

Your repo: **https://github.com/Niranjanprakash/Eco_system**

---

## 🚀 DEPLOY NOW (2 Steps)

### Step 1: Setup MySQL on Railway (2 min)

1. Go to **https://railway.app**
2. Sign up with GitHub
3. Click **"New Project"** → **"Provision MySQL"**
4. Click MySQL service → **"Variables"** tab
5. Copy these values:

```
MYSQLHOST=containers-us-west-xxx.railway.app
MYSQLPORT=6379
MYSQLDATABASE=railway
MYSQLUSER=root
MYSQLPASSWORD=xxxxxxxxxxxxx
```

---

### Step 2: Deploy on Render (5 min)

1. Go to **https://render.com**
2. Sign up with GitHub
3. Click **"New +"** → **"Web Service"**
4. Select repo: **Niranjanprakash/Eco_system**
5. Fill settings:

```
Name: ecoplan
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app --bind 0.0.0.0:$PORT
```

6. Click **"Advanced"** → Add Environment Variables:

```
DB_HOST=<from railway MYSQLHOST>
DB_PORT=<from railway MYSQLPORT>
DB_NAME=railway
DB_USER=root
DB_PASSWORD=<from railway MYSQLPASSWORD>
GEOAPIFY_API_KEY=7c65c75f74714a81ba775f7102e0dbdb
OPENWEATHER_API_KEY=ee991cefa6ba7ab9b97b2ab62f1b4a92
FLASK_ENV=production
```

7. Click **"Create Web Service"**

---

## 🎉 DONE!

Your app will be live at:
```
https://ecoplan.onrender.com
```

With persistent MySQL from Railway! 🗄️

---

## ⏱️ Time: ~7 minutes total

- Railway MySQL: 2 min
- Render deploy: 5 min

**Go deploy now! 🚀**
