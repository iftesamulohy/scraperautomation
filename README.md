# 🕷️ Web Scraping Automation Project

## 📚 Table of Contents

- [Deploy on Your Local Machine](#-deploy-on-your-local-machine)


[![Click to Watch the Project Overview on YouTube](https://img.youtube.com/vi/ppg-4cH4cac/0.jpg)](https://www.youtube.com/watch?v=ppg-4cH4cac)

🎬 **Watch the video overview**: [Click here to see how the project works in action »](https://www.youtube.com/watch?v=ppg-4cH4cac)

---

## 📌 Project Overview

This is a web scraping automation project designed to efficiently collect and process data from specific online sources. The scraper is built with robustness and scalability in mind, using modern Python libraries and Django integration to store and manage the collected data. The system also includes support for image downloading, file storage, duplicate detection, and scheduled scraping.

---

## 🚀 Deploy on Your Local Machine

Follow the steps below to run the project locally.

### 1. 🔁 Clone the Repository

```bash
git clone https://github.com/iftesamulohy/scraperautomation.git
cd scraperautomation
```

### 2. 🐍 Create a Virtual Environment

```bash
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
```

### 3. 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. ⚙️ Set Environment Variables

Create a `.env` file in the root directory and add your database credentials:

```env
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=127.0.0.1
DB_PORT=3306
SECRET_KEY=your_django_secret_key
DEBUG=True
```

> ☑️ Make sure `.env` is listed in `.gitignore`.

### 5. 🛠 Set Up MySQL Using XAMPP

- Start **Apache** and **MySQL** via the XAMPP Control Panel.
- Open [http://localhost/phpmyadmin](http://localhost/phpmyadmin)
- Create a new database with the name you set in `.env`.

### 6. 🔨 Run Migrations

```bash
python manage.py migrate
```

### 7. 📥 Load Initial Data

```bash
python manage.py loaddata data.json
```

### 8. 🚦 Start the Server

```bash
python manage.py runserver
```

Now open your browser and visit:  
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📁 Repository

GitHub Repo: [https://github.com/iftesamulohy/scraperautomation](https://github.com/iftesamulohy/scraperautomation)

---
