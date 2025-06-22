import os
import uuid
import pytest
from time import sleep
from fastapi.testclient import TestClient

# Import your FastAPI app and functions from your module.
# Adjust the import if your file is named differently (e.g., main.py)
from api.server_api import app, connect_to_databases, save_to_sql_function

# --- Dummy Database Handlers ---
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class DummyCursor:
    def __init__(self):
        self.last_query = ""

    def execute(self, query):
        self.last_query = query
        # Return self so that fetchone() can be called
        return self

    def fetchone(self):
        # Return a dummy count, for example
        return [42]

    def fetchall(self):
        return []  # No URLs in the dummy SQL DB

class DummySQLDB:
    def __init__(self):
        self.insert_calls = []  # record calls to InsertIntoIDxURL
        self.connected = False
        self.cursor = DummyCursor()

    def InsertIntoIDxURL(self, df):
        self.insert_calls.append(df)

    def ConnectToAzureSQL(self, pwd):
        self.connected = True

    def CloseConnection(self):
        pass

class DummyDB:
    def __init__(self):
        self.added_elements = []
        self.push_called = False

    def add_element(self, key, value):
        self.added_elements.append((key, value))

    def push_to_DB(self):
        self.push_called = True

    def FindTotalDocuments(self):
        return [10]

    def CloseConnection(self):
        pass

# --- Override the Database Connection Function ---
def dummy_connect_to_databases(app):
    """A dummy version of connect_to_databases that sets app.state with dummy db objects."""
    app.state.db = DummyDB()
    app.state.SQL_db = DummySQLDB()
    return True

# --- Pytest Fixture to Override Real DB Connections and Sleep ---
@pytest.fixture(autouse=True)
def override_dependencies(monkeypatch):
    # Override the connect_to_databases function used in your app
    monkeypatch.setattr("api.server_api.connect_to_databases", dummy_connect_to_databases)
    # Also override sleep so that tests do not actually wait
    monkeypatch.setattr("time.sleep", lambda x: None)
    # Ensure that our dummy connections are set on app.state
    dummy_connect_to_databases(app)
    yield

# Create a TestClient for the app.
client = TestClient(app)

# --- Tests for Endpoints and Functions ---
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_save_html_to_cosmosdb():
    payload = {
        "url": "https://example.com",
        "original_text": "Some HTML content",
        "internal_link": ["https://example.com/page1"],
        "language": "en"
    }
    response = client.post("/save_html_to_cosmosdb", json=payload)
    assert response.status_code == 200
    data = response.json()
    # The response returns a dict with one key whose value is "done"
    for value in data.values():
        assert value == "done"
    # Check that the dummy SQL DB's InsertIntoIDxURL was called
    assert len(app.state.SQL_db.insert_calls) > 0
    # Check that dummy DB pushed data
    assert app.state.db.push_called is True

def test_save_pdf_to_cosmosdb():
    payload = {
        "url": "https://example.com/pdf",
        "original_text": "PDF content",
        "language": "en"
    }
    response = client.post("/save_pdf_to_cosmosdb", json=payload)
    assert response.status_code == 200
    data = response.json()
    for value in data.values():
        assert value == "done"
    # Verify that the dummy SQL DB and DB were used.
    assert len(app.state.SQL_db.insert_calls) > 0
    assert app.state.db.push_called is True

def test_save_to_sql():
    # Ensure that the dummy SQL DB returns no URLs so that all passed URLs are new.
    app.state.SQL_db.cursor.fetchall = lambda: []
    payload = {
        "urls": ["https://example.com", "https://example.com/page1"]
    }
    response = client.post("/save_to_sql", json=payload)
    assert response.status_code == 200
    data = response.json()
    for value in data.values():
        assert value == "done"

def test_get_progress():
    # Prepare the dummy methods to return fixed values:
    app.state.db.FindTotalDocuments = lambda: [10]
    # Overriding execute so that fetchone() returns [42]
    app.state.SQL_db.cursor.execute = lambda q: type("Dummy", (), {"fetchone": lambda self: [42]})()
    response = client.get("/get_progress")
    assert response.status_code == 200
    # The endpoint returns a tuple (elementsIndb, elementsInSQL) which is converted to JSON as a list.
    data = response.json()
    assert data == [10, 42]
