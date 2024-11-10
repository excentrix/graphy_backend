# FastAPI Project Setup

Follow these instructions to set up and run the FastAPI project using Uvicorn.

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the FastAPI application using Uvicorn:**

   ```bash
   uvicorn main:app --reload
   ```

   - `main` is the name of your Python file (without the `.py` extension).
   - `app` is the name of the FastAPI instance.

2. **Access the application:**

   Open your browser and navigate to `http://127.0.0.1:8000`.

For more details, refer to the [FastAPI documentation](https://fastapi.tiangolo.com/).
