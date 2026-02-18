# 🤖 LLM Appointment Booking Chatbot

An AI-powered appointment booking chatbot built using:

* 🧠 Google Gemini (LLM with tool calling)
* ⚡ FastAPI backend
* 🐘 PostgreSQL database
* 🐳 Docker & Docker Compose

This project demonstrates how an LLM can interact with a backend API to create real-world appointments with proper business validation.

---

# 🚀 Features

* Natural language appointment booking
* Gemini function/tool calling
* Business hours validation (9 AM – 7 PM)
* Only today + next 2 days allowed
* Unique appointment time enforcement
* Approve / Reject appointment endpoints
* Fully Dockerized setup

---

# 🛠 Tech Stack

* Python 3.10+
* FastAPI
* PostgreSQL
* SQLAlchemy
* Docker
* Google Gemini API

---

# 📂 Project Structure

```
.
├── main.py              # FastAPI backend
├── gemini.py            # LLM chatbot logic
├── docker-compose.yml   # Docker services
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

---

# ⚙️ Setup Instructions (Step-by-Step)

## ✅ Step 1 — Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/llm-appointment-booking-chatbot.git
cd llm-appointment-booking-chatbot
```

---

## ✅ Step 2 — Install Docker

Make sure Docker is installed:

```bash
docker --version
docker-compose --version
```

If not installed, download Docker Desktop from:
[https://www.docker.com/](https://www.docker.com/)

---

## ✅ Step 3 — Create Environment File

Create a file named:

```
.env
```

Add:

```
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=postgresql://postgres:password@db:5432/appointments
```

⚠️ Do not push this file to GitHub.

---

## ✅ Step 4 — Start PostgreSQL + FastAPI Using Docker

Run:

```bash
docker-compose up --build
```

This will automatically:

* Start PostgreSQL database
* Create the `appointments` database
* Start FastAPI server
* Create required tables

---

## ✅ Step 5 — Verify Backend

Open your browser:

```
http://localhost:8000/docs
```

You should see FastAPI Swagger UI.

This means PostgreSQL and backend are connected successfully.

---

## ✅ Step 6 — Run the Chatbot

Open a new terminal:

```bash
python gemini.py
```

You can now type:

```
Book appointment for John tomorrow at 10 AM
```

The chatbot will:

1. Extract structured data
2. Call backend API
3. Store data in PostgreSQL
4. Return confirmation

---

# 📌 Available API Endpoints

| Method | Endpoint       | Description           |
| ------ | -------------- | --------------------- |
| GET    | `/view`        | View all appointments |
| GET    | `/detail/{id}` | Get appointment by ID |
| POST   | `/create`      | Create appointment    |
| PUT    | `/accept/{id}` | Approve appointment   |
| PUT    | `/reject/{id}` | Reject appointment    |

---

# 🐘 How PostgreSQL Is Setup

PostgreSQL runs inside Docker.

When you run:

```bash
docker-compose up
```

Docker:

* Pulls PostgreSQL image
* Creates database
* Connects FastAPI using `DATABASE_URL`
* Automatically creates tables on startup

No manual database setup required.

---

# 🔒 Business Rules Implemented

* Appointment must be between 9 AM – 7 PM
* Appointment must be on the hour (10:00, 11:00, etc.)
* Appointment allowed only today + next 2 days
* No duplicate time slots
* No duplicate IDs

---

# 🎯 Learning Outcomes

This project demonstrates:

* LLM tool calling integration
* Backend API development
* Database modeling with SQLAlchemy
* Docker-based deployment
* Secure environment variable management

* Help you deploy this project live
* Review your entire repo before publishing 🚀
