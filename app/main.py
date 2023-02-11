""" Main page of services """

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from route import auth, images, account, umkm, simulasi, generate_file, core, sjh
app = FastAPI()


@app.get('/', include_in_schema=False)
async def redirect():
    """ a function for redirect / into /docs """
    return RedirectResponse('/docs')

app.include_router(router=auth.app, prefix="/auth", tags=["Auth"])
app.include_router(router=generate_file.app, prefix="/generate", tags=["Generate"])
app.include_router(router=sjh.app, prefix="/sjh", tags=["sjh"])
app.include_router(router=images.app, prefix="/util", tags=["Util"])
app.include_router(router=account.app, prefix="/account", tags=["Account"])
app.include_router(router=core.app, prefix="/core", tags=["Core"])
app.include_router(router=umkm.app, prefix="/umkm", tags=["UMKM"])
app.include_router(router=simulasi.app, prefix="/simulasi", tags=["Simulasi"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
