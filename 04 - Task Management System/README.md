# 📨 Task Management System (Version 2.0.0)

A **microservices-based Task Management web application** built with **Django**.  
This project demonstrates the transition from a **monolithic architecture** to a **microservices architecture**, implementing **full CRUD operations** for tasks with **user authentication** across distributed services.

The UI remains **clean, simple, and minimal** using **HTML, Bootstrap, CSS, and light JavaScript**, while the focus shifts to **microservices design patterns, inter-service communication, and distributed system architecture**.

This is **Version 2**, representing a significant architectural evolution from the monolithic Version 1, showcasing real-world microservices concepts and Django best practices.

---

## 🏗️ Architecture Overview

The application is split into **three independent services**:

### 1. **User Service** (Authentication Service)
- Handles user registration, login, and logout
- Manages user data and authentication
- Exposes REST endpoints for user operations
- Independent service responsible for all user-related logic

### 2. **Task Service** (Task Management Service)
- Manages all task CRUD operations
- Handles task status transitions (ongoing, completed, soft_delete)
- Exposes REST endpoints for task operations
- Stores task data with user ownership references

### 3. **Web Service** (Frontend/Gateway Service)
- Serves the user interface (HTML templates)
- Acts as the entry point for user requests
- Communicates with User Service and Task Service via HTTP
- Aggregates data from backend services for the frontend

### Communication Pattern
- **Inter-service communication**: HTTP requests using Python's `requests` library
- **Shared Database**: All services connect to a single PostgreSQL database (Version 2 design choice)
- **Synchronous calls**: Services communicate directly via REST endpoints

---

## 🚀 Features

### User Management
- User registration with validation
- Login and logout functionality
- Session-based authentication
- User-specific data isolation

### Task Management (CRUD)
- Create new tasks with title and description
- View task list on dashboard (user-specific)
- Update existing tasks
- Soft delete (mark as deleted, recoverable)
- Hard delete (permanent removal)
- Restore soft-deleted tasks
- Task status management: ongoing, completed, soft_delete

### Microservices Features
- Service separation by domain (users, tasks, web interface)
- Independent service deployment capability
- HTTP-based inter-service communication
- Centralized database with service-specific tables

---

## 🛠️ Technologies & Architecture Patterns

### Microservices Architecture
- **Service decomposition** by business capability
- **Shared database pattern** (single PostgreSQL instance)
- **API-based communication** between services
- Each service runs independently on different ports

### Inter-Service Communication
- **HTTP/REST** for synchronous communication
- Python `requests` library for service-to-service calls
- JSON data exchange format
- Error handling for network failures

### Database Design
- **PostgreSQL** as the shared database
- Service-specific models and tables
- Foreign key relationships using user IDs
- Task ownership tracked via `owner` field

### Django Best Practices
- **Class-Based Views (CBV)** for clean, reusable code
- **Django Forms** and **ModelForms** for validation
- **Authentication system** integrated across services
- **URL namespacing** for organized routing
- **Template inheritance** for consistent UI

### Service Structure
Each service follows standard Django structure:
- `models.py` - Data models
- `views.py` - Request handlers (API endpoints or template views)
- `urls.py` - URL routing
- `settings.py` - Service-specific configuration

### Frontend
- Bootstrap-based responsive design
- Minimal JavaScript for interactions
- Server-side rendering with Django templates
- Clean separation between presentation and logic

---
## 📌 Planned Versions & Future Improvements

This project is intentionally developed in **incremental versions**.  
Each version introduces new concepts and best practices to deepen understanding of Django and real-world backend development.

### 🔹 Version 1.1.0 – Dashboard & Task Management Enhancements (Done)
Focus: Improving usability and introducing real-world task handling patterns.

Planned improvements:
- Dashboard statistics (total tasks, ongoing, completed, deleted).
- Task filtering by status (All / Ongoing / Done / Deleted).
- Soft delete mechanism (Recycle Bin instead of permanent deletion).
- Restore deleted tasks from Recycle Bin.
- Permanent delete option for deleted tasks.
- Improved success and error feedback messages.
---

### 🔹 Version 1.2.0 – Authentication & Security Improvements
Focus: Enhancing user authentication and security flows.

Planned improvements:
- Forgot password functionality using Django’s built-in auth system.
- Email-based password reset flow.
- Improved form validation and error handling.
- Access control hardening (ownership checks on all task actions).
---

### 🔹 Version 2.0.0 – User Profiles & Custom User Model
Focus: Extending user functionality and preparing for scalable authentication.

Planned improvements:
- User profile page (username, email, join date, task statistics).
- Profile access from dashboard.
- Custom User model implementation.
- Authentication using email instead of username.
- Foundation for phone number authentication in future versions.
---

### 🔹 Version 2.1.0 – Task Features & Productivity Tools
Focus: Making tasks more powerful and realistic.

Planned improvements:
- Task priority levels (Low / Medium / High).
- Due dates for tasks.
- Overdue task highlighting.
- Sorting tasks by priority or due date.
- Improved task UI indicators.
---

### 🔹 Version 3.0.0 – UX, Performance & Advanced Features
Focus: Preparing the project for real production scenarios.

Planned improvements:
- Pagination for large task lists.
- Task search functionality.
- Confirmation modals using Bootstrap (instead of basic JS alerts).
- Improved UI/UX consistency.
- Performance optimizations on database queries.
- Optional API layer using Django REST Framework.
---

### 🚀 Long-Term Vision
The long-term goal of this project is to evolve from a learning-focused Django app into a **clean, scalable, and production-ready task management system**, while maintaining simplicity and clarity at each development stage.

---

## 🏗 Folder Structure - V1

The project follows a **clear and modular Django structure**, separating concerns between authentication, core layout, and task management.  
Each app contains its own templates, keeping the project organized and easy to maintain.

```text
project_root/
├── accounts/
│   ├── urls.py
│   ├── views.py
│   ├── forms.py
│   ├── models.py
│   └── templates/
│       └── accounts/
│           ├── login.html
│           └── register.html
│
├── core/
│   ├── urls.py
│   ├── views.py
│   └── templates/
│       └── core/
│           ├── base.html
│           └── landing.html
│
├── tasks/
│   ├── urls.py
│   ├── views.py
│   ├── forms.py
│   ├── models.py
│   └── templates/
│       └── tasks/
│           ├── dashboard.html
│           ├── task_create.html
│           └── task_update.html
│
├── task_manager/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── db.sqlite3
├── manage.py
├── README.md
├── VERSION
└── todo