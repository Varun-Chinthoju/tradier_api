"""Msgspec models for market data."""

import msgspec
from typing import List, Optional, Union

class OptionGreeks(msgspec.Struct):
    delta: Optional[float] = None
    gamma: Optional[float] = None
    theta: Optional[float] = None
    vega: Optional[float] = None
    rho: Optional[float] = None
    phi: Optional[float] = None
    bid_iv: Optional[float] = None
    mid_iv: Optional[float] = None
    ask_iv: Optional[float] = None
    smv_vol: Optional[float] = None
    updated_at: Optional[str] = None

class Quote(msgspec.Struct):
    symbol: str
    description: str
    exch: str
    type: str
    last: Optional[float] = None
    change: Optional[float] = None
    volume: Optional[int] = None
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    bid: Optional[float] = None
    ask: Optional[float] = None
    change_percentage: Optional[float] = None
    average_volume: Optional[int] = None
    last_volume: Optional[int] = None
    trade_date: Optional[int] = None
    prevclose: Optional[float] = None
    week_52_high: Optional[float] = None
    week_52_low: Optional[float] = None
    bidsize: Optional[int] = None
    bidexch: Optional[str] = None
    bid_date: Optional[int] = None
    asksize: Optional[int] = None
    askexch: Optional[str] = None
    ask_date: Optional[int] = None
    open_interest: Optional[int] = None
    contract_size: Optional[int] = None
    expiration_date: Optional[str] = None
    expiration_type: Optional[str] = None
    option_type: Optional[str] = None
    root_symbol: Optional[str] = None
    underlying: Optional[str] = None
    strike: Optional[float] = None
    lot_size: Optional[int] = None
    greeks: Optional[OptionGreeks] = None

class QuotesData(msgspec.Struct):
    quote: Union[Quote, List[Quote], None] = None

class QuotesResponse(msgspec.Struct):
    quotes: Optional[QuotesData] = None

quotes_decoder = msgspec.json.Decoder(QuotesResponse)

# Option Chains
class OptionsData(msgspec.Struct):
    option: Union[Quote, List[Quote], None] = None

class OptionsChainResponse(msgspec.Struct):
    options: Optional[OptionsData] = None

options_chain_decoder = msgspec.json.Decoder(OptionsChainResponse)

# Option Strikes
class StrikesData(msgspec.Struct):
    strike: Union[float, List[float], None] = None

class StrikesResponse(msgspec.Struct):
    strikes: Optional[StrikesData] = None

strikes_decoder = msgspec.json.Decoder(StrikesResponse)

# Option Expirations
class ExpirationsData(msgspec.Struct):
    date: Union[str, List[str], None] = None

class ExpirationsResponse(msgspec.Struct):
    expirations: Optional[ExpirationsData] = None

expirations_decoder = msgspec.json.Decoder(ExpirationsResponse)

# Historical Quotes
class HistoryQuote(msgspec.Struct):
    date: str
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    volume: Optional[int] = None

class HistoryData(msgspec.Struct):
    day: Union[HistoryQuote, List[HistoryQuote], None] = None

class HistoryResponse(msgspec.Struct):
    history: Optional[HistoryData] = None

history_decoder = msgspec.json.Decoder(HistoryResponse)

# Time and Sales
class Tick(msgspec.Struct):
    time: str
    timestamp: Optional[int] = None
    price: Optional[float] = None
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    volume: Optional[int] = None
    vwap: Optional[float] = None
    bid: Optional[float] = None
    ask: Optional[float] = None
    bidsize: Optional[int] = None
    asksize: Optional[int] = None
    condition: Optional[str] = None

class SeriesData(msgspec.Struct):
    data: Union[Tick, List[Tick], None] = None

class TimeSalesResponse(msgspec.Struct):
    series: Optional[SeriesData] = None

timesales_decoder = msgspec.json.Decoder(TimeSalesResponse)

# Market Clock
class MarketClock(msgspec.Struct):
    date: str
    description: str
    state: str
    timestamp: Optional[int] = None
    next_change: Optional[str] = None
    next_state: Optional[str] = None

class ClockResponse(msgspec.Struct):
    clock: Optional[MarketClock] = None

clock_decoder = msgspec.json.Decoder(ClockResponse)

# Market Calendar
class CalendarDay(msgspec.Struct):
    date: str
    status: str
    description: Optional[str] = None

class CalendarDays(msgspec.Struct):
    day: Union[CalendarDay, List[CalendarDay], None] = None

class CalendarMonth(msgspec.Struct):
    year: int
    month: int
    days: Optional[CalendarDays] = None

class CalendarMonths(msgspec.Struct):
    month: Union[CalendarMonth, List[CalendarMonth], None] = None

class CalendarData(msgspec.Struct):
    months: Optional[CalendarMonths] = None

class CalendarResponse(msgspec.Struct):
    calendar: Optional[CalendarData] = None

calendar_decoder = msgspec.json.Decoder(CalendarResponse)

# Security Lookup and Search
class Security(msgspec.Struct):
    symbol: str
    exchange: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None

class SecuritiesData(msgspec.Struct):
    security: Union[Security, List[Security], None] = None

class LookupResponse(msgspec.Struct):
    securities: Optional[SecuritiesData] = None

lookup_decoder = msgspec.json.Decoder(LookupResponse)
