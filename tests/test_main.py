"""Tests for the main FastAPI application."""

import pytest
from fastapi.testclient import TestClient

from app.main import app, items

client = TestClient(app)

INITIAL_ITEMS = [
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


@pytest.fixture(autouse=True)
def reset_items():
    """Reset the items list to its initial state before each test."""
    items.clear()
    items.extend([item.copy() for item in INITIAL_ITEMS])
    yield
    items.clear()
    items.extend([item.copy() for item in INITIAL_ITEMS])


def test_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to FastAPI GitOps Starter!"}


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "fastapi-gitops-starter"


def test_list_items():
    """Test the list items endpoint."""
    response = client.get("/api/items")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 5
    assert data["items"][0]["id"] == 1
    assert data["items"][0]["name"] == "Learn Spanish"


def test_get_item():
    """Test the get item endpoint."""
    response = client.get("/api/items/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Learn Spanish"


def test_get_item_not_found():
    """Test the get item endpoint with a non-existent item."""
    response = client.get("/api/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item 999 not found"


def test_delete_item():
    """Test the delete item endpoint."""
    response = client.delete("/api/items/1")
    assert response.status_code == 200
    data = response.json()
    assert data["deleted"] is True
    assert data["id"] == 1

    # Verify the item is actually gone
    response = client.get("/api/items/1")
    assert response.status_code == 404


def test_delete_item_not_found():
    """Test the delete item endpoint with a non-existent item."""
    response = client.delete("/api/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item 999 not found"


def test_search_items():
    """Test the search items endpoint."""
    response = client.get("/api/items/search?name=learn")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 2
    names = [item["name"] for item in data["items"]]
    assert "Learn Spanish" in names
    assert "Learn to cook" in names


def test_search_items_no_results():
    """Test the search items endpoint with no matching results."""
    response = client.get("/api/items/search?name=xyz_not_existing")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []