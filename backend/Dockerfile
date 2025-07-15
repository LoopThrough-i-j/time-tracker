FROM python:3.10-slim-bullseye

RUN apt-get -y update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip

WORKDIR /mercor-backend

RUN pip3 install uv

RUN uv venv

COPY requirements.txt requirements.txt

RUN uv pip install --system -r requirements.txt

COPY . .

EXPOSE 8080

# Run service on container startup
CMD ["python3", "main.py"]
