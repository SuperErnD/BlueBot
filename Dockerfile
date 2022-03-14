FROM python

COPY . ./
WORKDIR ./

RUN apt install libffi-dev
RUN apt install python3.10-dev
RUN pip install -r requirements.txt
RUN python main.py
ENV        SHELL=/bin/bash
ENTRYPOINT ["python", "main.py"]
CMD        ["python", "main.py"]

