"""Market data module functionality."""

from typing import List, Optional
from .client import TradierClient
from .models.market_data import (
    Quote, quotes_decoder,
    options_chain_decoder,
    strikes_decoder,
    expirations_decoder,
    HistoryQuote, history_decoder,
    Tick, timesales_decoder,
    MarketClock, clock_decoder,
    CalendarMonth, calendar_decoder,
    Security, lookup_decoder
)

async def get_quotes(
    client: TradierClient,
    symbols: List[str],
    greeks: bool = False,
    include_lot_size: bool = False
) -> List[Quote]:
    """
    Get quotes for one or more symbols.
    
    Documentation: https://docs.tradier.com/reference/brokerage-api-markets-get-quotes
    Note: Single-item matching results from Tradier's JSON are gracefully flattened to python lists.

    Args:
        client: The initialized asynchronous TradierClient.
        symbols: A list of symbols to get quotes for (e.g., ['AAPL', 'SPY']).
        greeks: Include greek calculations for options if True.
        include_lot_size: Include lot size information if True.

    Returns:
        A strictly-typed list of Quote models.
    """
    if not symbols:
        return []

    params = {
        "symbols": ",".join(symbols),
        "greeks": str(greeks).lower(),
        "includeLotSize": str(include_lot_size).lower()
    }
    
    raw_data = await client.get("markets/quotes", params=params)
    
    response = quotes_decoder.decode(raw_data)
    
    if not response.quotes or response.quotes.quote is None:
        return []
        
    if isinstance(response.quotes.quote, list):
        return response.quotes.quote
    return [response.quotes.quote]

async def get_option_chains(
    client: TradierClient,
    symbol: str,
    expiration: str,
    greeks: bool = False
) -> List[Quote]:
    """
    Get option chains for a specific underlying symbol and expiration date.
    
    Documentation: https://docs.tradier.com/reference/brokerage-api-markets-get-options-chains
    Note: Single-item matching results from Tradier's JSON are gracefully flattened to python lists.
    
    Args:
        client: The initialized asynchronous TradierClient.
        symbol: The underlying security symbol (e.g., 'AAPL').
        expiration: The expiration date in YYYY-MM-DD format.
        greeks: Include greek and IV calculations courtesy of ORATS if True.
        
    Returns:
        A strictly-typed list of Quote models representing the option chain.
    """
    params = {
        "symbol": symbol,
        "expiration": expiration,
        "greeks": str(greeks).lower()
    }
    raw_data = await client.get("markets/options/chains", params=params)
    response = options_chain_decoder.decode(raw_data)
    
    if not response.options or response.options.option is None:
        return []
    if isinstance(response.options.option, list):
        return response.options.option
    return [response.options.option]

async def get_option_strikes(
    client: TradierClient,
    symbol: str,
    expiration: str
) -> List[float]:
    """
    Get option strikes for a specific underlying symbol and expiration date.
    
    Documentation: https://docs.tradier.com/reference/brokerage-api-markets-get-options-strikes
    Note: Single-item matching results from Tradier's JSON are gracefully flattened to python lists.
    
    Args:
        client: The initialized asynchronous TradierClient.
        symbol: The underlying security symbol (e.g., 'AAPL').
        expiration: The expiration date in YYYY-MM-DD format.
        
    Returns:
        A strictly-typed list of strike prices as floats.
    """
    params = {
        "symbol": symbol,
        "expiration": expiration
    }
    raw_data = await client.get("markets/options/strikes", params=params)
    response = strikes_decoder.decode(raw_data)
    
    if not response.strikes or response.strikes.strike is None:
        return []
    if isinstance(response.strikes.strike, list):
        return response.strikes.strike
    return [response.strikes.strike]

async def get_option_expirations(
    client: TradierClient,
    symbol: str,
    include_all_roots: bool = False,
    strikes: bool = False
) -> List[str]:
    """
    Get option expirations for a specific underlying symbol.
    
    Documentation: https://docs.tradier.com/reference/brokerage-api-markets-get-options-expirations
    Note: Single-item matching results from Tradier's JSON are gracefully flattened to python lists.
    
    Args:
        client: The initialized asynchronous TradierClient.
        symbol: The underlying security symbol (e.g., 'AAPL').
        include_all_roots: Include all roots corresponding to the symbol if True.
        strikes: Include the strikes for each expiration if True.
        
    Returns:
        A strictly-typed list of expiration dates in YYYY-MM-DD format as strings.
    """
    params = {
        "symbol": symbol,
        "includeAllRoots": str(include_all_roots).lower(),
        "strikes": str(strikes).lower()
    }
    raw_data = await client.get("markets/options/expirations", params=params)
    response = expirations_decoder.decode(raw_data)
    
    if not response.expirations or response.expirations.date is None:
        return []
    if isinstance(response.expirations.date, list):
        return response.expirations.date
    return [response.expirations.date]

async def get_historical_quotes(
    client: TradierClient,
    symbol: str,
    interval: str = "daily",
    start: Optional[str] = None,
    end: Optional[str] = None,
    session_filter: str = "all"
) -> List[HistoryQuote]:
    """
    Get historical quotes for a symbol.
    
    Documentation: https://docs.tradier.com/reference/brokerage-api-markets-get-history
    Note: Single-item matching results from Tradier's JSON are gracefully flattened to python lists.
    
    Args:
        client: The initialized asynchronous TradierClient.
        symbol: The security symbol (e.g., 'AAPL').
        interval: The interval of the historical data (default: 'daily', options: 'daily', 'weekly', 'monthly').
        start: Start date in YYYY-MM-DD format (optional).
        end: End date in YYYY-MM-DD format (optional).
        session_filter: Time filter (default: 'all', options: 'all', 'open').
        
    Returns:
        A strictly-typed list of HistoryQuote models representing the historical metrics.
    """
    params = {
        "symbol": symbol,
        "interval": interval,
        "session_filter": session_filter
    }
    if start:
        params["start"] = start
    if end:
        params["end"] = end
        
    raw_data = await client.get("markets/history", params=params)
    response = history_decoder.decode(raw_data)
    
    if not response.history or response.history.day is None:
        return []
    if isinstance(response.history.day, list):
        return response.history.day
    return [response.history.day]

