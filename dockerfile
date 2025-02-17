FROM python:3.10
WORKDIR /usr/local/app

# Install the application dependencies
COPY api ./api
RUN python -m ensurepip --upgrade
RUN pip install --upgrade pip setuptools --no-cache-dir
RUN pip install --no-cache-dir -r ./api/requirements.txt
RUN rm -rf /root/.cache/pip

# Expose port
EXPOSE 8001

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

CMD ["fastapi", "run", "api/main.py", "--host", "0.0.0.0", "--port", "8001"]