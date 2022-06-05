from pydantic import BaseSettings


class DatabaseSettings(BaseSettings):
    """Settings for database package"""

    echo = True