async def get_time_and_sales(
    client: TradierClient,
    symbol: str,
    interval: str = "1min",
    start: Optional[str] = None,
    end: Optional[str] = None,
    session_filter: str = "all"
) -> List[Tick]:
    """
    Get time and sales (tick) data for a symbol.
    
    Documentation: https://docs.tradier.com/reference/brokerage-api-markets-get-timesales
    Note: Single-item matching results from Tradier's JSON are gracefully flattened to python lists.
    
    Args:
        client: The initialized asynchronous TradierClient.
        symbol: The security symbol (e.g., 'AAPL').
        interval: Time interval (default: '1min', options: 'tick', '1min', '5min', '15min').
        start: Start datetime in YYYY-MM-DD HH:MM format (optional).
        end: End datetime in YYYY-MM-DD HH:MM format (optional).
        session_filter: Session filter (default: 'all', options: 'all', 'open').
        
    Returns:
        A strictly-typed list of Tick models containing exact transaction details.
    """
    params = {
        "symbol": symbol,
        "interval": interval,
        "session_filter": session_filter
    }
    if start:
        params["start"] = start
    if end:
        params["end"] = end
        
    raw_data = await client.get("markets/timesales", params=params)
    response = timesales_decoder.decode(raw_data)
    
    if not response.series or response.series.data is None:
        return []
    if isinstance(response.series.data, list):
        return response.series.data
    return [response.series.data]

async def get_market_clock(
    client: TradierClient,
    delayed: bool = False
) -> Optional[MarketClock]:
    """
    Get the market calibration clock.
    
    Documentation: https://docs.tradier.com/reference/brokerage-api-markets-get-clock
    
    Args:
        client: The initialized asynchronous TradierClient.
        delayed: Get the delayed market clock status if True.
        
    Returns:
        A strictly-typed MarketClock model detailing the current market states.
    """
    params = {"delayed": str(delayed).lower()}
    raw_data = await client.get("markets/clock", params=params)
    response = clock_decoder.decode(raw_data)
    return response.clock

async def get_market_calendar(
    client: TradierClient,
    month: Optional[int] = None,
    year: Optional[int] = None
) -> List[CalendarMonth]:
    """
    Get the market calendar for the current or specified month/year.
    
    Documentation: https://docs.tradier.com/reference/brokerage-api-markets-get-calendar
    Note: Single-item matching results from Tradier's JSON are gracefully flattened to python lists.
    
    Args:
        client: The initialized asynchronous TradierClient.
        month: Calendar month (1-12) (optional).
        year: Calendar year (e.g., 2024) (optional).
        
    Returns:
        A strictly-typed list of CalendarMonth models representing the market status days.
    """
    params = {}
    if month is not None:
        params["month"] = str(month)
    if year is not None:
        params["year"] = str(year)
        
    raw_data = await client.get("markets/calendar", params=params)
    response = calendar_decoder.decode(raw_data)
    
    if not response.calendar or not response.calendar.months or response.calendar.months.month is None:
        return []
        
    if isinstance(response.calendar.months.month, list):
        return response.calendar.months.month
    return [response.calendar.months.month]

async def lookup_symbol(
    client: TradierClient,
    q: str,
    indexes: bool = False
) -> List[Security]:
    """
    Look up a symbol or security by prefix (maps to /v1/markets/lookup).
    
    Documentation: https://docs.tradier.com/reference/brokerage-api-markets-get-lookup
    Note: Single-item matching results from Tradier's JSON are gracefully flattened to python lists.
    
    Args:
        client: The initialized asynchronous TradierClient.
        q: The prefix query string (e.g., 'app' for Apple).
        indexes: Include indexes in the lookup response if True.
        
    Returns:
        A strictly-typed list of Security models representing the matched assets.
    """
    params = {
        "q": q,
        "indexes": str(indexes).lower()
    }
    raw_data = await client.get("markets/lookup", params=params)
    response = lookup_decoder.decode(raw_data)
    
    if not response.securities or response.securities.security is None:
        return []
    if isinstance(response.securities.security, list):
        return response.securities.security
    return [response.securities.security]

async def search_securities(
    client: TradierClient,
    q: str,
    exchanges: Optional[str] = None,
    types: Optional[str] = None
) -> List[Security]:
    """
    Search for a symbol using detailed filters (maps to /v1/markets/search).
    
    Documentation: https://docs.tradier.com/reference/brokerage-api-markets-get-search
    Note: Single-item matching results from Tradier's JSON are gracefully flattened to python lists.
    
    Args:
        client: The initialized asynchronous TradierClient.
        q: The exact or partial string query.
        exchanges: Comma-separated list of precise exchanges to filter by (optional).
        types: Comma-separated list of security types (stock, option, etf, index) (optional).
        
    Returns:
        A strictly-typed list of Security models returning the matched assets.
    """
    params = {"q": q}
    if exchanges:
        params["exchanges"] = exchanges
    if types:
        params["types"] = types
        
    raw_data = await client.get("markets/search", params=params)
    response = lookup_decoder.decode(raw_data)
    
    if not response.securities or response.securities.security is None:
        return []
    if isinstance(response.securities.security, list):
        return response.securities.security
    return [response.securities.security]
