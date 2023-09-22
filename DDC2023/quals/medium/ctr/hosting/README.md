
## Handout: A URL and the following text
```
basic ctr
```

## Docker setup
```bash
docker build -t ctr1 .
docker run -p 8000:8000 --name ctr1_container ctr1

# http://127.0.0.1:8000/
```