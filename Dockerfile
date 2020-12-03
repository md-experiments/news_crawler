FROM python
WORKDIR /news_crawl
COPY . .
RUN pip install -r requirements.txt
CMD ["/bin/bash"]