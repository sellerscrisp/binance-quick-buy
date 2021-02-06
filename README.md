# Binance Quick Buy
This little application allows a user to quickly buy a Bitcoin pair on Binance and sell at a specified return.

## Installation
```bash
# Update the API_KEY and API_SECRET variables in `settings_template.py`. 
# Rename the file:
mv settings_template.py settings.py
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Technologies
1. Python 3.8.5
2. [python-binance](https://github.com/sammchardy/python-binance)
