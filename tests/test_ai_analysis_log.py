import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_success_save_ai_analysis_log(
    async_client: AsyncClient,
) -> None:
    """AIアナリティクスログを保存APIへのリクエストが成功時のテスト"""
    processable_entity: str = (
        "/image/d03f1d36ca69348c51aa/c413eac329e1c0d03/test.jpg"
    )

    response = await async_client.post(
        "/save-ai-analysis-log",
        json={
            "image_path": processable_entity,
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    response_json = response.json()
    assert response_json["success"] is True
    assert response_json["message"] == "success"
    assert response_json["estimated_data"]["class_"] == 3
    assert response_json["estimated_data"]["confidence"] == 0.8683


@pytest.mark.asyncio
async def test_failed_save_ai_analysis_log(
    async_client: AsyncClient,
) -> None:
    """AIアナリティクスログを保存APIへのリクエストが失敗時のテスト"""
    unprocessable_entity: int = 999

    response = await async_client.post(
        "/save-ai-analysis-log",
        json={
            "image_path": unprocessable_entity,
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
