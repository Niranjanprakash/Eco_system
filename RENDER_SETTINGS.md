# 🎯 RENDER.COM DEPLOYMENT - QUICK REFERENCE

## Copy-Paste These Settings

### Build Command
```
pip install -r requirements.txt
```

### Start Command
```
gunicorn app:app --bind 0.0.0.0:$PORT
```

### Environment Variables
```
GEOAPIFY_API_KEY=7c65c75f74714a81ba775f7102e0dbdb
OPENWEATHER_API_KEY=ee991cefa6ba7ab9b97b2ab62f1b4a92
FLASK_ENV=production
```

### Instance Type
```
Free
```

### Python Version
```
3.11.0
```

---

## Your Live URL Will Be
```
https://ecoplan-app.onrender.com
```
(or whatever name you choose)

---

## Files Already Created ✅
- ✅ Procfile
- ✅ runtime.txt
- ✅ requirements.txt (with gunicorn)
- ✅ app.py (PORT configured)

---

## Next Step
**Push to GitHub and deploy!** 🚀
