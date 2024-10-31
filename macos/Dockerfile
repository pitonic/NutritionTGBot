FROM dockurr/macos

COPY ./macos/requirements.txt requirements.txt

RUN apt update && \
    apt install --no-install-recommends -y pip && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*
