import yaml
from fastapi import Request, HTTPException
from starlette.responses import JSONResponse

WHITELIST_FILE = "token_whitelist.yaml"

with open(WHITELIST_FILE, "r", encoding="utf-8") as f:
    token_data = yaml.safe_load(f)

TOKEN_WHITELIST = set(token_data)


async def token_validation_middleware(request: Request, call_next):
    token = request.query_params.get("token")

    if not token or token not in TOKEN_WHITELIST:
        return JSONResponse(
            status_code=401,
            content={"code": 40100, "message": "invalid token"}
        )

    response = await call_next(request)
    return response
