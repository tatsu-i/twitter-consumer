# Twitter consumer

## 環境変数の設定
テンプレートをコピーし必要なAPIキーを入力します。
```
$ cp env.template .env
$ vim .env
```

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
AI:
ChatGPTは、ユーザーの要望を直接ChatGPTに投げて結果を返すことができる。
また、企業が宿題系のコーディング試験を出す場合、Chatbot対策が必要になるかもしれない。
ChatGPTをAPIとして利用することもできる。ChatGPTをアドバイザーとして利用することもできる。
```
