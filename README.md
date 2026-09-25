# Employee Management API

A RESTful **Employee Management API** built with **FastAPI, PostgreSQL, SQLAlchemy, and Pydantic**.

## 🚀 Features

* Employee CRUD operations
* Department filtering
* Employee search
* Email & phone uniqueness validation
* Pydantic validation
* Database error handling
* Transaction management
* Swagger/OpenAPI documentation

## 🛠️ Tech Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic
* Uvicorn

## 📁 Structure

```text
employee-api/
├── database/
├── models/
├── schemas/
├── services/
├── routers/
├── main.py
└── requirements.txt
```

## ⚙️ Setup

```bash
git clone <repository-url>
cd employee-api

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

Create PostgreSQL database:

```sql
CREATE DATABASE employee_db;
```

Run the application:

```bash
uvicorn main:app --reload
```

## 🔗 API Endpoints

| Method | Endpoint          | Description     |
| ------ | ----------------- | --------------- |
| POST   | `/employees/`     | Create employee |
| GET    | `/employees/`     | Get employees   |
| GET    | `/employees/{id}` | Get employee    |
| PUT    | `/employees/{id}` | Full update     |
| PATCH  | `/employees/{id}` | Partial update  |
| DELETE | `/employees/{id}` | Delete employee |

## 🔍 Search & Filter

```http
GET /employees/?department=IT
```

```http
GET /employees/?search=rahul
```

```http
GET /employees/?department=IT&search=rahul
```

## 📚 Documentation

Swagger:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

## 👨‍💻 Author

**Sagar Maurya**

GitHub: https://github.com/sagarMaurya81
