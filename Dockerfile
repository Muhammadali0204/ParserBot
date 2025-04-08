FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl unzip wget gnupg ca-certificates \
    libnss3 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 libgbm1 \
    libasound2 libatk1.0-0 libatk-bridge2.0-0 libgtk-3-0 xdg-utils fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google.gpg \
&& echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
> /etc/apt/sources.list.d/google-chrome.list \
&& apt-get update \
&& apt-get install -y google-chrome-stable


COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./ /app/
