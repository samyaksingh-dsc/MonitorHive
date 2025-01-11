# Website Monitoring and Security Platform

## Setup Instructions

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Install dev dependencies: `pip install -r requirements-dev.txt`
6. Update .env file with your configurations
7. Initialize the database: `alembic upgrade head`
8. Run the application: `uvicorn backend.main:app --reload`

## Development

- Run tests: `pytest`
- Format code: `black .`
- Check types: `mypy .`
