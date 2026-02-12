import os

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(
    title="FastAPI GitOps Starter",
    description="A starter template for learning GitOps with FastAPI",
    version="1.0.0",
    root_path=os.getenv("ROOT_PATH", "/GitOps-Starter"),
)

items = [
    {
        "id": 1,
        "name": "Learn Spanish",
        "description": "Complete Duolingo course and reach B1 level by December",
    },
    {
        "id": 2,
        "name": "Run a marathon",
        "description": "Train for and complete a full marathon by October",
    },
    {
        "id": 3,
        "name": "Read 24 books",
        "description": "Read at least 2 books per month across different genres",
    },
    {
        "id": 4,
        "name": "Learn to cook",
        "description": "Master 10 new recipes from different cuisines",
    },
    {
        "id": 5,
        "name": "Save for travel",
        "description": "Save 20% of monthly income for a travel fund",
    },
]


@app.get("/")
async def root():
    """Root endpoint returning a welcome message."""
    return {"message": "Welcome to FastAPI GitOps Starter!"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return JSONResponse(
        status_code=200,
        content={"status": "healthy", "service": "fastapi-gitops-starter"},
    )


@app.get("/api/items")
async def list_items():
    """Endpoint to list all personal goal items."""
    return {"items": items}


@app.get("/api/items/search")
async def search_items(name: str):
    """Search items by name (case-insensitive)."""
    results = [item for item in items if name.lower() in item["name"].lower()]
    return {"items": results}


@app.get("/api/items/{item_id}")
async def get_item(item_id: int):
    """Endpoint to get a specific item by ID."""
    item = next((item for item in items if item["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return item


@app.delete("/api/items/{item_id}")
async def delete_item(item_id: int):
    """Delete a specific item by ID."""
    item = next((item for item in items if item["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    items.remove(item)
    return {"deleted": True, "id": item_id}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)