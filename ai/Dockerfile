# Stage 1: Build environment
FROM ubuntu:22.04 as builder

# Install necessary system dependencies
RUN apt update && \
    apt install --no-install-recommends -y gcc libgl1 libglib2.0-0 libpython3-dev gnupg curl && \
    # Install Xcode command-line tools
    apt install -y --no-install-recommends software-properties-common && \
    apt-add-repository 'deb http://archive.ubuntu.com/ubuntu/ focal main restricted' && \
    apt update && \
    apt install -y --no-install-recommends xcode-select && \
    xcode-select --install && \
    # Upgrade pip
    apt install -y --no-install-recommends python3-pip && \
    pip install --upgrade pip

# Stage 2: Final image
FROM python:3.10-slim

# Copy the requirements file
COPY ./ai/requirements.txt requirements.txt

# Copy dependencies from the builder stage
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/local/lib /usr/local/lib
COPY --from=builder /usr/local/include /usr/local/include
COPY --from=builder /usr/local/share /usr/local/share

# Install necessary system dependencies
RUN apt update && \
    apt install --no-install-recommends -y gcc libgl1 libglib2.0-0 libpython3-dev gnupg && \
    # Upgrade pip
    pip install --upgrade pip && \
    # Install Python dependencies
    pip install --no-cache-dir -r requirements.txt && \
    # Clean up
    rm -rf /var/lib/apt/lists/*

#CMD ["bash", "-c", "sleep infinity"]
#CMD ["bash", "-c", "streamlit run tracker.py"]
CMD ["bash", "-c", "streamlit run ocrmac.py"]
