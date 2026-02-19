# 🔍 VIEW DATABASE IN PGADMIN

## ✅ Data Added Successfully!

3 cities added to PostgreSQL:
- Chennai (ID: 1)
- Mumbai (ID: 2)
- Bangalore (ID: 3)

---

## 📊 Open pgAdmin and View Data

### 1️⃣ Open pgAdmin 4

### 2️⃣ Connect to Server

1. Right-click **"Servers"** → **"Register"** → **"Server"**
2. Fill in:

**General Tab:**
- Name: `Local PostgreSQL`

**Connection Tab:**
- Host: `localhost`
- Port: `5432`
- Database: `postgres`
- Username: `postgres`
- Password: `Pvbn@7738`
- Save password: ✓

3. Click **"Save"**

### 3️⃣ View EcoPlan Database

1. Expand: **Servers** → **Local PostgreSQL** → **Databases**
2. Find and expand: **ecoplan**
3. Expand: **Schemas** → **public** → **Tables**

You'll see 4 tables:
- ✅ **cities** (3 rows)
- ✅ **analysis_results** (0 rows)
- ✅ **simulations** (0 rows)
- ✅ **recommendations** (0 rows)

### 4️⃣ View City Data

1. Right-click **cities** table
2. Select **"View/Edit Data"** → **"All Rows"**
3. You'll see Chennai, Mumbai, Bangalore with all details!

---

## 🔍 Run SQL Queries

Click **"Query Tool"** and try:

```sql
-- View all cities
SELECT name, population, green_space_area, aqi FROM cities;

-- Count cities
SELECT COUNT(*) FROM cities;

-- Cities with high AQI
SELECT name, aqi FROM cities WHERE aqi > 100;
```

---

## 🚀 Run Flask App Locally

```bash
python app.py
```

Then go to: `http://localhost:5000`

- Add more cities via `/manual_input`
- View dashboard at `/dashboard`
- Check pgAdmin to see new data!

---

**Your PostgreSQL is working perfectly! 🎉**
