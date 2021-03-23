FROM python:3.6

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    python3-dev

# For requirements
RUN pip install -r requirements.txt


# CMD ["python", "jsongenerator.py"]