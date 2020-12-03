FROM python
WORKDIR /news_crawl
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["/bin/bash"]