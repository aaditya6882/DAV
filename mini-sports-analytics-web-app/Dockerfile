# Run the Flask dashboard in a small, production-ready Python container.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MPLCONFIGDIR=/tmp/matplotlib

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# The application creates processed data and chart images at runtime.
RUN useradd --create-home appuser \
    && mkdir -p data/processed static/images/plots /tmp/matplotlib \
    && chown -R appuser:appuser /app /tmp/matplotlib

USER appuser

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "--timeout", "120", "app:create_app()"]
