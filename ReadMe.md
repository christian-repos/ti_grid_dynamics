(MVP) Retrieval-Augmented Generation API Usage Guide
=========
This guide will walk you through setting up the project environment and using the API. Within this repository, you'll find:

* Environment file
* The application
* Tests
* Dockerfile
* Kubernetes deployment file

Follow the instructions below to get started. Please note that this is not a production-ready code, it is a simple demo. 

## Configuring the .env File

1. Rename "envsample" file to ".env".
2. Add VOYAGE_API_KEY and OPENAI_API_KEY environment variables.

## Setting Up the Environment with Docker

1. Ensure you have Docker installed on your machine.
2. Navigate to this project directory where the "Dockerfile" file is located.
3. Run the following commands

```bash
docker build -t raq-sqlalchemy .
docker run -p 8000:8000 raq-sqlalchemy
```

## (Skip this if you used docker) Setting Up the Environment for easier local development

1. Ensure you have python 3.12 and pip installed on your system.
2. Navigate to this project directory where the "requirements.txt" file is located.
3. Install the required packages using pip:
    ```bash
    pip install --no-cache-dir -Ur requirements.txt
    ```
4. Run the FastAPI server with the following command after you enabled the virtual environment:
    ```bash
    uvicorn main:app --reload
    ```

## Accessing the Documentation
Open your web browser and go to http://127.0.0.1:8000/docs.
You will see the interactive API documentation.
![Documentation](/docs/docs.png?raw=true "Documentation interface")

In the top right corner, click on the lock icon and provide the REST_API_TOKEN from env
![Authorization](/docs/auth.png?raw=true "Authorization token")

## Routes
* /create_vector - Creates vectors from the latest SQLAlchemy documentation and saves them into a FAISS index. 
* /ask - process queries and returns a response.