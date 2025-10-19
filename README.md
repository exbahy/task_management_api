# Django Task Manager

A full-stack task management web application built with Django. This project allows users to register, log in, and manage their personal tasks through a simple and clean user interface.

The application is built using a traditional server-side rendering approach and does not require any JavaScript for its core functionality.

## Features

-   **User Authentication**: Secure user registration and login system.
-   **Task Management (CRUD)**:
    -   **Create**: Add new tasks with a title, description, due date, and priority.
    -   **Read**: View a list of all your tasks, sorted by the due date.
    -   **Update**: Edit existing tasks.
    -   **Delete**: Remove tasks you no longer need.
-   **Task Status**: Mark tasks as "Completed" or "Pending".
-   **Task Prioritization**: Assign "Low", "Medium", or "High" priority to tasks, with visual indicators.
-   **Secure**: Users can only view and manage their own tasks.

## Key URL Endpoints and Functionality

Since this is a server-side rendered application, it does not expose a JSON API. Instead, it uses URL endpoints that handle standard web form data (`application/x-www-form-urlencoded`) and respond with rendered HTML pages.

Here is a breakdown of the key functionalities:

---

### 1. View All Tasks

-   **Endpoint**: `/tasks/`
-   **HTTP Method**: `GET`
-   **Description**: Displays all tasks for the currently logged-in user.
-   **Request Body**: None. Requires an active session (user must be logged in).
-   **Response**: Renders the `task_list.html` template with a list of the user's tasks.

---

### 2. Add a New Task

-   **Endpoint**: `/tasks/create/`
-   **HTTP Methods**: `GET`, `POST`
-   **Description**:
    -   `GET`: Displays the form for creating a new task.
    -   `POST`: Submits the data to create the new task in the database.
-   **Request Body (POST Form Data)**:
    ```
    csrfmiddlewaretoken: (Django's security token)
    title: "Your Task Title"
    description: "A description of the task."
    due_date: "YYYY-MM-DD"
    priority: "High" | "Medium" | "Low"
    ```
-   **Response**:
    -   `GET`: Renders the `task_form.html` template.
    -   `POST`: On success, redirects to the task list (`/tasks/`). On validation error, it re-renders the `task_form.html` with error messages.

---

### 3. Edit an Existing Task

-   **Endpoint**: `/tasks/update/<int:pk>/` (e.g., `/tasks/update/1/`)
-   **HTTP Methods**: `GET`, `POST`
-   **Description**:
    -   `GET`: Displays the task form pre-filled with the existing task's data.
    -   `POST`: Submits the updated data for the task.
-   **Request Body (POST Form Data)**: Same as creating a task.
-   **Response**:
    -   `GET`: Renders the `task_form.html` template.
    -   `POST`: On success, redirects to the task list (`/tasks/`).

---

### 4. Delete a Task

-   **Endpoint**: `/tasks/delete/<int:pk>/` (e.g., `/tasks/delete/1/`)
-   **HTTP Methods**: `GET`, `POST`
-   **Description**:
    -   `GET`: Shows a confirmation page to prevent accidental deletion.
    -   `POST`: Deletes the task from the database.
-   **Request Body (POST Form Data)**:
    ```
    csrfmiddlewaretoken: (Django's security token)
    ```
-   **Response**:
    -   `GET`: Renders the `task_confirm_delete.html` template.
    -   `POST`: On success, redirects to the task list (`/tasks/`).

---

### 5. Mark Task as Complete/Pending

-   **Endpoint**: `/tasks/toggle/<int:pk>/` (e.g., `/tasks/toggle/1/`)
-   **HTTP Method**: `POST`
-   **Description**: Toggles the status of a task between 'Pending' and 'Completed'.
-   **Request Body (POST Form Data)**:
    ```
    csrfmiddlewaretoken: (Django's security token)
    ```
-   **Response**: Redirects to the task list (`/tasks/`) with the task's status updated.

---

## Prerequisites

-   Python 3.8+
-   Django 4.0+

## Setup and Installation

Follow these steps to get the project running on your local machine.

**1. Clone the Repository (or Create the Files)**

If this were a git repository, you would clone it. Since you are creating the files, ensure they are in the correct structure.

**2. Create and Activate a Virtual Environment**

It's highly recommended to use a virtual environment to manage project dependencies.

```bash
# Navigate to the project's root directory
cd path/to/task_manager

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate