import requests
import pandas as pd
import time
import datetime as dt
import pytz

api_key = 'YOUR_BSCSCAN_API_KEY_HERE'
if api_key == 'YOUR_BSCSCAN_API_KEY_HERE':
    print('Bscscan api key missing. Create a free account and introduce your API key above.')
    exit(1)

history = pd.read_csv('dogebonk_history.csv')
biz_announcement_timestamp = dt.datetime(2021, 5, 3, 22, 22, 0, tzinfo=pytz.UTC).timestamp()
early_tx_timestamps = [t for t in list(history['UnixTimestamp']) if t < biz_announcement_timestamp]
early_addresses = [a for a in history['To'][5:len(early_tx_timestamps)]
                   if a != '0xbe80839a3be4d3953d5588a60a11aeaed286b593'] # exclude liquidity pool address

print('Checking for large early DOBO insiders...')
cumulative = 0
for address in set(early_addresses):
    r = requests.get('https://api.bscscan.com/api?module=account&action=tokenbalance'
                     '&contractaddress=0xAe2DF9F730c54400934c06a17462c41C08a06ED8'
                     '&address=' + address + '&apikey=' + api_key)

    balance_in_billions = round(int(r.json()['result']) / 1_000_000_000_000_000_000, 2)
    cumulative = round(cumulative + balance_in_billions, 2)
    time.sleep(1) # avoid getting throttled by bscscan
    if(balance_in_billions > 1000):
        print('cumulative=' + str(cumulative) + ', address=' + address + ', balance=' + str(balance_in_billions))

print('cumulative=' + str(cumulative))

# output
# cumulative=1412.97, address=0x52ec8e34c3dbb7cc6f493dc2a5e973dcadf2c31e, balance=1409.03
# cumulative=2872.6, address=0x68c838ccdd83b4826a0d3dc3288a10d214224534, balance=1451.93
# cumulative=5788.77, address=0xb78e0723b82e97dca6ead85219cb3edf233e5579, balance=2537.64
# cumulative=20913.64, address=0x5754abd8869851eeca1b9c4bf534e66d95fc9978, balance=13918.85
# cumulative=22830.43, address=0x089d0b893aa471c544f7f79c4d175b577bee4dfc, balance=1915.03
# cumulative=22953.77
