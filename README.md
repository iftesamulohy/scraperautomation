# 🕷️ Web Scraping Automation Project

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Django-4.2+-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django" />
  <img src="https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL" />
  <img src="https://img.shields.io/badge/AWS-EC2-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white" alt="AWS" />
  <img src="https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white" alt="Nginx" />
</div>

<div align="center">
  <h3>🚀 Robust Web Scraping Automation with Django Integration</h3>
  <p>A production-ready web scraping solution designed for efficiency, scalability, and data integrity.</p>
</div>

---

## 📚 Table of Contents

- [🎬 Project Demo](#-project-demo)
- [📌 Project Overview](#-project-overview)
- [✨ Features](#-features)
- [🚀 Deploy on Your Local Machine](#-deploy-on-your-local-machine)
- [☁️ Deploy on AWS EC2 with Gunicorn and Nginx](#️-deploy-on-aws-ec2-with-gunicorn-and-nginx)
- [📁 Repository](#-repository)

---

## 🎬 Project Demo

[![Click to Watch the Project Overview on YouTube](https://img.youtube.com/vi/ppg-4cH4cac/0.jpg)](https://www.youtube.com/watch?v=ppg-4cH4cac)

🎬 **Watch the video overview**: [Click here to see how the project works in action »](https://www.youtube.com/watch?v=ppg-4cH4cac)

---

## 📌 Project Overview

This is a web scraping automation project designed to efficiently collect and process data from specific online sources. The scraper is built with robustness and scalability in mind, using modern Python libraries and Django integration to store and manage the collected data. The system also includes support for image downloading, file storage, duplicate detection, and scheduled scraping.

---

## ✨ Features

### 🔥 Core Functionality
- **Automated Data Collection** - Intelligent scraping with configurable targets
- **Django Integration** - Robust backend with ORM and admin interface
- **MySQL Database** - Reliable data storage with relationship management
- **Image Processing** - Automatic image downloading and optimization
- **Duplicate Detection** - Smart algorithms to prevent data redundancy

### 🎯 Advanced Capabilities
- **Scheduled Scraping** - Automated execution with cron job support
- **Error Handling** - Comprehensive error tracking and recovery
- **Rate Limiting** - Respectful scraping with customizable delays
- **Data Validation** - Built-in validation for data integrity
- **Logging System** - Detailed logs for monitoring and debugging

### 🛡️ Production Ready
- **Scalable Architecture** - Designed for high-volume data processing
- **Security Features** - Environment-based configuration and secure deployment
- **Monitoring Tools** - Performance tracking and health checks
- **Cloud Deployment** - AWS EC2 ready with Nginx and Gunicorn

---

## 🚀 Deploy on Your Local Machine

Follow the steps below to run the project locally.

### Prerequisites

Make sure you have the following installed:
- **Python 3.9+** - Latest Python version
- **MySQL** - Database server (via XAMPP or standalone)
- **Git** - Version control system

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

## ☁️ Deploy on AWS EC2 with Gunicorn and Nginx

Follow the steps below to deploy the project on an AWS EC2 instance.

### Prerequisites

- **AWS EC2 Instance** - Ubuntu 20.04 LTS or newer
- **Security Groups** - Allow HTTP (80), HTTPS (443), and SSH (22)
- **Domain Name** - Optional, but recommended for production

### Automated Deployment Script

```bash
#!/bin/bash

# Update and upgrade system
sudo apt update && sudo apt upgrade -y

# Install necessary packages
sudo apt install -y python3-pip python3-venv nginx git supervisor

# Clone project repo
cd /home/ubuntu || exit
git clone https://github.com/iftesamulohy/scraperautomation.git
cd scraperautomation || exit

# Create and activate virtual environment
python3 -m venv env
source env/bin/activate

# Upgrade pip and install gunicorn plus requirements
pip install --upgrade pip
pip install gunicorn
pip install -r requirements.txt

# NOTE: Create your .env file manually with proper credentials before continuing

# Run migrations and collect static files
python manage.py migrate
python manage.py collectstatic --noinput

# Create Gunicorn supervisor config
sudo tee /etc/supervisor/conf.d/gunicorn.conf > /dev/null <<EOF
[program:gunicorn]
directory=/home/ubuntu/scraperautomation
command=/home/ubuntu/env/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/scraperautomation/app.sock scraperautomation.wsgi:application
autostart=true
autorestart=true
user=ubuntu
stderr_logfile=/var/log/gunicorn/gunicorn.err.log
stdout_logfile=/var/log/gunicorn/gunicorn.out.log

[group:guni]
programs=gunicorn
EOF

# Reload and start supervisor service
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start gunicorn

# Setup Nginx site config
sudo tee /etc/nginx/sites-available/scraperautomation > /dev/null <<EOF
server {
    listen 80;
    server_name <your-ec2-public-ip-or-domain>;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/scraperautomation/app.sock;
    }
}
EOF

# Enable Nginx site and restart service
sudo ln -sf /etc/nginx/sites-available/scraperautomation /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Setup firewall rules
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw --force enable

echo "Deployment finished! Visit http://<your-ec2-public-ip>/"
```

### Manual Deployment Steps

1. **Launch EC2 Instance**
   - Choose Ubuntu 20.04 LTS AMI
   - Configure security groups for HTTP/HTTPS/SSH
   - Connect via SSH

2. **Run Deployment Script**
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

3. **Configure Environment Variables**
   ```bash
   nano .env
   # Add your production credentials
   ```

4. **SSL Certificate (Optional)**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

---

## 📁 Repository

GitHub Repo: [https://github.com/iftesamulohy/scraperautomation](https://github.com/iftesamulohy/scraperautomation)

---

<div align="center">
  <p>Made with ❤️ for efficient web scraping automation</p>
  <p>
    <a href="#-web-scraping-automation-project">Back to Top</a>
  </p>
</div>