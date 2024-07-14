from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.database.db import get_db
from api.schemas.ai_analysis_log import (
    SaveAiAnalysisLogIn,
    SaveAiAnalysisLogOut,
)
from api.services.ai_analysis_log import create_ai_analysis_log

router: APIRouter = APIRouter(tags=["AIアナリティクスログ"])


@router.post(
    "/save-ai-analysis-log",
    status_code=status.HTTP_201_CREATED,
    response_model=SaveAiAnalysisLogOut,
    summary="AIアナリティクスログを保存",
)
async def save_ai_analysis_log(
    save_ai_analysis_log_in: SaveAiAnalysisLogIn,
    db: AsyncSession = Depends(get_db),
):
    """
    AIアナリティクスログを保存

    Args:
    - save_ai_analysis_log_in: AIアナリティクスログを保存するための情報
    - db: 非同期のDBセッション

    Returns:
    - 保存したAIアナリティクスログ
    """
    return await create_ai_analysis_log(save_ai_analysis_log_in.image_path, db)
