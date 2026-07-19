FROM python:3.12-slim

WORKDIR /app

RUN pip install \
        aidge-core \
        aidge-backend-cpu \
        aidge-learning \
        aidge-export-cpp \
        aidge-onnx \
        aidge-quantization \
        fastapi \
        uvicorn \
        python-multipart

COPY app /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]