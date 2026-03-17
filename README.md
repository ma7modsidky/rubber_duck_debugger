# 🦆 Rubber Duck AI | Agentic Debugger

An AI-powered diagnostic dashboard that transforms messy Python tracebacks into actionable resolutions. Built with Django and Google Gemini (via LangChain), it maintains a **memory** of past errors to provide context-aware debugging assistance.

---

## 🚀 Features

- **Traceback Analysis**  
  Paste raw Python logs and receive clear root-cause explanations with suggested fixes.

- **Contextual Memory**  
  Uses PostgreSQL to track error history and detect recurring issues.

- **Modern UI**  
  Responsive dark-mode dashboard built with Tailwind CSS and Markdown rendering.

- **Containerized Setup**  
  Fully Dockerized for consistent development and easy deployment.

---

## 🛠️ Tech Stack

**Backend**
- Django 5.0
- Python 3.11

**AI Orchestration**
- LangChain
- Google Gemini 3.1 Flash

**Database**
- PostgreSQL 15

**Frontend**
- Tailwind CSS (Typography + Prose)

**DevOps**
- Docker
- GitHub Actions (CI)

---

## 📦 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/rubber-duck-ai.git
cd rubber_duck_ai
```

### 2️⃣ Environment Setup

Create a `.env` file in the project root:

```env
SECRET_KEY=your_very_long_secret_random_string_for_django_security
DEBUG=True
DATABASE_URL=postgres://postgres:postgres@db:5432/rubber_duck_db
GOOGLE_API_KEY=your_key
```

### 3️⃣ Run with Docker

```bash
docker-compose up --build
```

The application will be available at:

```
http://localhost:8000
```

---

## 🧪 Testing

Run migrations and tests inside the container:

```bash
docker compose exec web python manage.py migrate
docker compose exec web pytest
```

---

<!-- ## 📁 Project Structure

```
rubber_duck_ai/
│
├── apps/
    ├── debugger/
├── config/
├── templates/
├── static/
├── manage.py
└── docker-compose.yml
└── docker-compose.yml
``` -->

---

## 🤝 Contributing

Contributions are welcome! Please open an issue to discuss proposed changes or submit a pull request.

---

## 📜 License

This project is licensed under the MIT License.