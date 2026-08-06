# 🎉 Event Management System

A web-based **Event Management System** built using the **Django Framework** that simplifies event organization, registration, and attendee management. The application provides separate dashboards for administrators and users, making event management efficient and user-friendly.

---

## 📖 Overview

The Event Management System (EMS) is designed to provide a centralized platform where organizers can create and manage events while users can browse, register, and manage their event tickets. The project follows Django's **Model-View-Template (MVT)** architecture for a clean, scalable, and maintainable codebase.

---

## ✨ Features

### 👨‍💼 Admin
- Dashboard with event statistics
- Create, update, and delete events
- Manage attendees
- Configure ticket types and pricing
- Track registrations

### 👤 User
- Browse available events
- Register for events
- View registered events
- Manage tickets
- Personal dashboard

---

## 🛠 Tech Stack

| Technology | Description |
|------------|-------------|
| **Backend** | Django (Python) |
| **Frontend** | HTML5, CSS3, JavaScript, Bootstrap |
| **Database** | MySQL |
| **Authentication** | Django Authentication System |

---

## 🏗 System Architecture

The application follows Django's **MVT (Model-View-Template)** architecture.

- **Models** – Define database tables and relationships.
- **Views** – Handle application logic and user requests.
- **Templates** – Render dynamic web pages using HTML and Bootstrap.

---

## 📂 Project Structure

```
EventManagementSystem/
│── event_management/
│── events/
│── users/
│── templates/
│── static/
│── media/
│── manage.py
│── requirements.txt
└── README.md
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/event-management-system.git
cd event-management-system
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database

Update your MySQL database settings inside:

```
settings.py
```

Then run:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser

```bash
python manage.py createsuperuser
```

### 6. Start the Development Server

```bash
python manage.py runserver
```

Open your browser and visit:

```
http://127.0.0.1:8000/
```

---

## 📸 Screenshots

| Home | Dashboard |
|------|-----------|
| Add Screenshot | Add Screenshot |

| Event Details | Registration |
|--------------|--------------|
| Add Screenshot | Add Screenshot |

---

## 🔐 Security Features

- Django Authentication
- Role-Based Access Control
- Password Hashing
- CSRF Protection
- Input Validation
- Secure Authorization

---

## 🌟 Future Enhancements

- 💳 Payment Gateway Integration
- 📧 Email Notifications
- 🎟 QR Code Tickets
- 📊 Event Analytics
- ⭐ Reviews & Ratings
- 📅 Calendar Integration
- 🔔 Push Notifications
- 📱 Social Media Integration

---

## 🎯 Objectives

- Centralized event management platform
- Easy event registration process
- Efficient attendee tracking
- Secure ticket management
- Responsive user interface

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Add new feature"
```

4. Push to your branch

```bash
git push origin feature-name
```

5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Rachit Sinha**

- GitHub: https://github.com/CodedBankai
- LinkedIn: https://www.linkedin.com/in/rachit-sinha-a859b6357
