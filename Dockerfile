FROM python:3.6

# install agavepy
RUN pip install --no-cache-dir agavepy

# add the python script to docker container
ADD hello.py /hello.py

# command to run the python script
CMD ["python", "/hello.py"]
