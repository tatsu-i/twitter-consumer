# Twitter consumer

## generate logstash config

```bash
$ pip install tweepy --upgrade
$ python generate.py > logstash/logstash.conf
```

## build and run
```
$ docker-compose up -d --build
```
