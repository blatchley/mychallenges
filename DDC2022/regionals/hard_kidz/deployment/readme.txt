
docker build -t linearkidz .
docker run -p 13333:9999 -d --restart always --name linearkidz linearkidz