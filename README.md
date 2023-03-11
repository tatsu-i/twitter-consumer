# Twitter consumer

## generate logstash config

```bash
$ docker-compose run --entrypoint python worker /app/generate.py > docker/logstash/logstash.conf
```

## build and run
```
$ docker-compose up -d --build
```
