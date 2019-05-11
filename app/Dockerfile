FROM python:3.7-alpine
COPY . /app
RUN apk add --no-cache gcc libc-dev unixodbc-dev
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["flask"]
CMD ["run", "--host=0.0.0.0"]
