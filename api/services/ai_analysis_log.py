import logging
from datetime import datetime

import httpx
from fastapi import status
from httpx import Response
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.dml import ReturningInsert

from api.config import settings
from api.models.ai_analysis_log import AiAnalysisLog
from api.schemas.ai_analysis_log import EstimatedData, SaveAiAnalysisLogOut

logger: logging.Logger = logging.getLogger(__name__)


async def create_ai_analysis_log(
    image_path: str,
    db: AsyncSession,
) -> SaveAiAnalysisLogOut | None:
    """
    AIアナリティクスログを保存

    Args:
    - image_path: 画像ファイルパス
    - db: 非同期のDBセッション

    Returns:
    - 保存したAIアナリティクスログ
    """
    error_response_dict: dict = {
        "success": False,
        "message": "Error:E50012",
        "estimated_data": {},
    }

    async with httpx.AsyncClient() as client:
        try:
            logger.info(
                {
                    "action": "save",
                    "status": "run",
                    "image_path": image_path,
                }
            )

            request_timestamp: datetime = datetime.now()
            response: Response = await client.post(
                f"{settings.mock_up_domain}/mock-up",
                json={"image_path": image_path},
            )
            response_timestamp: datetime = datetime.now()
            response.raise_for_status()

            response_dict: dict = response.json()
            result: SaveAiAnalysisLogOut = await _save_log_to_db(
                db,
                image_path,
                response_dict,
                request_timestamp,
                response_timestamp,
            )

            logger.info(
                {
                    "action": "save",
                    "status": "success",
                    "image_path": image_path,
                }
            )

            return result
        except httpx.HTTPStatusError as exc:
            logger.error(
                {
                    "action": "save",
                    "status": "error",
                    "image_path": image_path,
                    "status_code": exc.response.status_code,
                    "detail": exc.response.text,
                }
            )

            return await _save_log_to_db(
                db,
                image_path,
                error_response_dict,
                request_timestamp,
                response_timestamp,
            )
        except httpx.RequestError:
            logger.error(
                {
                    "action": "save",
                    "status": "error",
                    "image_path": image_path,
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                }
            )

            return await _save_log_to_db(
                db,
                image_path,
                error_response_dict,
                request_timestamp,
                response_timestamp,
            )


async def _save_log_to_db(
    db: AsyncSession,
    image_path: str,
    response_dict: dict,
    request_timestamp: datetime,
    response_timestamp: datetime,
) -> SaveAiAnalysisLogOut:
    """
    AIアナリティクスログをデータベースに保存

    Args:
    - db: 非同期のDBセッション
    - image_path: 画像ファイルパス
    - response_dict: レスポンスの辞書
    - request_timestamp: リクエストのタイムスタンプ
    - response_timestamp: レスポンスのタイムスタンプ

    Returns:
    - 保存したAIアナリティクスログ
    """
    success: bool = response_dict.get("success", False)
    message: str = response_dict.get(
        "message",
        response_dict.get("detail", ""),
    )
    estimated_data: dict = response_dict.get("estimated_data", {})
    class_: int | None = estimated_data.get("class_")
    confidence: float | None = estimated_data.get("confidence")

    stmt: ReturningInsert = (
        insert(AiAnalysisLog)
        .values(
            image_path=image_path,
            success=success,
            message=message,
            class_=class_,
            confidence=confidence,
            request_timestamp=request_timestamp,
            response_timestamp=response_timestamp,
        )
        .returning(AiAnalysisLog)
    )
    result: AiAnalysisLog = await db.scalar(stmt)

    return SaveAiAnalysisLogOut(
        success=result.success,
        message=result.message,
        estimated_data=(
            EstimatedData(
                class_=result.class_,
                confidence=result.confidence,
            )
            if estimated_data
            else {}
        ),
    )
