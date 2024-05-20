# Appointment System

## Overview

The Appointment System is a Django-based web application designed to manage and schedule appointments. It includes features for user authentication, appointment booking, and an admin panel for managing users and appointments.

## Features

- User Authentication: Secure login and registration system.
- Appointment Booking: Users can book, view, and cancel appointments.
- Admin Panel: Admins can manage users and appointments through a user-friendly interface.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Django 3.2 or higher
- PostgreSQL (or SQLite for local development)

### Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/ayush27072021/appointment-system.git
    cd appointment-system
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv env
    env\Scripts\activate   # On Windows
    source env/bin/activate  # On macOS/Linux
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the database:**

    - **For PostgreSQL:** Update `DATABASES` settings in `appointment_system/settings.py` with your PostgreSQL credentials.
    - **For SQLite (default):** No changes needed.

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / "db.sqlite3",
        }
    }
    ```

5. **Apply the migrations:**

    ```sh
    python manage.py migrate
    ```

6. **Create a superuser:**

    ```sh
    python manage.py createsuperuser
    ```

7. **Collect static files:**

    ```sh
    python manage.py collectstatic
    ```

8. **Run the development server:**

    ```sh
    python manage.py runserver
    ```

### Project Structure

- **appointment_system/**: Contains project-wide settings and URLs.
- **appointments/**: Contains the main app for booking appointments.
- **users/**: Handles user authentication and profile management.
- **static/**: Contains static files (CSS, JavaScript, images).
- **templates/**: Contains HTML templates for the project.

### Code Overview

#### Models

- **User**: Custom user model extending Django's AbstractUser.
- **Appointment**: Represents an appointment with fields for date, time, user, and status.

#### Views

- **User Views**: Handles user registration, login, and profile management.
- **Appointment Views**: Handles creating, viewing, and canceling appointments.

#### URLs

- **appointment_system/urls.py**: Project-level URL configurations.
- **appointments/urls.py**: URL configurations for the appointments app.
- **users/urls.py**: URL configurations for the users app.

### Code Flow

1. **User Authentication:**
    - Users can register and log in.
    - Authenticated users can access their profile and manage appointments.

2. **Appointment Booking:**
    - Users can book new appointments through a form.
    - Booked appointments are displayed in the user's dashboard.
    - Users can cancel their appointments if needed.

3. **Admin Panel:**
    - Admins can log in to the Django admin panel.
    - Admins can manage users and appointments from the admin interface.

### Contributing

1. **Fork the repository.**
2. **Create a new branch:**

    ```sh
    git checkout -b feature-branch
    ```

3. **Make your changes and commit them:**

    ```sh
    git commit -m "Description of your changes"
    ```

4. **Push to the branch:**

    ```sh
    git push origin feature-branch
    ```

5. **Open a pull request.**

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to customize this template as needed for your project. If you need further assistance, let me know!
