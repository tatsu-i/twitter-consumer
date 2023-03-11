import os
import json
import click
import pickle
import tiktoken
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.docstore.document import Document
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

@click.command()
@click.option("-u", "--user_list", required=True, help="Comma-separated list of users")
@click.option("-e", "--es_host", default="elasticsearch:9200", help="Elasticsearch host and port")
@click.option('--output-file', '-o', default='/data/vectorstore.pkl', help='Output file name')
@click.option('--dry-run', '-d', is_flag=True, help='If set, does not actually add documents to vectorstore')
def ingest(user_list, es_host, output_file, dry_run):
    # Elasticsearchに接続する
    es = Elasticsearch(hosts=[es_host])

    # ユーザーリスト
    user_list = [user.strip() for user in user_list.split(",")]
    #user_list = ["umiyuki_ai", "npaka123", "izutorishima", "Yamkaz", "odashi_t", "dll7", "mattn_jp", "odashi_t"]

    # 現在の年月を取得する
    now = datetime.now()
    year_month = now.strftime("%Y-%m")

    # インデックス名を作成する
    index_name = "twitter-" + year_month
    # Elasticsearchから検索する
    s = Search(using=es, index=index_name)
    #q = Q("bool",
    #      should=[Q("match", user=user) for user in user_list]
    #      )
    #s = s.query(q)
    #response = s.execute()
    s = s.query("bool", should=[{"match": {"user": user}} for user in user_list])
    s = s.params(scroll="10m")
    response = s.scan()

    raw_documents = []
    # ヒットしたドキュメントを表示する
    for hit in response:
        hit = hit.to_dict()
        metadata = {"source": json.dumps({"user": hit["user"] ,"timestamp": hit["@timestamp"], "source": hit["source"]}, ensure_ascii=False)}
        raw_documents.append(Document(page_content=hit["message"], metadata=metadata))

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=500,
    )
    documents = text_splitter.split_documents(raw_documents)
    print(f"load {len(documents)} documents")
    encoding = tiktoken.encoding_for_model("text-embedding-ada-002")
    text = ""
    for doc in documents:
        text += doc.page_content.replace("\n", " ")
    token_count = len(encoding.encode(text, allowed_special='all'))
    # https://openai.com/pricing
    print(f"use {token_count} token")
    print(f"price {token_count*0.0000004} USD")

    if dry_run:
        print("Dry run mode enabled. Exiting without adding documents to vectorstore.")
        return
    if os.path.exists(output_file):
        with open(output_file, "rb") as f:
            vectorstore = pickle.load(f)
            vectorstore.add_documents(documents)
    else:
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(documents, embeddings)

    # Save vectorstore
    with open(output_file, "wb") as f:
        pickle.dump(vectorstore, f)

if __name__ == "__main__":
    ingest()
