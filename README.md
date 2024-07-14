# 技術テスト

<img width="1465" alt="技術テスト" src="https://github.com/user-attachments/assets/26fc1c56-b2e3-45c1-8369-d3400d01ca79">

## 環境構築

- `.env.example`ファイルをコピーして`.env`ファイルを作成

- 必要に応じて`.env`の定義を変更

- Dockerコンテナを作成・起動

    ```commandline
    docker compose -f compose.yml -f compose.test.yml up -d
    ```

- `app`と`db`と`test_db`のコンテナが起動していることを確認

    ```commandline
    docker compose ps
    ```

- DBマイグレーションを実行

    ```commandline
    make db_upgrade
    ```

- APIドキュメントを表示
  
  http://localhost:8000/docs など
