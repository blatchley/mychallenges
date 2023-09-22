
docker build -t fromage .
docker run -p 13337s:9999 -d --restart always --name fromage fromage