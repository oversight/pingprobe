FROM python:3.8
ENV OS_CONFIG_FOLDER /data/config/pingprobe/
ADD . /code
WORKDIR /code
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "pingprobe.py"]
