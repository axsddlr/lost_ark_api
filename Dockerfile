FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
LABEL maintainer="Andre Saddler <andrexsaddler@gmail.com>"

LABEL build_date="2021-07-20"
RUN pip install virtualenv

WORKDIR /api
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY . .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
