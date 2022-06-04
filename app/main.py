from typing import Union
import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from route import auth


app = FastAPI()


@app.get('/',include_in_schema=False)
async def redirect():
    return RedirectResponse('/docs')


app.include_router(router=auth.app, prefix="/auth", tags=["Auth"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)