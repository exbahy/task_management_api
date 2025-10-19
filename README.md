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

## Prerequisites

-   Python 3.8+
-   Django 4.0+

## Setup and Installation

Follow these steps to get the project running on your local machine.

**1. Clone the Repository (or Create the Files)**

If this were a git repository, you would clone it. Since you are creating the files, ensure they are in the correct structure as outlined.

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