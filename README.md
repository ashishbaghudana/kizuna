# Kizuna - A Personal Relationship Manager

Kizuna is a simple, private web application designed to help you nurture your personal and professional relationships. It provides a centralized place to manage important information about your contacts, remember key dates, and keep track of interactions.

---

## Technology Stack
* **Backend:** Python 3.10+ with Flask
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Migrations:** Alembic
* **Frontend:** JavaScript (Framework TBD)

---

## Setup & Installation

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/](https://github.com/)<Your-Username>/kizuna.git
    cd kizuna
    ```

2.  **Create and Activate Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables:**
    Create a `.env` file in the project root. Copy the contents of `.env.example` (if you create one) or use the following template:
    ```env
    SECRET_KEY=your-super-secret-and-random-string
    DATABASE_URL=postgresql://user:password@localhost/kizuna
    ```

---

## Database Migrations

This project uses Alembic to manage database schema changes.

1.  **Generate a New Migration (after changing models):**
    ```bash
    alembic revision --autogenerate -m "A descriptive message about the change"
    ```

2.  **Apply Migrations:**
    ```bash
    alembic upgrade head
    ```

3.  **Reset Database (for development only):**
    A custom command is available to wipe and recreate the database.
    ```bash
    flask reset-db
    ```

---

## Running the Application

1.  **Set the Flask App environment variable:**
    ```bash
    export FLASK_APP=wsgi.py
    ```

2.  **Run the development server:**
    ```bash
    flask run
    ```
    The API will be available at `http://127.0.0.1:5000`.

---

## API Endpoints (Current)

* `POST /api/users`: Create a new user.
* `POST /api/contacts`: Create a new contact.
* `GET /api/users/<user_id>/contacts`: Get a list of a user's contacts.
* `GET /api/contacts/<contact_id>`: Get a single contact's details.
* `PUT /api/contacts/<contact_id>`: Update a contact's name.
* `DELETE /api/contacts/<contact_id>`: Delete a contact.
* `POST /api/contacts/<contact_id>/phone_numbers`: Add a phone number to a contact.