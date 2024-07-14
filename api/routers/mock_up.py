from fastapi import APIRouter

from api.schemas.mock_up import MockUpIn, MockUpOut
from api.services.mock_up import get_mock_up

router: APIRouter = APIRouter(tags=["モックアップ"])


@router.post(
    "/mock-up",
    response_model=MockUpOut,
    summary="モックアップ",
)
async def mock_up(mockup_in: MockUpIn):
    """
    モックアップをレスポンス

    Args:
    - mockup_in: モックアップを返すための情報

    Returns:
    - モックアップ
    """
    return await get_mock_up(mockup_in.image_path)
