# Fibre From Address

このプロジェクトは、住所からファイバータイプを検索するためのFlaskアプリケーションです。

物件に関する検索ワードと部屋番号を入力すると、Seleniumを使用してフレッツ光提供エリア検索サイトからその住所のファイバータイプを判定します。

[English Version](README.md)

## 必要な環境

- Python 3.10
- Docker
- Docker Compose
- (オプション) Kubernetes

## セットアップ (docker)

### 1. Docker ComposeでSeleniumを起動

```sh
$ docker-compose up -d
```

## 2. セットアップ (Kubernetes)

```sh
$ kubectl apply -f deploy.yaml
$ kubectl apply -f service.yaml
$ kubectl apply -f ingress.yaml
```

## 使用方法

### 2. エンドポイント

- `POST /api/search?address=<建物検索ワード>&roomNumber=<部屋番号>`: 住所と部屋番号を指定してファイバータイプを検索します。

### 3. フロントエンド

ブラウザで `http://localhost:5000` にアクセスし、住所と部屋番号を入力して検索します。

![alt text](imgs/image.png)

## 開発

### 1. Dockerコンテナの実行

```sh
make docker-run
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。