FROM public.ecr.aws/datamindedacademy/capstone:v3.4.1-hadoop-3.3.6-v1

USER 0
RUN useradd -ms /bin/bash partyanimal
USER partyanimal
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY spark_job.py .
COPY utils.py .

ENTRYPOINT ["python3"]
CMD [ "spark_job.py" ]

