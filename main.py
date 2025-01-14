from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes.user import router as user_router
from routes.echo import router as echo_router


app = FastAPI()

@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")

app.include_router(user_router)
app.include_router(echo_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)