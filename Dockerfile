# Use an official Python runtime as a parent image
FROM python:3.10-alpine

# Set max Memory Usage for Container
ENV MAX_MEMORY_USAGE=2048

RUN mkdir -p /usr/share/dcbot

# Set the working directory to /usr/share/dcbot
WORKDIR /usr/share/dcbot

# Copy the requirements file to the working directory
COPY requirements.txt .

RUN pip install --upgrade pip
#RUN pip install --no-cache-dir TTS
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY bot/ ./

VOLUME ["/usr/share/dcbot/configs", "/usr/share/dcbot/chats"]

CMD ["python", "bot.py"]
