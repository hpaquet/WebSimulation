FROM python:3.7.4

COPY . /simulationapp

WORKDIR /simulationapp

RUN pip install -r requirements.txt

RUN python setup.py install

CMD [ "python", "./simulationapp/app.py" ]