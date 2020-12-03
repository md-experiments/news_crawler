FROM python
WORKDIR /news
RUN pip install -r requirements.txt
COPY . .
CMD ["/bin/bash"]