from typing import Union
import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from imp import reload
from route import auth, images


app = FastAPI()


@app.get('/',include_in_schema=False)
async def redirect():
    return RedirectResponse('/docs')


app.include_router(router=auth.app, prefix="/auth", tags=["Auth"])
app.include_router(router=images.app, prefix="/image", tags=["Image"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)