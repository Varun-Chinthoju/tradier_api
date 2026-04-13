import pytest
from aioresponses import aioresponses
from tradier_api import TradierClient, get_quotes

@pytest.mark.asyncio
async def test_get_quotes_multiple():
    mock_payload = b"""
    {
      "quotes": {
        "quote": [
          {
            "symbol": "AAPL",
            "description": "Apple Inc",
            "exch": "Q",
            "type": "stock",
            "last": 273.47,
            "change": -1.78,
            "volume": 47994892,
            "open": 275,
            "high": 275.73,
            "low": 271.7,
            "close": 273.47,
            "bid": 273.53,
            "ask": 273.59,
            "change_percentage": -0.65,
            "average_volume": 50967638,
            "last_volume": 0,
            "trade_date": 1762982100011,
            "prevclose": 275.25,
            "week_52_high": 277.32,
            "week_52_low": 169.2101,
            "bidsize": 100,
            "bidexch": "Z",
            "bid_date": 1762982138000,
            "asksize": 200,
            "askexch": "Q",
            "ask_date": 1762982257000,
            "root_symbols": "AAPL",
            "lot_size": 100
          }
        ]
      }
    }
    """
    
    # We use sandbox=True to test the base_url
    client = TradierClient(sandbox=True, token="MOCK_TOKEN")
    
    with aioresponses() as m:
        m.get('https://sandbox.tradier.com/v1/markets/quotes?greeks=false&includeLotSize=false&symbols=AAPL', body=mock_payload)
        
        async with client:
            quotes = await get_quotes(client, ["AAPL"])
            
            assert len(quotes) == 1
            quote = quotes[0]
            assert quote.symbol == "AAPL"
            assert quote.last == 273.47
            assert quote.change_percentage == -0.65
            assert quote.lot_size == 100
            
@pytest.mark.asyncio
async def test_get_quotes_single():
    mock_payload = b"""
    {
      "quotes": {
        "quote": {
          "symbol": "SPY",
          "description": "SPDR S&P 500",
          "exch": "P",
          "type": "etf"
        }
      }
    }
    """
    
    client = TradierClient(sandbox=False, token="MOCK_TOKEN")
    
    with aioresponses() as m:
        m.get('https://api.tradier.com/v1/markets/quotes?greeks=false&includeLotSize=false&symbols=SPY', body=mock_payload)
        
        async with client:
            quotes = await get_quotes(client, ["SPY"])
            
            assert len(quotes) == 1
            quote = quotes[0]
            assert quote.symbol == "SPY"
            assert quote.type == "etf"

@pytest.mark.asyncio
async def test_get_option_strikes_single():
    # Tradier returns a single float instead of a list when only one strike matches
    mock_payload = b"""
    {
      "strikes": {
        "strike": 150.0
      }
    }
    """
    
    from tradier_api import get_option_strikes
    client = TradierClient(sandbox=False, token="MOCK_TOKEN")
    
    with aioresponses() as m:
        m.get('https://api.tradier.com/v1/markets/options/strikes?expiration=2024-01-19&symbol=AAPL', body=mock_payload)
        
        async with client:
            strikes = await get_option_strikes(client, "AAPL", "2024-01-19")
            
            assert isinstance(strikes, list)
            assert len(strikes) == 1
            assert strikes[0] == 150.0

@pytest.mark.asyncio
async def test_get_historical_quotes_multiple():
    mock_payload = b"""
    {
      "history": {
        "day": [
          {
            "date": "2023-01-03",
            "open": 130.28,
            "high": 130.9,
            "low": 124.17,
            "close": 125.07,
            "volume": 112117471
          },
          {
            "date": "2023-01-04",
            "open": 126.89,
            "high": 128.66,
            "low": 125.08,
            "close": 126.36,
            "volume": 89113633
          }
        ]
      }
    }
    """
    
    from tradier_api import get_historical_quotes
    client = TradierClient(sandbox=False, token="MOCK_TOKEN")
    
    with aioresponses() as m:
        m.get('https://api.tradier.com/v1/markets/history?interval=daily&session_filter=all&symbol=AAPL', body=mock_payload)
        
        async with client:
            history = await get_historical_quotes(client, "AAPL")
            
            assert isinstance(history, list)
            assert len(history) == 2
            assert history[0].date == "2023-01-03"
            assert history[0].open == 130.28
            assert history[1].date == "2023-01-04"
            assert history[1].volume == 89113633

