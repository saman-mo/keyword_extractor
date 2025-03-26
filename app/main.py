import uvicorn
import json
from typing import Dict

from fastapi import FastAPI, Response, Header, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.config import env_settings, Settings, LoginRequest
from app.dependencies.model.keyword_exctractor import get_keyword_extractor
from app.exception_handlers import handle_internal_error
from app.keyword_extractor_data_types import KeywordExtractorPayload
from app.utils.ke_utils import sort_results

import logging
import sentry_sdk



logging.basicConfig(level=logging.INFO)


def create_app():
    app = FastAPI(
        exception_handlers={
            status.HTTP_500_INTERNAL_SERVER_ERROR: handle_internal_error
        }
    )
    sentry_sdk.init(env_settings.SENTRY_DSN)
    sentry_sdk.init(environment=env_settings.TW_ENV)
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"]
    )
    return app


app = create_app()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

@AuthJWT.load_config
def get_config():
    return Settings()

@app.get("/")
def home(request: Request):
    """Serve the login page dynamically"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/login")
def login(data: LoginRequest, Authorize: AuthJWT = Depends()):
    """Authenticate user and return JWT token"""
    username, password = data.username, data.password

    if env_settings.USERS.get(username) and env_settings.USERS.get(username) == password:
        access_token = Authorize.create_access_token(subject=username)
        return {"token": access_token}
    
    return JSONResponse(status_code=401, content={"message": "Invalid credentials"})


@app.post("/v1/keywords")
def handle_request(
        payload: KeywordExtractorPayload,
        Authorize: AuthJWT = Depends(),
        keyword_extractor=Depends(get_keyword_extractor)
        ):
    """Extract keywords (Protected route)"""
    Authorize.jwt_required()  # Require authentication
    current_user = Authorize.get_jwt_subject()
    res = keyword_extractor(payload)
    res = sort_results(res)
    return res


@app.get('/health')
def check_health():
    """Check if the dependent service are healthy"""
    return Response(status_code=200)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)