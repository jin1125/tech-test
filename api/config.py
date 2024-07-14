from functools import lru_cache

import sqlalchemy
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    """
    環境変数を.envから読み込む

    - .envファイルに定義されている環境変数を読み込む
    - 環境変数が定義されていない場合、クラス変数が使用される

    Attributes:
    - app_title: アプリのタイトル
    - cors_credentials: Cookieの共有を許可するか
    - cors_headers: クロスオリジンリクエストに対応するHTTPリクエストヘッダ
    - cors_methods: クロスオリジンリクエストを許可するHTTPメソッド
    - cors_origins: クロスオリジンリクエストを許可するオリジン
    - db_echo: SQLのログを出力するか
    - mock_up_domain: モックアップのドメイン
    - docs_url: SwaggerUIのURL
    - postgres_alembic_host: PostgreSQLのalembicでのホスト名
    - postgres_db: PostgreSQLのデータベース名
    - postgres_host: PostgreSQLのホスト名
    - postgres_password: PostgreSQLのパスワード
    - postgres_port: PostgreSQLのポート番号
    - postgres_user: PostgreSQLのユーザ名
    - redoc_url: ReDocのURL
    - test_db_echo: テスト時にSQLのログを出力するか
    - test_postgres_host: テスト用のPostgreSQLのホスト名
    - test_postgres_port: テスト用のPostgreSQLのポート番号

    - model_config: クラスの設定を定義
    """

    app_title: str = "技術テスト"
    cors_credentials: bool = True
    cors_headers: list[str] = ["*"]
    cors_methods: list[str] = ["*"]
    cors_origins: list[str] = ["*"]
    db_echo: bool = False
    docs_url: str | None = "/docs"
    mock_up_domain: str = "http://127.0.0.1:8000"
    postgres_alembic_host: str = "localhost"
    postgres_database: str = "postgres"
    postgres_host: str = "db"
    postgres_password: str = "postgres"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    redoc_url: str | None = "/redoc"
    test_db_echo: bool = True
    test_postgres_host: str = "test_db"
    test_postgres_port: int = 5432

    def get_async_url(self) -> URL:
        """
        PostgreSQLへの非同期接続情報(URL)を取得

        - URLを生成

        Returns:
        - PostgreSQLへの非同期接続情報(URL)
        """
        return sqlalchemy.engine.url.URL.create(
            drivername="postgresql+asyncpg",
            database=self.postgres_database,
            host=self.postgres_host,
            port=5432,
            username=self.postgres_user,
            password=self.postgres_password,
        )

    def get_test_async_url(self) -> URL:
        """
        テスト用のPostgreSQLへの非同期接続情報(URL)を取得

        - URLを生成

        Returns:
        - テスト用のPostgreSQLへの非同期接続情報(URL)
        """
        return sqlalchemy.engine.url.URL.create(
            drivername="postgresql+asyncpg",
            database="test_db",
            host=self.test_postgres_host,
            port=5432,
            username="test_user",
            password="password",
        )

    model_config = SettingsConfigDict(
        extra="allow",
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> Settings:
    """
    環境変数もしくはクラス変数を取得

    - .envの環境変数もしくはSettingsクラス変数を取得する
    - lru_cacheデコレータによって、Settingsクラスは1度だけインスタンス化される

    Returns:
    - Settingsクラスのインスタンス
    """
    return Settings()


settings: Settings = get_settings()
