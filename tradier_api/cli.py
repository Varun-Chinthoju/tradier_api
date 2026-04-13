"""Command line interface for Tradier API SDK."""

import argparse
import getpass
import sys
import asyncio
import msgspec
from .auth import set_api_token
from .client import TradierClient
from .market_data import (
    get_quotes, get_option_chains, get_option_strikes, get_option_expirations,
    get_historical_quotes, get_time_and_sales, get_market_clock,
    get_market_calendar, search_securities, lookup_symbol
)

def str2bool(v):
    """Custom action to parse boolean strings cleanly"""
    if isinstance(v, bool):
        return v
    if str(v).lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif str(v).lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

async def execute_api_call(coro, client, **kwargs):
    """Execute a market data endpoint and JSON encode the strictly-typed structures identically to typical output."""
    async with client:
        try:
            result = await coro(client, **kwargs)
            print(msgspec.json.encode(result).decode('utf-8'))
        except msgspec.DecodeError as e:
            print(f"Error parsing API response. The gateway may be down or response was malformed: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error executing command: {e}", file=sys.stderr)
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Tradier API SDK CLI")
    parser.add_argument("--sandbox", action="store_true", help="Use sandbox environment globally")
    
    # We use required=False for python 3.8+ compatibility and manual fallback routing
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    subparsers.required = True
    
    # Auth subcommand
    auth_parser = subparsers.add_parser("auth", help="Configure your Tradier API Token securely")
    auth_parser.add_argument("--no-keyring", action="store_true", help="Store token in config.ini instead of system keyring")
    
    # Get Quotes subcommand
    quotes_parser = subparsers.add_parser("get_quotes", help="Get quotes for one or more symbols")
    quotes_parser.add_argument("--symbols", required=True, help="Comma-separated list of symbols (e.g. NVDA,MSFT)")
    quotes_parser.add_argument("--greeks", type=str2bool, nargs='?', const=True, default=False)
    quotes_parser.add_argument("--include_lot_size", type=str2bool, nargs='?', const=True, default=False)

    chains_parser = subparsers.add_parser("get_option_chains", help="Get option chains")
    chains_parser.add_argument("--symbol", required=True)
    chains_parser.add_argument("--expiration", required=True, help="YYYY-MM-DD")
    chains_parser.add_argument("--greeks", type=str2bool, nargs='?', const=True, default=False)

    strikes_parser = subparsers.add_parser("get_option_strikes", help="Get option strikes")
    strikes_parser.add_argument("--symbol", required=True)
    strikes_parser.add_argument("--expiration", required=True, help="YYYY-MM-DD")

    exps_parser = subparsers.add_parser("get_option_expirations", help="Get option expirations")
    exps_parser.add_argument("--symbol", required=True)
    exps_parser.add_argument("--include_all_roots", type=str2bool, nargs='?', const=True, default=False)
    exps_parser.add_argument("--strikes", type=str2bool, nargs='?', const=True, default=False)

    history_parser = subparsers.add_parser("get_historical_quotes", help="Get historical quotes")
    history_parser.add_argument("--symbol", required=True)
    history_parser.add_argument("--interval", default="daily", choices=["daily", "weekly", "monthly"])
    history_parser.add_argument("--start", help="YYYY-MM-DD")
    history_parser.add_argument("--end", help="YYYY-MM-DD")
    history_parser.add_argument("--session_filter", default="all", choices=["all", "open"])

    timesales_parser = subparsers.add_parser("get_time_and_sales", help="Get time and sales (tick)")
    timesales_parser.add_argument("--symbol", required=True)
    timesales_parser.add_argument("--interval", default="1min", choices=["tick", "1min", "5min", "15min"])
    timesales_parser.add_argument("--start", help="YYYY-MM-DD HH:MM")
    timesales_parser.add_argument("--end", help="YYYY-MM-DD HH:MM")
    timesales_parser.add_argument("--session_filter", default="all", choices=["all", "open"])

    clock_parser = subparsers.add_parser("get_market_clock", help="Get market clock")
    clock_parser.add_argument("--delayed", type=str2bool, nargs='?', const=True, default=False)

    calendar_parser = subparsers.add_parser("get_market_calendar", help="Get market calendar")
    calendar_parser.add_argument("--month", type=int)
    calendar_parser.add_argument("--year", type=int)

    search_parser = subparsers.add_parser("search_securities", help="Lookup a symbol by prefix")
    search_parser.add_argument("--q", required=True)
    search_parser.add_argument("--indexes", type=str2bool, nargs='?', const=True, default=False)

    lookup_parser = subparsers.add_parser("lookup_symbol", help="Search for a symbol using filters")
    lookup_parser.add_argument("--q", required=True)
    lookup_parser.add_argument("--exchanges")
    lookup_parser.add_argument("--types")

    args = parser.parse_args()
    
    if args.command == "auth":
        print("--- Tradier API SDK Authentication Setup ---")
        token = getpass.getpass("Enter your Tradier API Token (input hidden): ").strip()
        if not token:
            print("Error: Token cannot be empty.")
            sys.exit(1)
            
        use_keyring = not args.no_keyring
        try:
            set_api_token(token, use_keyring=use_keyring)
            storage = "system keyring" if use_keyring else "local config.ini file"
            print(f"Success! Token securely saved to {storage}.")
        except Exception as e:
            print(f"Failed to save token: {e}")
            sys.exit(1)
            
    elif args.command == "get_quotes":
        symbols = [s.strip() for s in args.symbols.split(',')]
        client = TradierClient(sandbox=args.sandbox)
        asyncio.run(execute_api_call(get_quotes, client, symbols=symbols, greeks=args.greeks, include_lot_size=args.include_lot_size))
        
    elif args.command == "get_option_chains":
        client = TradierClient(sandbox=args.sandbox)
        asyncio.run(execute_api_call(get_option_chains, client, symbol=args.symbol, expiration=args.expiration, greeks=args.greeks))
        
    elif args.command == "get_option_strikes":
        client = TradierClient(sandbox=args.sandbox)
        asyncio.run(execute_api_call(get_option_strikes, client, symbol=args.symbol, expiration=args.expiration))
        
    elif args.command == "get_option_expirations":
        client = TradierClient(sandbox=args.sandbox)
        asyncio.run(execute_api_call(get_option_expirations, client, symbol=args.symbol, include_all_roots=args.include_all_roots, strikes=args.strikes))
        
    elif args.command == "get_historical_quotes":
        client = TradierClient(sandbox=args.sandbox)
        asyncio.run(execute_api_call(get_historical_quotes, client, symbol=args.symbol, interval=args.interval, start=args.start, end=args.end, session_filter=args.session_filter))
        
    elif args.command == "get_time_and_sales":
        client = TradierClient(sandbox=args.sandbox)
        asyncio.run(execute_api_call(get_time_and_sales, client, symbol=args.symbol, interval=args.interval, start=args.start, end=args.end, session_filter=args.session_filter))
        
    elif args.command == "get_market_clock":
        client = TradierClient(sandbox=args.sandbox)
        asyncio.run(execute_api_call(get_market_clock, client, delayed=args.delayed))
        
    elif args.command == "get_market_calendar":
        client = TradierClient(sandbox=args.sandbox)
        asyncio.run(execute_api_call(get_market_calendar, client, month=args.month, year=args.year))
        
    elif args.command == "lookup_symbol":
        client = TradierClient(sandbox=args.sandbox)
        asyncio.run(execute_api_call(lookup_symbol, client, q=args.q, indexes=args.indexes))
        
    elif args.command == "search_securities":
        client = TradierClient(sandbox=args.sandbox)
        asyncio.run(execute_api_call(search_securities, client, q=args.q, exchanges=args.exchanges, types=args.types))

if __name__ == "__main__":
    main()
