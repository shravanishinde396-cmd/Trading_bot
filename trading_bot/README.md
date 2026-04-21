# Binance Futures Testnet Trading Bot

A production-grade Python Trading Bot application for Binance Futures Testnet (USDT-M), featuring a full REST API, a Command Line Interface (CLI), and a modern Web Dashboard.

## Features
- **Binance Integration**: Connects to the Futures Testnet for risk-free development.
- **REST Backend**: FastAPI-powered architecture matching SaaS backend standards.
- **CLI Tool**: Typer-based command utility for quick order placements.
- **Web Dashboard**: Clean Streamlit UI with real-time log previews and straightforward trade forms.
- **Robustness**: Pydantic validations, comprehensive logging, and graceful exception handling.

## Setup Steps

1. **Clone the repository and install dependencies**:
   Ensure you have Python 3.10+ installed.
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   Copy `.env.example` to `.env` and provide your Testnet API keys.
   ```bash
   cp .env.example .env
   # Edit .env and enter your BINANCE_API_KEY and BINANCE_API_SECRET
   ```
   *Note: Obtain your Binance Testnet keys from [Binance Futures Testnet](https://testnet.binancefuture.com).*

## Running the Application

### 1. Run the API (Backend)
The backend must be running for the Web UI to place orders successfully.
```bash
uvicorn api.main:app --reload
```
API Documentation will be available at: `http://localhost:8000/docs`

### 2. Run the Web UI (Dashboard)
```bash
streamlit run ui/app.py
```

### 3. Run the CLI
You can run the CLI directly to interact with the bot engine (independently of the API/UI).
```bash
python cli.py trade --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

## Usage Examples

### Example MARKET Order (CLI)
```bash
python cli.py trade --symbol BTCUSDT --side SELL --type MARKET --quantity 0.05
```

### Example LIMIT Order (CLI)
```bash
python cli.py trade --symbol ETHUSDT --side BUY --type LIMIT --quantity 0.1 --price 3200.50
```

## Screenshots
*(Insert placeholders for screenshots below)*
- `[Screenshot: Web Dashboard Orders Form]`
- `[Screenshot: CLI Execution Output]`
- `[Screenshot: FastAPI Swagger Docs]`
