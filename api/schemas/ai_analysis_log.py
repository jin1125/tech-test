from pydantic import Field

from api.schemas.base import BaseSchema


class SaveAiAnalysisLogIn(BaseSchema):
    """
    AIアナリティクスログ保存リクエストスキーマ

    - AIアナリティクスログを保存するリクエストのスキーマを定義

    Attributes:
    - image_path: 画像ファイルパスのフィールド
    """

    image_path: str = Field(
        default=...,
        description="画像ファイルパス",
        examples=["/image/d03f1d36ca69348c51aa/c413eac329e1c0d03/test.jpg"],
    )


class EstimatedData(BaseSchema):
    """
    予測データスキーマ

    Attributes:
    - class_: クラスのフィールド
    - confidence: 信頼度のフィールド
    """

    class_: int | None = Field(
        default=None,
        description="クラス",
        examples=[3],
    )
    confidence: float | None = Field(
        default=None,
        description="信頼度",
        examples=[0.8683],
    )


class SaveAiAnalysisLogOut(BaseSchema):
    """
    AIアナリティクスログ保存レスポンススキーマ

    - 保存したAIアナリティクスログをレスポンスするスキーマを定義

    Attributes:
    - success: リクエスト成功かのフィールド
    - message: メッセージのフィールド
    - estimated_data: 予測データのフィールド
    """

    success: bool = Field(
        default=False,
        description="リクエスト成功か",
        examples=[True],
    )
    message: str | None = Field(
        default=None,
        description="メッセージ",
        examples=["success"],
    )
    estimated_data: EstimatedData | dict = Field(
        default=...,
        description="予測データ",
    )
