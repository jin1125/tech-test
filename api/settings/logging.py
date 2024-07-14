import logging


def setup_logging() -> None:
    """
    ロギングの設定

    - 出力するログの設定を行う
    """
    logging.basicConfig(
        filename="api/logs/api.log",
        format="[%(levelname)s] %(asctime)s | %(message)s",
        level=logging.INFO,
    )
