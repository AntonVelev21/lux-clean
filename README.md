# 🧼✨ LuxClean

A web platform for a professional cleaning business, built with **Django**, **Tailwind CSS** and **PostgreSQL**.

> 🚧 **Work in progress**: this project is currently under active development. 🚧

![Status](https://img.shields.io/badge/status-in%20development-orange?style=flat-square)
![Python](https://img.shields.io/badge/python-3.11-blue?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/django-%23092E20?style=flat-square&logo=django&logoColor=white)
![Tailwind](https://img.shields.io/badge/tailwind-%2338B2AC?style=flat-square&logo=tailwindcss&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/postgresql-%23316192?style=flat-square&logo=postgresql&logoColor=white)

## 🧱 Project structure
| `core` | Shared logic and base functionality |
| `web` | Public pages |
| `services` | Cleaning services offered |
| `orders` | Order creation logic |
| `users` | Accounts and authentication |


## 🛠️ Technologies used
| **Language** | Python |
| **Backend** | Django |
| **Database** | PostgreSQL |
| **Frontend** | Tailwind CSS, Django Templates |
| **Tooling** | Node.js / npm (Tailwind build), Git |
| **Dev environment** | PyCharm, virtualenv (`.venv`) |


## 🚀 Getting started

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt
npm install

# 3. Configure environment variables
copy .env.example .env

# 4. Apply migrations and run
python manage.py migrate
python manage.py runserver
```

## 👤 Author

**Anton Velev**: [LinkedIn](https://www.linkedin.com/in/anton-velev-python/)
