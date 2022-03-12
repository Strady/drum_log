import pydantic


class AppSettings(pydantic.BaseSettings):
    app_port: int = 8000
    app_host: str = "0.0.0.0"
    jwt_secret: str
    jwt_ttl: int = 600


