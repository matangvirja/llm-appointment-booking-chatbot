# 📅 LLM Appointment Booking Chatbot

An AI-powered appointment booking chatbot built using **Google Gemini (LLM with tool calling)**, **FastAPI**, **PostgreSQL**, and **Docker**.

The chatbot understands natural language queries and books appointment slots based on defined business rules.

---

## 🚀 Features

* 🧠 Natural language booking using Google Gemini
* ⚡ FastAPI backend
* 🗄 PostgreSQL database
* 🐳 Fully Dockerized setup
* 📆 Appointment slots:

  * 9 AM – 7 PM
  * 1-hour slots
  * Lunch break: 1 PM – 2 PM (not bookable)
  * Only today + next 2 days
* ❌ Prevents duplicate bookings
* 🔄 LLM tool calling for function execution

---

## 🏗 Architecture Overview

```
User → FastAPI Endpoint → Gemini LLM
                              ↓
                        Tool Call Function
                              ↓
                         PostgreSQL DB
```

**Flow:**

1. User sends natural language input
2. Gemini interprets intent
3. Gemini calls backend tool (function)
4. Backend validates business rules
5. Appointment stored in database
6. Confirmation returned to user

---

## 📂 Project Structure

```
.
├── main.py                # FastAPI application
├── gemini.py              # Gemini LLM + tool calling logic
├── requirements.txt       # Python dependencies
├── Dockerfile
├── docker-compose.yml
├── .env.example           # Environment variable template
└── README.md
```

---

## 🛠 Tech Stack

* Python 3.10+
* FastAPI
* Google Gemini API
* SQLAlchemy
* PostgreSQL
* Docker & Docker Compose

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/matangvirja/llm-appointment-booking-chatbot.git
cd llm-appointment-booking-chatbot
```

---

### 2️⃣ Setup Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
DATABASE_URL=postgresql://postgres:password@db:5432/appointments
```

⚠️ Never commit your real API keys.

---

### 3️⃣ Run with Docker

```bash
docker-compose up --build
```

The API will run at:

```
http://localhost:8000
```

---

## 🧪 Example API Usage

### POST /chat

```json
{
  "message": "Book appointment for Alice tomorrow at 3 PM"
}
```

### Sample Response

```json
{
  "response": "✅ Appointment confirmed for Alice at 3 PM tomorrow."
}
```

---

## 💬 Example Conversations

### ✔ Valid Booking

**User:**

> Book appointment for John tomorrow at 11 AM

**Bot:**

> ✅ Appointment confirmed for John at 11 AM tomorrow.

---

### ❌ Slot Already Booked

**User:**

> Book appointment for Alex tomorrow at 11 AM

**Bot:**

> ❌ That slot is already booked. Please choose another time.

---

### ❌ Outside Working Hours

**User:**

> Book appointment at 8 PM

**Bot:**

> ❌ Appointments are available between 9 AM and 7 PM only.

---

## 📜 Business Rules

* Working hours: 9 AM – 7 PM
* Lunch break: 1 PM – 2 PM
* Maximum booking window: Today + 2 days
* 1-hour time slots only
* No duplicate bookings
* Validates input before DB insertion

---

## 🧠 How LLM Tool Calling Works

1. Gemini receives user input
2. Gemini detects booking intent
3. Gemini calls backend function like:

```python
book_appointment(name, date, time)
```

4. Backend validates:

   * Slot availability
   * Working hours
   * Date range
5. Returns structured confirmation

---

## 🧪 Future Improvements

* [ ] User authentication
* [ ] Frontend UI (React / Streamlit)
* [ ] Email/SMS notifications
* [ ] Admin dashboard
* [ ] Expand booking window beyond 2 days
* [ ] Add unit tests (pytest)

---

## 🔒 Security Notes

* Do NOT commit `.env`
* Store API keys securely
* Consider rate limiting in production
* Add input validation for production deployment

---

## 🧪 Running Without Docker (Optional)

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Ensure PostgreSQL is running locally and `DATABASE_URL` is correct.

---

## 📌 Why This Project?

This project demonstrates:

* Practical LLM tool integration
* Backend API development
* Database management
* Dockerized deployment
* Business rule enforcement
* Real-world AI system architecture

It can serve as a base for building:

* AI scheduling assistants
* Customer service bots
* Clinic booking systems
* Office automation tools

---

## 👨‍💻 Author

**Matang Virja**
AI Engineering Student
GitHub: [https://github.com/matangvirja](https://github.com/matangvirja)
