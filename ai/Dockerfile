FROM python:3.7-slim

COPY ./ai/requirements.txt requirements.txt

RUN apt update && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

#CMD ["bash", "-c", "sleep infinity"]
#CMD ["bash", "-c", "streamlit run tracker.py"]
CMD ["bash", "-c", "streamlit run ocrmac.py"]
