FROM python:3.7

USER root

WORKDIR /KeckKeywordInterface

ADD . /KeckKeywordInterface
#RUN apt-get install -y git
#RUN git clone https://github.com/Terry071896/KeckKeywordInterface /KeckKeywordInterface
#RUN cd /KeckKeywordInterface
RUN pip install -r requirements.txt

EXPOSE 8050

WORKDIR /KeckKeywordInterface
CMD [ "python", "./index.py"]
