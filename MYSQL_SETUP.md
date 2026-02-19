# 🗄️ MYSQL SETUP - Railway.app (FREE)

## 🚀 Quick Setup

### 1️⃣ Create MySQL Database on Railway

1. Go to **https://railway.app**
2. Sign up with GitHub
3. Click **"New Project"** → **"Provision MySQL"**
4. Wait 30 seconds for database creation

### 2️⃣ Get Database Credentials

Click on MySQL service → **"Variables"** tab

Copy these values:
```
MYSQLHOST=containers-us-west-xxx.railway.app
MYSQLPORT=6379
MYSQLDATABASE=railway
MYSQLUSER=root
MYSQLPASSWORD=xxxxxxxxxxxxx
```

### 3️⃣ Add to Render Environment Variables

In Render dashboard, add these:

```
DB_HOST=containers-us-west-xxx.railway.app
DB_PORT=6379
DB_NAME=railway
DB_USER=root
DB_PASSWORD=xxxxxxxxxxxxx
```

### 4️⃣ Deploy

Your app will now use Railway MySQL instead of SQLite!

---

## ✅ Benefits

✅ **Persistent data** - Never resets
✅ **Free tier** - 500MB storage
✅ **Fast** - Optimized for production
✅ **Automatic backups**

---

## 🔗 Connection String Format

Railway provides a connection URL:
```
mysql://root:password@host:port/railway
```

Our app automatically uses environment variables, so just set them in Render!

---

## 📊 Test Connection

After deployment, check Render logs for:
```
[OK] Database 'railway' ready
[OK] Database tables initialized successfully
```

---

**That's it! Your app now has persistent MySQL storage.** 🎉
