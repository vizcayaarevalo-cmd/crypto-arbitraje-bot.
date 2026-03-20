import ccxt
import time
from concurrent.futures import ThreadPoolExecutor

ex = ccxt.gateio()
saldo_actual = 502.79  # Empezamos con tu racha ganadora

def ejecutar_auto_trader(m):
    global saldo_actual
    try:
        # Solo operamos el triángulo de WNCG
        tickers = ex.fetch_tickers(['BTC/USDT', 'WNCG/BTC', 'WNCG/USDT'])
        p1 = tickers['BTC/USDT']['ask'] # USDT -> BTC
        p2 = tickers['WNCG/BTC']['ask'] # BTC -> WNCG
        p3 = tickers['WNCG/USDT']['bid'] # WNCG -> USDT
        
        final_usdt = (saldo_actual / p1 / p2) * p3
        ganancia_neta = (final_usdt - saldo_actual) - (final_usdt * 0.002)
        
        if ganancia_neta > 0.01: # Si ganamos más de 1 centavo, ejecutamos
            saldo_actual += ganancia_neta
            log = f"🎯 [SNIPER] WNCG | Ganancia: +${ganancia_neta:.4f} | Saldo: ${saldo_actual:.2f}"
            with open("auto_trader.log", "a") as f:
                f.write(f"{time.strftime('%H:%M:%S')} | {log}\n")
            print(f"\n{log}")
    except Exception as e:
        pass

print("🎯 SNIPER WNCG INICIADO...")
last_heartbeat = time.time()

while True:
    if time.time() - last_heartbeat > 10:
        msg = f"💓 [VIVO] Monitoreando WNCG... Saldo: ${saldo_actual:.2f}"
        with open("auto_trader.log", "a") as f:
            f.write(f"{time.strftime('%H:%M:%S')} | {msg}\n")
        last_heartbeat = time.time()
        print(".", end="", flush=True)
    
    # Ejecución ultra-rápida
    ejecutar_auto_trader('WNCG')
    time.sleep(0.5) # Pausa mínima para no banear la IP
