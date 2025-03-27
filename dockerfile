FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY

# Copy the requirements file
COPY ./* ./

RUN pip install --upgrade pip

# Install dependencies, including DVC for S3 support
RUN pip install --no-cache-dir -r requirements.txt

# Pull data from DVC
RUN dvc pull  # This fetches the tracked data from your DVC remote (S3)

# Expose the port for the FastAPI application
EXPOSE 8000

# Command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]