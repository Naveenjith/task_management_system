# Task Management App

This is a Django-based task management system designed to track tasks, worked hours, and completion reports. The application features a role-based permission system with three user types: Users, Admins, and SuperAdmins.

## Features

- **User:** View tasks, mark them as complete, and submit reports with their worked hours.  
- **Admin:** Allows assigning new tasks and reviewing the completion reports.  
- **SuperAdmin:** Can create, edit, and delete any user; view every task in the system; promote regular users to the Admin role or demote them.  

## Tech Stack

* **Python** & **Django**  
* **Django REST Framework**  
* **Django REST Framework Simple JWT**  
* **SQLite3**  

---

## Setup and Installation

1. **Clone the Repo**
    ```bash
    git clone https://github.com/Naveenjith/task_management_system.git
    cd task_management_system
    ```

2. **Set Up Your Virtual Environment**
    ```bash
    # Create the environment
    python -m venv venv

    # On Windows
    venv\Scripts\activate

    # On macOS/Linux
    source venv/bin/activate
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Database**
    Initial migrations
    ```bash
    python manage.py migrate
    ```

5. **Create Django Superuser Account**
    ```bash
    python manage.py createsuperuser
    ```

6. **Running server**
    ```bash
    python manage.py runserver
    ```
    The app will run at `http://127.0.0.1:8000/`.

7. **Final Steps**
    After Superuser creation, use the superuser credentials to login to the Dashboard,  
    Create a user,  
    Promote the user to admin,  
    Create another user,  
    Use the `edit` feature to assign the user to an admin.  

---

## API Endpoints

| Method | Endpoint                       | Description                     |
|--------|--------------------------------|---------------------------------|
| POST   | `/api/login/`                  | Log in for access/refresh tokens |
| POST   | `/api/token/refresh/`          | Get new access token             |
| GET    | `/task/api/task/`             | View all tasks                   |
| PUT    | `/task/api/task/<id>/completeview/` | Mark task as complete            |
| GET    | `/task/api/task/<id>/reportview/`   | View task reports                |

---

### User Workflow
The user authenticates via the `/api/login/` endpoint to receive a JWT. Using this token, they fetch their assigned tasks from `/task/api/task/` and submit completed work via a `PUT` request to `/task/api/task/<id>/completeview/`, including a report and worked hours.

### Admin Workflow
The Admin logs into the web dashboard. Their view is filtered to show only tasks assigned to users they manage. They can create new tasks for these users and review submitted completion reports. Their access is strictly limited to task management within their scope.

### SuperAdmin Workflow
The SuperAdmin has full system privileges via the web dashboard. They are responsible for all user account management (CRUD), role assignment (promoting/demoting Admins), and assigning users to be managed by Admins. They have a global view of all tasks and reports.
