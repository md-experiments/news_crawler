FROM continuumio/miniconda3
WORKDIR /news
RUN pip install -r requirements.txt
COPY . .
CMD ["/bin/bash"]