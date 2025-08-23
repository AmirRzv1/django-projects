# 🌐 Social Network Website (Version 1.0.0)


A simple social networking platform built with **Django**.  
Users can register, log in, and interact with other users by creating posts, following/unfollowing, liking/disliking posts, and adding comments with replies.  
The UI is intentionally kept **basic and minimal** to focus on learning Django best practices rather than frontend design.  

This project serves as a practice implementation of core Django features and techniques, resembling a simplified version of platforms like **Stack Overflow** or **Twitter**.

---

## 🚀 Features
- User authentication (Login, Logout, Registration, Password Reset via Gmail).
- Post creation and display on the homepage.
- Like/Dislike posts.
- Comment and reply on posts.
- Follow/Unfollow other users.
- Custom error handling (custom 404 page instead of default 500).
- Extended User model with signals.
- Custom admin panel.
- Simple, clean structure with reusable apps and templates.

---

## 🛠️ Technologies & Best Practices

This project demonstrates Django’s core features and clean coding techniques:

- **App Structure**
  - Standard app naming conventions.
  - Each app has its own `templates/` folder with subfolders named after the app to avoid duplication.

- **Views & Forms**
  - Used **Class-Based Views (CBV)**.
  - Applied **LoginRequiredMixin** for restricting access.
  - Customized with `dispatch()` method for fine-grained control.
  - Forms use Django **widgets** and **custom validation** (`clean()` methods + field-level validation).

- **Authentication & Authorization**
  - Custom authentication backend (email-based login).
  - Extended `User` model via **AbstractUser**.

- **URLs & Navigation**
  - Used **namespaced URLs**.
  - Applied `reverse()` and `reverse_lazy()` for generating URLs.
  - Implemented `get_absolute_url()` in models for clean routing.
  - Supported **next parameter** handling for redirects.

- **Models & ORM**
  - Applied backward relations with `related_name`.
  - Query optimization with `order_by` and **Meta ordering**.
  - Used **signals** for automatic user-related actions.

- **Templates**
  - Kept templates lightweight (minimal logic).
  - Pushed complexity into views/models.
  - 
---

## 🏗 Folder Structure

> The project follows a modular app-based structure.  
> Each app (`account`, `home`, `post`) contains its own `templates/` folder,  
> with a subfolder named after the app to avoid conflicts and keep things organized.

<pre lang="markdown">
project_root/
├── account/
├── home/
├── post/
├── social_network/
├── templates/
├── db.sqlite3
├── manage.py
└── VERSION
</pre>

---

## 📂 Project Structure Highlights
- Each app has its own templates folder with app-specific subfolders.
- Minimal template logic, more in views/models.
- Proper URL namespacing to prevent conflicts.
- Organized use of `forms.py`, `views.py`, and models for clean architecture.

---

## 📌 Planned Features (Future Versions)
- Profile improvements:  
  - Show follower/following lists & counts.  
  - Display number of posts per user.  
- Enhanced profile management (profile pictures, bios, etc.).  
- Improved UI/UX with better design and buttons.  
- Additional search and filtering features.  
- More interactive dashboard and notifications.

---