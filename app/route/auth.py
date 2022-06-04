from fastapi import APIRouter

app = APIRouter()

@app.get('/auth')
def auth():
    return "test auth"