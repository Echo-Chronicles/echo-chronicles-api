from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from routes.user import router as user_router
from routes.echo import router as echo_router

app = FastAPI(
    title="Echo Chronicles API",
    description="API for Echo Chronicles",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/", include_in_schema=False)
def read_root():
    return RedirectResponse(url="/docs")

app.include_router(user_router)
app.include_router(echo_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=2, timeout_keep_alive=240)