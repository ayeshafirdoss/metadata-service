from fastapi import FastAPI
from app.api import datasets, search, lineage

app = FastAPI(
    title="Metadata Service",
    version="2.0.0"
)

app.include_router(datasets.router, prefix="/api/v2")
app.include_router(search.router, prefix="/api/v2")
app.include_router(lineage.router, prefix="/api/v2")


@app.get("/")
def health():
    return {"status": "ok"}
