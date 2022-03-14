FROM python

COPY . ./
WORKDIR ./

RUN apt update
RUN apt install libpython3-dev
RUN pip install -r requirements.txt
RUN python main.py
ENV        SHELL=/bin/bash
ENTRYPOINT ["python", "main.py"]
CMD        ["python", "main.py"]

