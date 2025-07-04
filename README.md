# Snapshotter MCP Server

This is the MCP (Multi-Chain Protocol) server for the Snapshotter Core project.

## Setup

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd snapshotter-mcp-server
    ```

2.  **Install dependencies using Poetry:**

    If you don't have Poetry installed, follow the instructions [here](https://python-poetry.org/docs/#installation).

    ```bash
    poetry install
    ```

## Running the Application

To start the server, use Uvicorn:

```bash
poetry run python -m main
```

## Running Tests

To run the tests, use Pytest:

```bash
poetry run pytest
```
