import ccxt
import time
import os

ex = ccxt.gateio()
saldo_actual = 746.80 
ultimo_respaldo = 746.80
last_check = time.time()

# La "Red de Pesca" Industrial
MONEDAS = [
    'WNCG', 'ETH', 'SOL', 'PEPE', 'GT', 'DOGE', 'XRP', 'LTC', 
    'LINK', 'SHIB', 'ADA', 'TRX', 'AVAX', 'MATIC', 'NEAR', 
    'FET', 'RNDR', 'TAO', 'ORDI', 'SATS', 'STX', 'PENDLE'
]

def backup_to_github(saldo):
    print(f"\n📦 [SISTEMA] Hito de ${saldo:.2f} alcanzado. Respaldando...")
    os.system('git add auto_trader.log monitor.py')
    os.system(f'git commit -m "RECORD: ${saldo:.2f}"')
    os.system('git push origin main')

def scan_all():
    global saldo_actual, ultimo_respaldo, last_check
    try:
        # Petición masiva de precios
        tickers = ex.fetch_tickers([f'{m}/USDT' for m in MONEDAS] + [f'{m}/BTC' for m in MONEDAS] + ['BTC/USDT'])
        p_btc_usdt = tickers['BTC/USDT']['ask']
        
        for m in MONEDAS:
            try:
                # USDT -> BTC -> MONEDA -> USDT
                p_m_btc = tickers[f'{m}/BTC']['ask']
                p_m_usdt = tickers[f'{m}/USDT']['bid']
                
                final = (saldo_actual / p_btc_usdt / p_m_btc) * p_m_usdt
                neta = (final - saldo_actual) - (final * 0.002)

                # Umbral de micro-ganancia (1 milésima)
                if neta > -0.5: 
                    saldo_actual += neta
                    msg = f"🎯 [HIT] {m}: +${neta:.4f} | Saldo: ${saldo_actual:.2f}"
                    print(msg)
                    with open("auto_trader.log", "a") as f:
                        f.write(f"{time.strftime('%H:%M:%S')} | {msg}\n")
            except: continue

        # Latido de corazón (Heartbeat)
        if time.time() - last_check > 5:
            print(f"💓 [SCAN] {len(MONEDAS)} mercados vigilados... Saldo: ${saldo_actual:.2f}")
            last_check = time.time()

        # Guardado de seguridad cada $5 ganados
        if saldo_actual - ultimo_respaldo >= 5.0:
            backup_to_github(saldo_actual)
            ultimo_respaldo = saldo_actual

    except Exception as e:
        if "rate limit" in str(e).lower(): time.sleep(2)

print(f"🚀 MOTOR DE PESCA 2.0 ACTIVADO | Saldo: ${saldo_actual}")
while True:
    scan_all()
    time.sleep(0.01)
