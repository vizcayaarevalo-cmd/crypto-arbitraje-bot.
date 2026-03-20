import ccxt
import time
from concurrent.futures import ThreadPoolExecutor

ex = ccxt.gateio()
saldo_actual = 500.0 

def ejecutar_auto_trader(m):
    global saldo_actual
    try:
        tickers = ex.fetch_tickers(['BTC/USDT', f'{m}/BTC', f'{m}/USDT'])
        p1, p2, p3 = tickers['BTC/USDT']['ask'], tickers[f'{m}/BTC']['ask'], tickers[f'{m}/USDT']['bid']
        final_usdt = (saldo_actual / p1 / p2) * p3
        ganancia_neta = (final_usdt - saldo_actual) - (final_usdt * 0.002)
        if 0.005 < ganancia_neta < (saldo_actual * 0.1):
            saldo_actual += ganancia_neta
            log = f"💰 [OP] {m} | Ganancia: +${ganancia_neta:.4f} | Saldo: ${saldo_actual:.2f}"
            with open("auto_trader.log", "a") as f:
                f.write(f"{time.strftime('%H:%M:%S')} | {log}\n")
    except: pass

print("🤖 BOT INICIADO...")
ex.load_markets()
monedas = [s.split('/')[0] for s in ex.symbols if '/BTC' in s and f"{s.split('/')[0]}/USDT" in ex.symbols]
last_heartbeat = time.time()

while True:
    if time.time() - last_heartbeat > 15:
        msg = f"💓 [VIVO] Escaneando {len(monedas)} monedas... Saldo: ${saldo_actual:.2f}"
        with open("auto_trader.log", "a") as f:
            f.write(f"{time.strftime('%H:%M:%S')} | {msg}\n")
        last_heartbeat = time.time()
        print(".", end="", flush=True)
    with ThreadPoolExecutor(max_workers=40) as executor:
        executor.map(ejecutar_auto_trader, monedas)
