from fastapi import FastAPI

app = FastAPI(
    title="AIPOS API",
    description="AI Personal Operating System Backend",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {
        "application": "AIPOS",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }