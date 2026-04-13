# Tradier API Python SDK

A high-performance, strictly-typed, and asynchronous Python SDK for the [Tradier API](https://docs.tradier.com/).

This SDK is built using `aiohttp` for robust network connection pooling, and `msgspec` for ultra-fast, strictly-typed JSON deserialization and data validation.

## Installation

Ensure you have the required dependencies installed (ideally in a Python virtual environment). Since this project is available on GitHub, you can install it directly via pip:

```bash
pip install git+https://github.com/Varun-Chinthoju/tradier_api.git
```

## Authentication

The SDK automatically resolves your Tradier API token. It evaluates them securely in the following order:

1. **Environment Variable:** Set `TRADIER_API_TOKEN` in your system environment.
2. **System Keyring:** The SDK implements the Python `keyring` module to attempt fetching the token cleanly.
3. **Configuration File:** A secure fallback localized config file generated at `~/.config/tradier_api/config.ini` (strict `600` permissions used).

To comfortably bootstrap and save a token globally on your machine, the SDK provides an interactive CLI. Running this avoids hard-coding keys completely.

```bash
# Interactively set the API token (stored to system keyring)
tradier auth

# Or optionally force it to be stored in the local config.ini instead
tradier auth --no-keyring
```

You can also leverage the internal module programmatically if required:

```python
from tradier_api.auth import set_api_token

set_api_token("YOUR_TOKEN") # Keyring by default
```

## Usage

### Command Line Interface

The SDK bundles a top-level `tradier` CLI that acts as a fast utility map to internal endpoints.

```bash
# Obtain quote data for various symbols JSON-encoded
tradier get_quotes --symbols NVDA,MSFT --greeks=true --include_lot_size=true

# Switch context natively to sandbox endpoints
tradier --sandbox get_quotes --symbols AAPL
```

### Python API

Because performance is paramount, this SDK uses `aiohttp` and functions within an `async` Python event loop. You handle the `TradierClient` lifecycle utilizing an `async with` block, which establishes a reusable `aiohttp.ClientSession` internally to maximize the benefits of connection pooling.

#### Fetching Market Quotes

```python
import asyncio
from tradier_api import TradierClient, get_quotes

async def main():
    # Set sandbox=True to direct traffic toward https://sandbox.tradier.com
    # Set sandbox=False (default) to direct traffic to https://api.tradier.com
    # The API Token is automatically resolved by the Auth engine if not explicitly provided
    client = TradierClient(sandbox=True)
    
    # Use context manager to open the HTTP connection safely 
    async with client:
        # get_quotes immediately converts JSON payload into strongly-typed `Quote` objects
        quotes = await get_quotes(
            client, 
            symbols=["AAPL", "SPY"], 
            greeks=False, 
            include_lot_size=False
        )
        
        for q in quotes:
            print(f"Symbol: {q.symbol} | Last: {q.last} | Change: {q.change_percentage}%")

if __name__ == "__main__":
    asyncio.run(main())
```

## Testing

The SDK includes a comprehensive asynchronous test suite built using `pytest` and `aioresponses` to mock the remote API. To run the test suite and formally verify that the models appropriately deserialize endpoints smoothly dynamically, simply invoke it from the command line:

```bash
# If using poetry
poetry run pytest test_market_data.py

# Alternatively, explicitly running pytest natively inside the .venv directory
.venv/bin/pytest test_market_data.py
```

## Module Structure

- **`tradier_api.client.TradierClient`**: The core API asynchronous client handling the session and headers.
- **`tradier_api.market_data`**: The API wrappers mapping cleanly to endpoint resources (e.g., `get_quotes`).
- **`tradier_api.models`**: Structured payload schemas implementing `msgspec.Struct` defining explicit limits to what data looks like, and providing lightning-quick decoders mapping directly to object properties.
- **`tradier_api.exceptions`**: Clean exception mappings (e.g., `AuthenticationError`, `RateLimitError`).

## API References & Architecture Scope
The following external resources serve as the architectural base definition defining shapes modeled internally in this codebase module:

- Main Help/Documentation Layer: [Tradier Architecture Hub](https://docs.tradier.com/)
- Model: [Brokerage API - Markets (Get Quotes)](https://docs.tradier.com/reference/brokerage-api-markets-get-quotes.md)

*Currently this SDK supports endpoints mapped as requested up to Step 1 boundaries.*
