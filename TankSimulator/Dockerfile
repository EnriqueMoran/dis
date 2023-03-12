# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier containeddr logging
ENV PYTHONUNBUFFERED=1
ARG INSTALL_LIB=${INSTALL_LIB}

WORKDIR /app
COPY ./TankSimulator/requirements.txt .
COPY ./TankSimulator/src .
COPY ./TankSimulator/cfg .
COPY ./TankSimulator/tests .

# Install pip requirements
RUN python -m pip install -r requirements.txt

# Install open-dis library
COPY open-dis-python-20230223.tar.gz .
RUN if [ $INSTALL_LIB = 1 ] ; then \
        tar -xzf open-dis-python-20230223.tar.gz ; \
        pip install open-dis-python-master/. ; \
        apt-get update -y ; \
        apt-get install x11-xserver-utils -y ; \
    fi

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Expose used port to send PDU
EXPOSE 3000

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "/app/main.py"]