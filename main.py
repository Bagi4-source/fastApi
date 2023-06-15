import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

app = FastAPI()

WHITELISTED_IPS = ['194.58.109.219', '127.0.0.1']


@app.get("/")
async def root(request: Request):
    ip = str(request.client.host)
    if ip not in WHITELISTED_IPS:
        data = {
            'message': f'IP {ip} is not allowed to access this resource.'
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=data)

    # Proceed if IP is allowed
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
