# 🚀 Darshan's Portfolio

A personal portfolio website built with **Flask** and **MySQL**, deployed on **Render** with a cloud database on **Railway**.

---

## 🌐 Live Demo

[https://my1-portfolio-cmnx.onrender.com](https://my1-portfolio-cmnx.onrender.com)

---

## 📁 Project Structure

```
My_portfolio/
├── static/
│   ├── profile.jpg
│   └── style.css
├── templates/
│   ├── index.html
│   ├── about.html
│   ├── contact.html
│   ├── details.html
│   ├── login.html
│   └── work.html
├── app.py
├── requirements.txt
├── render.yaml
└── README.md
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | MySQL (Railway) |
| ORM | Flask-SQLAlchemy + PyMySQL |
| Auth | bcrypt password hashing |
| Hosting | Render (Web Service) |
| DB Host | Railway (MySQL) |

---

## ✨ Features

- Home, About, Work, and Contact pages
- Contact form that saves messages to MySQL database
- Admin login to view all submitted messages
- Protected inbox/details page (login required)
- Responsive design

---

## 🛠️ Local Setup

### 1. Clone the repo

```bash
git clone https://github.com/darshan320/My_portfolio.git
cd My_portfolio
```

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

```
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DATABASE=custermer_details
SECRET_KEY=your_secret_key
```

### 5. Set up local MySQL database

```sql
CREATE DATABASE custermer_details;

USE custermer_details;

CREATE TABLE Details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Full_name VARCHAR(200),
    Email VARCHAR(200),
    Subject VARCHAR(300),
    Message TEXT,
    Date DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 6. Run the app

```bash
python app.py
```

Visit `http://127.0.0.1:5000`

---

## 🚀 Deployment

### Render (Web Service)

Set these environment variables in Render dashboard:

| Key | Value |
|---|---|
| `MYSQL_HOST` | Railway public host |
| `MYSQL_PORT` | Railway public port |
| `MYSQL_USER` | Railway MySQL user |
| `MYSQL_PASSWORD` | Railway MySQL password |
| `MYSQL_DATABASE` | `railway` |
| `SECRET_KEY` | any random secret string |

### Railway (MySQL Database)

- Create a MySQL service on [railway.app](https://railway.app)
- Enable **Public Networking** in Settings to get the public host and port
- Run the `CREATE TABLE` SQL in the Database → Data tab

---

## 🔐 Admin Login

The details/inbox page is protected. Login at `/login` with the admin credentials set in `app.py`.

---

## 📦 Requirements

```
Flask==3.1.0
Flask-SQLAlchemy==3.1.1
PyMySQL==1.1.1
bcrypt==4.2.1
gunicorn==23.0.0
mysql-connector-python==8.3.0
python-dotenv==1.0.1
```

---

## 👨‍💻 Author

**Darshan S Linganagoudra**
Electronics & Communication Engineering (Advanced Communication Technology)

- GitHub: [github.com/darshan320](https://github.com/darshan320)
- LinkedIn: [linkedin.com/in/Darshan](https://www.linkedin.com/in/darshan-sadashivanagouda-linganagoudra-220367311/)
- Email: darshanlinganagoudra@gmail.com
