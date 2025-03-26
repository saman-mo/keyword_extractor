from pydantic import BaseSettings, BaseModel
from typing import Optional, Dict


class EnvSettings(BaseSettings):
    TW_ENV: str
    JOB2SKILLS_SERVICE_URL: str 
    USERS: Dict[str, str] = {"admin": "Thom/.8809", "guest": "Kl0p.124"}
    TOP_N_SKILLS: int = 100
    SENTRY_DSN: Optional[str]


env_settings = EnvSettings()


class Settings(BaseModel):
    authjwt_secret_key: str = "fFUInf6simHtYx9JErpAoJIRjKjKGTBd"


class LoginRequest(BaseModel):
    username: str
    password: str
