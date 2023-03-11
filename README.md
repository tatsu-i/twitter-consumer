# Twitter consumer

## Logstashの設定ファイル生成

```bash
$ docker-compose run --entrypoint python worker /app/generate.py > docker/logstash/logstash.conf
```

## Dockerのビルドと実行
```
$ docker-compose up -d --build
```

## チャットボットの作成
* create vector database
```
docker-compose exec chatbot python /app/ingest.py -u 'user1,user2,user3'
```

* run chatbot
```
docker-compose exec chatbot python /app/chat.py
You: ChatGPTの活用方法について
```
