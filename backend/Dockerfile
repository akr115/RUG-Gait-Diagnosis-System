FROM mambaorg/micromamba:debian12-slim

# Set working directory
WORKDIR /app

# Copy environment.yml and install dependencies
COPY flask/environment.yml .

# Create the environment
RUN micromamba create -y -n flask-env -f environment.yml && \
    micromamba clean --all --yes

# Copy your application code
COPY . .

# Expose Flask port
EXPOSE 8000

# Start the app
CMD ["micromamba", "run", "-n", "flask-env", "python", "flask/app.py"]

