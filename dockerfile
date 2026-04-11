# 1. Start with a very small Python base image
FROM python:3.10-alpine

# 2. Set environment variables to prevent unwanted behavior
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory in the container
WORKDIR /app

# 4. Install system dependencies needed for certain Python packages (like Pillow)
#    We use '--no-cache' and combine commands to keep the layer small.
RUN apk add --no-cache --virtual .build-deps gcc musl-dev linux-headers \
    && apk add --no-cache libjpeg-turbo-dev zlib-dev jpeg-dev

# 5. Copy only the requirements file first (for better caching)
COPY requirements.txt .

# 6. Install Python dependencies, crucially including the CPU-only PyTorch
#    The '--no-cache-dir' flag is critical for keeping the image size down.
RUN pip install --no-cache-dir torch==2.0.1 --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

# 7. Copy the rest of your application code
COPY . .

# 8. Expose the port your app runs on
EXPOSE 8000

# 9. Command to run your FastAPI app
# Change CMD to use the root main.py
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]