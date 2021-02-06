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
## Additional Configuration
On lines 43 and 67, change `client.create_test_order` to `client.create_order`.
To change the return value of the sell order, edit line 64 where the value is currently set to `1.5`.
## Technologies
1. Python 3.8.5
2. [python-binance](https://github.com/sammchardy/python-binance)
