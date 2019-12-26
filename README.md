# AWS 各種 ログを Elasticsearch Service 6.8 に取り込む Lambda Function (Python 3.8)

こちらは、

 - **[ALB/CLBのアクセスログをElasticsearch Service (6.0/6.2) に取り込むメモ](https://qiita.com/hmatsu47/items/826b00ff008d4e3edecf)**
 - **[CloudFrontのアクセスログをElasticsearch Service (6.0/6.2) に取り込むメモ（手抜き編）](https://qiita.com/hmatsu47/items/552ec1e4bc8e43051d9e)**
 - **[TABLE形式のAurora（MySQL互換）スロークエリログをElasticsearch Service (6.0/6.2) に取り込みS3に保存するメモ](https://qiita.com/hmatsu47/items/8c92b1a43fd412c054cf)**
 - **[Elasticsearch Service (6.0/6.2) に取り込んだログ（INDEX）をCuratorで削除するメモ](https://qiita.com/hmatsu47/items/e4b8a5bd44de0bee1682)**

の Lambda Function の Script を

 - Python 3.8 対応
 - Elasticsearch Service 6.8 対応

にするものです。

詳細は↑の記事を参照してください。

各 Lambda Function 用 zip file の作成方法は、以下をご覧ください。

※EC2 Amazon Linux 2 上での作成方法です。

 - **[ALB/CLB 用](alb_log_to_es/README.md)**
 - **[CloudFront 用](cf_log_to_es/README.md)**
 - **[Aurora MySQL 用](aurora_log_to_es/README.md)**
 - **[Curator 用](curator_es/README.md)**
