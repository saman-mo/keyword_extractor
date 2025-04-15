from pydantic import BaseSettings, BaseModel
from typing import Optional, Dict


USERS = {"admin": "Thom/.8809", "guest1": "Kl0p.124", "guest2": "Kl0p.101", "guest3": "Kl0p.516", 
        "guest4": "Kl0p.071", "guest5": "Kl0p.888", "guest6": "Kl0p.001", "guest7": "Kl0p.452", 
        "guest8": "Kl0p.666", "guest9": "Kl0p.713", "guest10": "Kl0p.929", "guest11": "Kl0p.183", 
        "guest12": "Kl0p.446", "guest13": "Kl0p.789", "guest14": "Kl0p.000", "guest15": "Kl0p.111", 
        "guest16": "Kl0p.222", "guest17": "Kl0p.333", "guest18": "Kl0p.444", "guest19": "Kl0p.555", "guest20": "Kl0p.606"}

class EnvSettings(BaseSettings):
    TW_ENV: str
    JOB2SKILLS_SERVICE_URL: str 
    USERS: Dict[str, str] = USERS
    TOP_N_SKILLS: int = 100
    SENTRY_DSN: Optional[str]


env_settings = EnvSettings()


class Settings(BaseModel):
    authjwt_secret_key: str = "fFUInf6simHtYx9JErpAoJIRjKjKGTBd"


class LoginRequest(BaseModel):
    username: str
    password: str
