# Task Manager API

A **Django REST Framework** (DRF) project for managing tasks and task assignments. Users can create tasks, assign them to other users, and track their status. Authentication is done using **JWT (JSON Web Tokens)**.

---

## **Features**

- User signup and JWT authentication
- CRUD operations for tasks
- Assign tasks to users
- Track task status (pending, in progress, completed)
- Permissions: only creators or admins can update/delete tasks; assigned users or admins can update assignments
- Filtering and optional due dates for tasks
- Pagination for task lists

---

## **API Endpoints** 

Endpoint	Method	Description
/api/users/	POST	Create a new user
/api/token/	POST	Obtain JWT access & refresh tokens
/api/token/refresh/	POST	Refresh JWT access token
/api/users/	GET	List all users (admin only)
/api/users/{id}/	GET / PUT / PATCH	Retrieve or update user info
/api/tasks/	GET / POST	List all tasks / Create a task
/api/tasks/{id}/	GET / PUT / PATCH / DELETE	Retrieve / update / delete a task
/api/task-assignments/	GET / POST	List assignments / Assign a task
/api/task-assignments/{id}/	GET / PUT / PATCH / DELETE	Retrieve / update / delete an assignment

## **Technologies Used**

- Python 3.x
- Django 5.2.6
- Django REST Framework 3.16.1
- Django Filter 25.1
- djangorestframework-simplejwt 5.5.1
- MySQL (or SQLite for development)
- Postman (for API testing)

---

## **Installation**

1. **Clone the repository:**

```bash
git clone <your_repo_url>
cd task_manager
