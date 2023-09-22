
docker build -t pydes .
docker run -p 13337s:9999 -d --restart always --name pydes pydes