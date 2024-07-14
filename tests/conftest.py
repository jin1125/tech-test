from typing import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from api.config import settings
from api.database.db import Base, get_db
from api.main import app


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator:
    """
    テストのセットアップを行うフィクスチャ

    - テスト用のテーブルをセットアップ
        - テーブルを削除
        - テーブルを作成
    - テスト用の非同期データベースセッションでオーバーライド
    - テスト用の非同期HTTPクライアントを提供
    - テスト用のテーブルをリセット
        - テーブルを削除

    Yields:
    - 非同期HTTPクライアント
    """
    async_test_engine: AsyncEngine = create_async_engine(
        settings.get_test_async_url(),
        echo=settings.test_db_echo,
    )
    async_test_session: sessionmaker = sessionmaker(  # type: ignore
        bind=async_test_engine,
        class_=AsyncSession,
    )
    async with async_test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async def _get_test_db() -> AsyncGenerator:
        async with async_test_session() as session:
            yield session
            await session.commit()

    app.dependency_overrides[get_db] = _get_test_db  # type:ignore

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    async with async_test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
