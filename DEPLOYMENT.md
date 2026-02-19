# 🚀 DEPLOYMENT GUIDE - Render.com

## ✅ Your Project is Ready!

Your Flask app structure is **perfect** for Render deployment.

---

## 📦 Files Created for Deployment

✅ **Procfile** - Tells Render how to start your app
✅ **runtime.txt** - Specifies Python version
✅ **requirements.txt** - Updated with gunicorn

---

## 🔥 DEPLOY TO RENDER.COM (Step-by-Step)

### Step 1: Push to GitHub

```bash
cd eco-system
git init
git add .
git commit -m "Ready for deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/eco-system.git
git push -u origin main
```

### Step 2: Deploy on Render

1. Go to **https://render.com**
2. Sign up/Login (use GitHub)
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub repo: `eco-system`
5. Fill in these settings:

```
Name: ecoplan-app
Region: Singapore (or closest to you)
Branch: main
Root Directory: (leave blank)
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app --bind 0.0.0.0:$PORT
Instance Type: Free
```

6. Click **"Advanced"** → Add Environment Variables:

```
GEOAPIFY_API_KEY = 7c65c75f74714a81ba775f7102e0dbdb
OPENWEATHER_API_KEY = ee991cefa6ba7ab9b97b2ab62f1b4a92
FLASK_ENV = production
```

7. Click **"Create Web Service"**

### Step 3: Wait for Deployment

- First deploy takes 5-10 minutes
- Watch the logs for any errors
- Once done, you'll get a live URL like:

```
https://ecoplan-app.onrender.com
```

---

## ⚠️ IMPORTANT NOTES

### Database (SQLite)

Your app uses `data/ecoplan.db` (SQLite).

**On Render Free Tier:**
- ✅ Works fine
- ⚠️ Data resets on server restart (every ~15 mins of inactivity)

**For Persistent Data:**
- Upgrade to Render Paid ($7/month) - keeps disk storage
- OR use external MySQL/PostgreSQL (Railway, PlanetScale)

### File Uploads

Your `data/uploads/` folder will also reset on free tier.

**Solution:**
- Use cloud storage (AWS S3, Cloudinary) for production
- For demo/hackathon, free tier is fine

---

## 🧪 Test Your Deployment

After deployment, test these URLs:

```
https://your-app.onrender.com/
https://your-app.onrender.com/upload
https://your-app.onrender.com/manual_input
https://your-app.onrender.com/dashboard
```

---

## 🐛 Troubleshooting

### Build Fails?

Check if `requirements.txt` has all dependencies:
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push
```

### App Crashes?

Check Render logs:
- Go to your service dashboard
- Click "Logs" tab
- Look for Python errors

### Port Issues?

Make sure `app.py` uses:
```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

---

## 🎯 ALTERNATIVE DEPLOYMENT OPTIONS

### Option 1: Railway.app
- Similar to Render
- Better free tier database
- Deploy: https://railway.app

### Option 2: PythonAnywhere
- Free tier with persistent storage
- Deploy: https://www.pythonanywhere.com

### Option 3: Heroku
- Classic choice (no longer free)
- Deploy: https://heroku.com

---

## 📊 What Works on Free Tier

✅ Full Flask app
✅ All templates/routes
✅ ML model predictions
✅ API integrations
✅ Dashboard visualizations
✅ File uploads (temporary)
✅ SQLite database (temporary)

---

## 🚀 QUICK DEPLOY CHECKLIST

- [ ] Push code to GitHub
- [ ] Create Render account
- [ ] Connect GitHub repo
- [ ] Set environment variables
- [ ] Deploy and wait
- [ ] Test live URL
- [ ] Share with team! 🎉

---

## 💡 PRO TIPS

1. **First deploy is slow** - Be patient
2. **Free tier sleeps** - First request takes 30s to wake up
3. **Use sample data** - Pre-load Tamil Nadu cities for demo
4. **Monitor logs** - Check for errors during demo
5. **Have backup** - Keep local version running just in case

---

## 📞 Need Help?

If deployment fails, check:
1. Render logs (most important)
2. GitHub repo structure
3. Environment variables
4. Python version compatibility

---

**Your app is deployment-ready! 🎉**

Just push to GitHub and deploy on Render.com.

Good luck with your hackathon! 🚀
