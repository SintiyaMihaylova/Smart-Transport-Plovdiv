# 🚌 Smart Transport Plovdiv

**Smart Transport Plovdiv** is a Django-based web platform designed to modernize and streamline public transportation management in Plovdiv, Bulgaria. The system bridge the gap between citizens and city operators by providing real-time data and a robust reporting mechanism.

![Django](https://img.shields.io/badge/django-%23092e20.svg?style=for-the-badge&logo=django&logoColor=white)
![Bootstrap](https://img.shields.io/badge/bootstrap-%23563d7c.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

---

## ✨ Key Features

### 👥 For Citizens (Users)
* **Route Navigation:** Browse all active bus lines and their respective schedules.
* **Station Directory:** Find detailed information and locations of bus stops across the city.
* **Issue Reporting:** Submit reports regarding delays, vehicle conditions, or infrastructure problems.
* **Multilingual Support:** Full interface availability in both **Bulgarian** and **English**.
* **Personal Dashboard:** Manage profile settings and track the status of submitted reports.

### 🛠️ For Administrators & Operators
* **Management Dashboard:** A centralized hub for processing citizen reports.
* **Line & Station CRUD:** Full control to Create, Read, Update, and Delete transport data.
* **Status Tracking:** Update report statuses (e.g., *New*, *In Progress*, *Resolved*) with admin comments.
* **Advanced Filtering:** Powerful search and filter tools for managing large datasets.

---

## 🚀 Tech Stack

* **Backend:** [Django 6.0](https://www.djangoproject.com/)
* **Frontend:** [Bootstrap 5](https://getbootstrap.com/), FontAwesome, Bootstrap Icons
* **Database:** SQLite (Development) / PostgreSQL (Production ready)
* **Authentication:** Custom User Model (Email-based)
* **Internationalization:** Django i18n framework

---

## 🛠️ Installation & Setup

Run the following commands in your terminal:

```bash
# Clone the repository
git clone https://github.com/SintiyaMihaylova/Plovdiv-Transport-System.git
cd Plovdiv-Transport-System

# Install dependencies
pip install -r requirements.txt

# Apply migrations (initial data will be loaded automatically)
python manage.py migrate

# Compile translations
python manage.py compilemessages

# Start the server
python manage.py runserver
```