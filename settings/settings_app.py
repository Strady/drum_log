import pydantic


class AppSettings(pydantic.BaseSettings):
    app_port: int = 8000
    app_host: str = "0.0.0.0"
    jwt_secret: str
    jwt_ttl: int = 600
    api_key_header: str = 'X-API-Key'
    api_key: str
    images_dir: str = 'pictures'


