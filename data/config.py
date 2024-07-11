from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    CHANNEL_ID: int
    BOT_TOKEN: str
    OWNER_ID: int

    RAPIDAPI_KEY: str

    @property
    def db_url_asyncpg(self):
        # postgresql+asyncpg://user:password@host:port/name
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def db_url_psycopg(self):
        # postgresql+psycopg://user:password@host:port/name
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
