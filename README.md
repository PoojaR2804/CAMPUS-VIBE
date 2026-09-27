# 🎓 CampusVibe – College Event Management System

## 📌 About the Project

**CampusVibe** is a web-based College Event Management System designed to make college event management simple and organized.

It allows students to create an account, log in, explore college events, and register for events online. The system helps students stay updated about campus activities and makes event registration easier.

This project was developed to provide a simple and user-friendly platform for managing college events.

## 🎯 Objectives

* To provide a single platform for college event information.
* To make event registration easy for students.
* To reduce manual work in managing event registrations.
* To store student and event details securely.
* To improve communication about campus activities.

## ✨ Features

* **Student Signup:** Students can create an account using their name, email, register number, department, and password.
* **Student Login:** Registered students can log in securely.
* **Event Management:** Students can explore available college events.
* **Online Event Registration:** Students can register for events through the website.
* **Database Integration:** Student and event details are stored in MongoDB.
* **User-Friendly Interface:** Simple and responsive design.
* **Logout:** Students can securely log out of their accounts.

## 🛠️ Technologies Used

| Technology    | Purpose                                 |
| ------------- | --------------------------------------- |
| HTML          | Structure of the website                |
| CSS           | Website styling and design              |
| JavaScript    | Interactive features                    |
| Python        | Backend programming                     |
| Flask         | Web application framework               |
| MongoDB Atlas | Cloud database                          |
| GitHub        | Version control and source code hosting |
| Render        | Website deployment                      |

## 🏗️ Project Structure

```text
CAMPUS-VIBE/
│
├── college_event_management/
│   ├── backend/
│   │   └── app.py
│   │
│   ├── frontend/
│   │   ├── templates/
│   │   │   ├── welcome.html
│   │   │   ├── index.html
│   │   │   ├── login.html
│   │   │   └── signup.html
│   │   │
│   │   └── static/
│   │       ├── css/
│   │       ├── js/
│   │       └── images/
│   │
│   └── requirements.txt
│
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/PoojaR2804/CAMPUS-VIBE.git
```

### 2. Navigate to the Project Folder

```bash
cd CAMPUS-VIBE/college_event_management
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file or configure the following environment variables:

```text
MONGODB_URI=your_mongodb_connection_string
SECRET_KEY=your_secret_key
```

Replace the example values with your own credentials. Do not share your database password or secret key.

### 6. Run the Application

```bash
python backend/app.py
```

Open the following URL in your browser:

```text
http://127.0.0.1:5000
```

## 🌐 Live Demo

**Website:** [CampusVibe – Live Website](https://campus-vibe-9yv8.onrender.com)

**GitHub Repository:** [CAMPUS-VIBE](https://github.com/PoojaR2804/CAMPUS-VIBE)

## 🔐 Security

* Passwords are stored as secure password hashes.
* Login sessions are used to manage user access.
* Database credentials are configured through environment variables.

## 🚀 Future Enhancements

* Admin dashboard for managing events.
* Event creation and editing features.
* Email notifications for event registrations.
* Student registration history.
* Event search and category filters.
* QR code-based event attendance.
* Event feedback and rating system.

## 👩‍💻 Developed By

**Pooja R.**

Arunachala College of Engineering for Women
Nagercoil, Tamil Nadu

---

⭐ If you find this project useful, feel free to explore the repository and share your feedback.
