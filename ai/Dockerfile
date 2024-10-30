FROM python:3.10-slim

# Copy the requirements file
COPY ./ai/requirements.txt requirements.txt

# Install necessary system dependencies
RUN apt update && \
    apt install --no-install-recommends -y gcc libgl1 libglib2.0-0 libpython3-dev gnupg curl && \
    # Download and install Xcode command-line tools
    curl -fsSL https://download.developer.apple.com/Developer_Tools/Command_Line_Tools_for_Xcode_13.2/Command_Line_Tools_for_Xcode_13.2.dmg -o /tmp/xcode-cli.dmg && \
    apt install -y --no-install-recommends hfsplus && \
    mkdir -p /tmp/xcode-cli && \
    mount -t hfsplus /tmp/xcode-cli.dmg /tmp/xcode-cli && \
    cp -R /tmp/xcode-cli/Command\ Line\ Tools /usr/local/ && \
    umount /tmp/xcode-cli && \
    rm -rf /tmp/xcode-cli.dmg /tmp/xcode-cli && \
    # Upgrade pip
    pip install --upgrade pip && \
    # Install Python dependencies
    pip install --no-cache-dir -r requirements.txt && \
    # Clean up
    rm -rf /var/lib/apt/lists/*

#CMD ["bash", "-c", "sleep infinity"]
#CMD ["bash", "-c", "streamlit run tracker.py"]
CMD ["bash", "-c", "streamlit run ocrmac.py"]
