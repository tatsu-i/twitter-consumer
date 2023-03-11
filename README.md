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
* 埋め込みデータベースの作成
ユーザIDをカンマ区切りで指定してツイート内容をベクトル化します。
```
docker-compose exec chatbot python /app/ingest.py -u 'user1,user2,user3'
```

* チャットボットの実行
以下のように質問を行います。ツイート内容を引用して質問に答えてくれます。
```
docker-compose exec chatbot python /app/chat.py
You: ChatGPTの活用方法について
```
