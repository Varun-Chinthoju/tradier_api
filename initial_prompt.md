Act as an expert Python developer. Your task is to implement a robust, strongly-typed Python SDK for the Tradier API based on the provided documentation links. 

### Architectural Requirements
* **Modular Design:** Create a separate Python module for each API category (e.g., `user_data.py`, `accounts.py`, `trading.py`, `market_data.py`, `watchlists.py`).
* **Function Mapping:** Implement one Python function per API endpoint within its respective module.
* **Strict Typing:** Functions MUST strictly adhere to the API specification. Enforce all required and optional parameters, payload schemas, and return types using Python type hints (`typing` module).
* **Docstrings:** Include concise docstrings detailing parameters, return types, and potential exceptions.

### Security & Authentication
* **Centralized Auth:** Implement a core authentication handler or base client class to manage request headers, base URLs, and session management.
* **Secret Management:** Implement secure credential loading. API keys must never be hardcoded or committed to version control. Fetch tokens securely via a system keyring, environment variables, or fallback to a secure local configuration file (e.g., `~/.config/tradier_api/config.ini` with strict `600` file permissions).

### Execution Plan
Execute this project iteratively. Stop and wait for my "LGTM" (Looks Good To Me) approval after Step 1 before proceeding.
* **Step 1:** Implement the core authentication module/client and the `get_quotes` function within the `market_data` module.
* **Step 2:** Await review. Do not generate code for the remaining endpoints until authorized.

### API Reference Links

**User Data**
* Get User Profile: https://docs.tradier.com/reference/brokerage-api-user-get-profile.md
* Get User Balances: https://docs.tradier.com/reference/brokerage-api-user-get-balances.md

**Accounts**
* Get Account Balances: https://docs.tradier.com/reference/brokerage-api-accounts-get-account-balances.md
* Get Account Positions: https://docs.tradier.com/reference/brokerage-api-accounts-get-account-positions.md
* Get Account History: https://docs.tradier.com/reference/brokerage-api-accounts-get-account-history.md
* Get Account Gain/Loss: https://docs.tradier.com/reference/brokerage-api-accounts-get-account-gainloss.md
* Get Account Orders: https://docs.tradier.com/reference/brokerage-api-accounts-get-account-orders.md

**Trading**
* Create Order: https://docs.tradier.com/reference/brokerage-api-trading-create-order.md
* Preview Order: https://docs.tradier.com/reference/brokerage-api-trading-preview-order.md
* Modify Order: https://docs.tradier.com/reference/brokerage-api-trading-modify-order.md
* Cancel Order: https://docs.tradier.com/reference/brokerage-api-trading-cancel-order.md

**Market Data**
* Get Quotes: https://docs.tradier.com/reference/brokerage-api-markets-get-quotes.md
* Get Option Chains: https://docs.tradier.com/reference/brokerage-api-markets-get-options-chains.md
* Get Option Strikes: https://docs.tradier.com/reference/brokerage-api-markets-get-options-strikes.md
* Get Option Expirations: https://docs.tradier.com/reference/brokerage-api-markets-get-options-expirations.md
* Get Historical Quotes: https://docs.tradier.com/reference/brokerage-api-markets-get-history.md
* Get Time and Sales: https://docs.tradier.com/reference/brokerage-api-markets-get-timesales.md
* Get Market Calibration: https://docs.tradier.com/reference/brokerage-api-markets-get-clock.md
* Get Market Calendar: https://docs.tradier.com/reference/brokerage-api-markets-get-calendar.md
* Search Securities: https://docs.tradier.com/reference/brokerage-api-markets-get-lookup.md
* Lookup Symbol: https://docs.tradier.com/reference/brokerage-api-markets-get-search.md

**Watchlists**
* Get Watchlists: https://docs.tradier.com/reference/brokerage-api-watchlists-get-watchlists.md
* Get Watchlist: https://docs.tradier.com/reference/brokerage-api-watchlists-get-watchlist.md
* Create Watchlist: https://docs.tradier.com/reference/brokerage-api-watchlists-create-watchlist.md
* Update Watchlist: https://docs.tradier.com/reference/brokerage-api-watchlists-update-watchlist.md
* Delete Watchlist: https://docs.tradier.com/reference/brokerage-api-watchlists-delete-watchlist.md
* Add Item to Watchlist: https://docs.tradier.com/reference/brokerage-api-watchlists-add-item-to-watchlist.md
* Remove Item from Watchlist: https://docs.tradier.com/reference/brokerage-api-watchlists-remove-item-from-watchlist.md