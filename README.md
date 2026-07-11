# TrekOra – Trekking Management System

TrekOra is a role-based Trekking Management System developed as part of the IIT Madras BS Degree Modern Application Development I project.

## Features

- User Registration and Login
- Role-based Access Control (Admin, Staff, User)
- Trek Management
- Trek Booking System
- Staff Assignment
- Booking History
- Trek Reviews and Ratings
- Search Functionality
- REST-style JSON APIs
- Responsive User Interface using Bootstrap 5

---

## Technologies Used

- Python
- Flask
- SQLAlchemy
- SQLite
- Jinja2
- HTML5
- CSS3
- Bootstrap 5

---

## Project Structure

```
TrekOra/
│
├── app.py
├── config.py
├── init_db.py
├── models.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── routes/
│   ├── auth.py
│   ├── admin.py
│   ├── staff.py
│   ├── user.py
│   └── api.py
│
├── templates/
│   ├── admin/
│   ├── staff/
│   ├── user/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   └── register.html
│
└── static/
    └── css/
        └── style.css
```

---

## Installation

Clone the repository

```bash
git clone <repository-url>
```

Install the required packages

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

The application will start at:

```
http://127.0.0.1:5000
```

---

## REST APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/treks` | GET | Retrieve all treks |
| `/api/treks/<id>` | GET | Retrieve trek details |
| `/api/users` | GET | Retrieve all users |
| `/api/bookings` | GET | Retrieve all bookings |
| `/api/treks` | POST | Create a new trek |
| `/api/treks/<id>` | PUT | Update an existing trek |
| `/api/treks/<id>` | DELETE | Delete a trek |

All API responses are returned in **JSON** format using Flask's `jsonify()`.

---

## Author

**Sutapa Naskar**

IIT Madras BS Degree Programme

Modern Application Development I Project