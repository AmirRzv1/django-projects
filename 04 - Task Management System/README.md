# 📨 Task Management System (Version 1.2.0)

A simple yet well-structured **Task Management web application** built with **Django**.  
The project focuses on implementing **full CRUD operations** (Create, Read, Update, Delete) for tasks, along with **user authentication** features such as **register, login, and logout**.

The UI is intentionally kept **clean, simple, and minimal**, using **HTML, Bootstrap, a bit of CSS, and light JavaScript**, to emphasize **backend logic, Django architecture, and best practices** rather than heavy frontend design.

This project represents **Version 1**, serving as a solid foundation for learning and applying real-world Django concepts in a practical, organized way.

---

## 🚀 Features

- User authentication system:
  - User registration.
  - Login and logout functionality.
- Task management (CRUD):
  - Create new tasks.
  - View task list (dashboard).
  - Update existing tasks.
  - Delete tasks with confirmation.
- Tasks are user-specific (each user sees only their own tasks).
- Task fields include:
  - Title
  - Description
  - Status (ongoing, done, deleted)
- Clean dashboard UI for managing tasks.
- Minimal JavaScript for user interactions (confirmation dialogs).
- Bootstrap-based responsive layout.
- Versioned project structure using a `VERSION` file.

---

## 🛠️ Technologies & Best Practices

This project demonstrates **core Django concepts** and **professional development practices**:

### App Structure
- Standard Django project and app structure.
- Clear separation of concerns:
  - `models.py` for data structure.
  - `views.py` for request handling.
  - `forms.py` for form logic.
  - `urls.py` for routing.
- Each app manages its own responsibility.

### Views
- **Class-Based Views (CBV)** used intentionally for clarity and scalability.
- Proper use of `get()` and `post()` methods.
- Secure object retrieval based on logged-in user.
- Clear separation between create, update, delete, and list views.

### Forms
- Usage of **Django Forms** and **ModelForms**.
- Form validation handled server-side.
- Reusable and clean form definitions.
- Pre-filled forms for update operations using `instance`.

### Authentication & Authorization
- Built on Django’s authentication system.
- Login-required access for task-related views.
- Tasks linked to users using foreign keys.
- Secure handling of user-owned data.

### URLs & Routing
- Clean and readable URL patterns.
- **Namespaced URLs** for better organization.
- Dynamic URL parameters for task operations.
- Consistent URL design across the project.

### Templates & UI
- Simple and readable HTML templates.
- Minimal logic inside templates.
- Bootstrap used for layout and styling.
- Clear user feedback with messages framework.
- Buttons and actions placed intuitively in the UI.

### JavaScript Integration
- JavaScript used only where necessary.
- Simple confirmation dialog before deleting tasks.
- No heavy frontend frameworks — focus stays on Django.


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