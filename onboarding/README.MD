# OmniDock Onboarding

## Setup

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd <repo-name>
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

3. Activate the virtual environment:
   ```bash
   poetry shell
   ```

## Start the Application

To run the development server:

```bash
python manage.py runserver
```

## Database Migrations

To manage database schema changes:

- Create new migrations:
  ```bash
  python manage.py makemigrations
  ```

- Apply migrations:
  ```bash
  python manage.py migrate
  ```