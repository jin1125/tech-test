from api.schemas.mock_up import EstimatedData, MockUpOut


async def get_mock_up(image_path: str) -> MockUpOut:
    """
    モックアップをレスポンス

    Args:
    - image_path: 画像ファイルパス

    Returns:
    - モックアップ
    """
    return MockUpOut(
        success=True,
        message="success",
        estimated_data=EstimatedData(class_=3, confidence=0.8683),
    )