@pytest.mark.asyncio
async def test_get_option_chains():
    mock_payload = b"""
    {
      "options": {
        "option": [
          {
            "symbol": "AAPL240119C00150000",
            "strike": 150.0,
            "description": "AAPL Jan 19 2024 150.0 Call",
            "exch": "Z",
            "type": "option"
          }
        ]
      }
    }
    """
    from tradier_api import get_option_chains
    client = TradierClient(sandbox=False, token="MOCK_TOKEN")
    with aioresponses() as m:
        m.get('https://api.tradier.com/v1/markets/options/chains?expiration=2024-01-19&greeks=false&symbol=AAPL', body=mock_payload)
        async with client:
            chains = await get_option_chains(client, "AAPL", "2024-01-19")
            assert len(chains) == 1
            assert chains[0].symbol == "AAPL240119C00150000"

@pytest.mark.asyncio
async def test_get_option_expirations():
    mock_payload = b"""
    {
      "expirations": {
        "date": [
          "2024-01-19",
          "2024-02-16"
        ]
      }
    }
    """
    from tradier_api import get_option_expirations
    client = TradierClient(sandbox=False, token="MOCK_TOKEN")
    with aioresponses() as m:
        m.get('https://api.tradier.com/v1/markets/options/expirations?includeAllRoots=false&strikes=false&symbol=AAPL', body=mock_payload)
        async with client:
            expirations = await get_option_expirations(client, "AAPL")
            assert len(expirations) == 2
            assert expirations[0] == "2024-01-19"

@pytest.mark.asyncio
async def test_get_time_and_sales():
    mock_payload = b"""
    {
      "series": {
        "data": [
          {
            "time": "2024-01-01T10:00:00Z",
            "price": 150.0,
            "volume": 100
          }
        ]
      }
    }
    """
    from tradier_api import get_time_and_sales
    client = TradierClient(sandbox=False, token="MOCK_TOKEN")
    with aioresponses() as m:
        m.get('https://api.tradier.com/v1/markets/timesales?interval=1min&session_filter=all&symbol=AAPL', body=mock_payload)
        async with client:
            sales = await get_time_and_sales(client, "AAPL")
            assert len(sales) == 1
            assert sales[0].price == 150.0

@pytest.mark.asyncio
async def test_get_market_clock():
    mock_payload = b"""
    {
      "clock": {
        "date": "2024-01-01",
        "description": "Market is open",
        "state": "open",
        "timestamp": 1234567890
      }
    }
    """
    from tradier_api import get_market_clock
    client = TradierClient(sandbox=False, token="MOCK_TOKEN")
    with aioresponses() as m:
        m.get('https://api.tradier.com/v1/markets/clock?delayed=false', body=mock_payload)
        async with client:
            clock = await get_market_clock(client)
            assert clock is not None
            assert clock.state == "open"

@pytest.mark.asyncio
async def test_get_market_calendar():
    mock_payload = b"""
    {
      "calendar": {
        "months": {
          "month": [
            {
              "year": 2024,
              "month": 1,
              "days": {
                "day": [
                    {
                      "date": "2024-01-01",
                      "status": "closed",
                      "description": "New Years"
                    }
                ]
              }
            }
          ]
        }
      }
    }
    """
    from tradier_api import get_market_calendar
    client = TradierClient(sandbox=False, token="MOCK_TOKEN")
    with aioresponses() as m:
        m.get('https://api.tradier.com/v1/markets/calendar?month=1&year=2024', body=mock_payload)
        async with client:
            calendar = await get_market_calendar(client, month=1, year=2024)
            assert len(calendar) == 1
            assert calendar[0].year == 2024

@pytest.mark.asyncio
async def test_search_securities():
    mock_payload = b"""
    {
      "securities": {
        "security": {
          "symbol": "AAPL",
          "exchange": "Q",
          "type": "stock",
          "description": "Apple Inc"
        }
      }
    }
    """
    from tradier_api import lookup_symbol
    client = TradierClient(sandbox=False, token="MOCK_TOKEN")
    with aioresponses() as m:
        m.get('https://api.tradier.com/v1/markets/lookup?indexes=false&q=AAPL', body=mock_payload)
        async with client:
            securities = await lookup_symbol(client, "AAPL")
            assert len(securities) == 1
            assert securities[0].symbol == "AAPL"

@pytest.mark.asyncio
async def test_lookup_symbol():
    mock_payload = b"""
    {
      "securities": {
        "security": [
          {
            "symbol": "MSFT",
            "exchange": "Q",
            "type": "stock",
            "description": "Microsoft Corp"
          }
        ]
      }
    }
    """
    from tradier_api import search_securities
    client = TradierClient(sandbox=False, token="MOCK_TOKEN")
    with aioresponses() as m:
        m.get('https://api.tradier.com/v1/markets/search?exchanges=Q&q=MSFT&types=stock', body=mock_payload)
        async with client:
            securities = await search_securities(client, "MSFT", exchanges="Q", types="stock")
            assert len(securities) == 1
            assert securities[0].symbol == "MSFT"
