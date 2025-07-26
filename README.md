# 🛒 Grocery Store - E-commerce Full Stack Project

This is a full-stack grocery store website built using **Django (Python)** on the backend and **HTML, CSS, JavaScript, Bootstrap** on the frontend.

## 🚀 Features

- 🧑‍💼 User Registration and Login (Authentication)
- 🛍️ Product Listing by Categories
- 🛒 Add to Cart / Remove from Cart
- 📦 Checkout Page
- 📊 Admin Panel for Inventory Management
- 💳 (Optional) Payment Gateway Integration
- 📱 Responsive Design (Mobile-friendly)

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS, JavaScript, Bootstrap  
- **Backend**: Python, Django  
- **Database**: SQLite (or PostgreSQL)  
- **Tools**: Django Admin Panel, Django ORM  

## 📁 Project Structure

GroceryStore/
│
├── manage.py
├── GroceryApp/ # Django App
│ ├── models.py # DB models
│ ├── views.py # Business logic
│ ├── urls.py # Routes
│ ├── templates/ # HTML pages
│ └── static/ # CSS/JS files
├── MYSql DataBase# MySQL DATABASE

**Clone the repo**

  git clone https://github.com/your-username/your-grocery-repo.git
  cd GroceryStore
  python -m venv venv
  venv\Scripts\activate      # On Windows
  
  pip install -r requirements.txt
  python manage.py makemigrations
  python manage.py migrate
  python manage.py runserver
  
  Open browser: http://127.0.0.1:8000/
  
  📌 Admin Panel
  python manage.py createsuperuser
