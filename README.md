# 🤖 LLM-Based AI Appointment Booking Chatbot

An intelligent appointment booking system powered by **Google Gemini (LLM)** with tool-calling capabilities, integrated with a **FastAPI backend**, **PostgreSQL database**, and fully containerized using **Docker**.

This project demonstrates real-world LLM integration with backend APIs and structured business logic validation.

---

## 🚀 Features

* 🧠 Natural language appointment booking
* 🔧 Gemini Tool Calling (Function Calling)
* ⚡ FastAPI REST backend
* 🐘 PostgreSQL database with SQLAlchemy ORM
* 🕒 Business hours validation (9 AM – 7 PM)
* 📅 Appointment allowed only for Today + Next 2 Days
* ⛔ Unique time slot enforcement
* ✅ Appointment approval / rejection system
* 🐳 Dockerized setup

---

## 🏗 System Architecture

```
User
  ↓
Gemini LLM (Tool Calling)
  ↓
FastAPI Backend
  ↓
PostgreSQL Database
  ↑
Tool Response → Gemini → User
```

---

## 🛠 Tech Stack

* **LLM**: Google Gemini 2.5 Flash
* **Backend**: FastAPI
* **Database**: PostgreSQL
* **ORM**: SQLAlchemy
* **Containerization**: Docker & Docker Compose
* **Environment Management**: python-dotenv
* **Language**: Python 3.10+

---

## 📂 Project Structure

```
.
├── main.py              # FastAPI backend
├── gemini.py            # LLM + Tool calling logic
├── docker-compose.yml   # Docker orchestration
├── Dockerfile           # Container setup
├── requirements.txt     # Dependencies
├── .env.example         # Example environment variables
├── .gitignore
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/llm-appointment-booking-chatbot.git
cd llm-appointment-booking-chatbot
```

---

### 2️⃣ Create `.env` File

Create a file named `.env`:

```
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=postgresql://postgres:password@db:5432/appointments
```

⚠️ Never commit your real API key.

---

### 3️⃣ Run with Docker

```bash
docker-compose up --build
```

This will:

* Start PostgreSQL
* Start FastAPI backend
* Create database tables automatically

---

### 4️⃣ Run the Chatbot

In a new terminal:

```bash
python gemini.py
```

You can now book appointments using natural language like:

```
Book an appointment for John tomorrow at 10 AM
```

---

## 📌 API Endpoints

| Method | Endpoint       | Description                |
| ------ | -------------- | -------------------------- |
| GET    | `/view`        | View all appointments      |
| GET    | `/detail/{id}` | Get appointment by ID      |
| POST   | `/create`      | Create appointment         |
| PUT    | `/accept/{id}` | Approve appointment        |
| PUT    | `/reject/{id}` | Reject appointment         |
| GET    | `/pending`     | View pending appointments  |
| GET    | `/approved`    | View approved appointments |
| GET    | `/rejected`    | View rejected appointments |

Swagger Docs available at:

```
http://localhost:8000/docs
```

---

## 🔒 Business Rules Implemented

* Appointment must be:

  * Between 9:00 AM and 7:00 PM
  * On the hour (e.g., 10:00, 11:00)
  * Today or within next 2 days
* Appointment time must be unique
* Appointment ID must be unique

---

## 🧪 Example Flow

1. User: "Book appointment for John tomorrow at 10 AM"
2. Gemini extracts structured parameters
3. Gemini calls backend function
4. FastAPI validates & stores data
5. Gemini responds with confirmation

---

## 🎯 Learning Outcomes

This project demonstrates:

* LLM tool calling integration
* Backend API design
* SQLAlchemy ORM usage
* Docker-based deployment
* Environment variable security
* Real-world business rule validation

---

## 🚀 Future Improvements

* 🌐 Web UI (React / Next.js)
* 🔐 JWT Authentication
* 📊 Admin Dashboard
* 🤖 Auto slot suggestion
* ☁️ Deployment on AWS / GCP
* 🧪 Unit & Integration Tests
* 🔄 CI/CD Pipeline

---

## 👨‍💻 Author

Matang Virja 
AI Engineering Student

---
    
