FROM python:3.6.8

# Install dependencies
RUN pip install --upgrade pip
RUN pip3 install turicreate

# Set the working directory
WORKDIR /app

# Copy the Python script to the container
COPY train.py .
COPY uploads ./uploads

# Set the entrypoint command to run both commands simultaneously
CMD ["sh", "-c", "python3 train.py test1 & python3 train.py test2"]
