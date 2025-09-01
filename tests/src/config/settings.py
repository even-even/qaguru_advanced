import os

import dotenv

dotenv.load_dotenv()


class AppSettings:
    """Настройки приложения через os.getenv."""

    def __init__(self, env: str | None = None):
        self.env = env or os.getenv("ENV", "dev").lower()

    @property
    def base_url(self) -> str:
        """Возвращает базовый URL в зависимости от окружения."""
        env_mapping = {
            "dev": os.getenv("DEV_URL"),
            "stage": os.getenv("STAGE_URL"),
            "prod": os.getenv("PROD_URL"),
        }

        url = env_mapping.get(self.env)

        if url is None:
            # Fallback URL если переменная окружения не установлена
            return "http://0.0.0.0:8000"

        return url
