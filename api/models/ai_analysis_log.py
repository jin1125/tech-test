from sqlalchemy import DECIMAL, Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from api.database.db import Base


class AiAnalysisLog(Base):
    """
    AiAnalysisLogモデル

    - DBテーブルを表すSQLAlchemyのモデルを定義

    Attributes:
    - __tablename__: テーブル名を定義

    - id: IDのカラム
    - image_path: 画像ファイルパスのカラム
    - success: リクエスト成功かのカラム
    - message: メッセージのカラム
    - class_: クラスのカラム
    - confidence: 信頼度のカラム
    - request_timestamp: リクエストタイムスタンプのカラム
    - response_timestamp: レスポンスタイムスタンプのカラム
    """

    __tablename__ = "ai_analysis_log"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="ID",
    )
    image_path: Mapped[str | None] = mapped_column(
        String(255),
        default=None,
        comment="画像ファイルパス",
    )
    success: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        comment="リクエスト成功か",
    )
    message: Mapped[str | None] = mapped_column(
        String(255),
        default=None,
        comment="メッセージ",
    )
    class_: Mapped[int | None] = mapped_column(
        Integer,
        default=None,
        comment="クラス",
    )
    confidence: Mapped[float | None] = mapped_column(
        DECIMAL(5, 4),
        default=None,
        comment="信頼度",
    )
    request_timestamp: Mapped[str | None] = mapped_column(
        DateTime,
        default=None,
        comment="リクエストタイムスタンプ",
    )
    response_timestamp: Mapped[str | None] = mapped_column(
        DateTime,
        default=None,
        comment="レスポンスタイムスタンプ",
    )
