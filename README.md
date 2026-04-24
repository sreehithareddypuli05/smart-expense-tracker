💰 ExpenseIQ — Smart Expense Tracker
live-https://smart-expense-tracker-7.onrender.com/

https://smart-expense-tracker-7.onrender.com/create-admin/ creates admin
with username:admin 

password:admin123

(u can see the user details in your admin portal)

A simple and secure web app to track your daily expenses, built with Django + Bootstrap.

✨ Features

🔐 User Signup, Login & Logout

💸 Add, edit, delete expenses

📊 Dashboard with total spending & charts

🏷️ Category-based tracking & filtering

📱 Responsive design (mobile + desktop)

🌙 Clean dark-themed UI

🛠️ Tech Stack

Backend: Django (Python)

Frontend: HTML, CSS, Bootstrap, JS

Database: SQLite (dev) / PostgreSQL (prod)

Deployment: Render

🚀 Run Locally

git clone this-repo

cd smart-expense-tracker

python -m venv venv

source venv/bin/activate   # or venv\Scripts\activate (Windows)

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver

python manage.py createsuperuser(for creating admin)

Open: http://127.0.0.1:8000

🌐 Deployment

Push code to GitHub

Connect repo to Render

Add environment variables

Deploy 🚀

🔒 Security

Passwords are securely hashed

Only logged-in users can access data

Each user sees only their own expenses
❤️

Built using Django for a full-stack internship project.
