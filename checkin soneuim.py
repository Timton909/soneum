from web3 import Web3
import time
import random

# Конфигурация
RPC_URL = "https://soneium-mainnet.g.alchemy.com"  
CONTRACT_ADDRESS = "0xbb4904e033Ef5Af3fc5d3D72888f1cAd7944784D"
PRIVATE_KEYS_FILE = "private_keys.txt"
CHAIN_ID = 1868
DELAY_MIN = 15    # Минимальная задержка между транзакциями
DELAY_MAX = 25   # Максимальная задержка между транзакциями

def initialize_web3(rpc_url):
    """Инициализация подключения к блокчейну"""
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    if not web3.is_connected():
        raise ConnectionError("Не удалось подключиться к RPC")
    return web3

def load_private_keys(file_path):
    """Загрузка приватных ключей из файла"""
    with open(file_path, "r") as file:
        return [line.strip() for line in file if line.strip()]

def send_transaction(web3, private_key):
    """Отправка транзакции"""
    account = web3.eth.account.from_key(private_key)
    
    # Параметры транзакции
    transaction = {
        'chainId': CHAIN_ID,
        'to': Web3.to_checksum_address(CONTRACT_ADDRESS),
        'data': '0xb5d7df97',
        'value': 0,  # 0 ETH
        'gas': 100000,
        'gasPrice': web3.eth.gas_price,
        'nonce': web3.eth.get_transaction_count(account.address),
    }

    try:
        # Оценка газа
        transaction['gas'] = web3.eth.estimate_gas(transaction)
        # Подпись и отправка
        signed_tx = web3.eth.account.sign_transaction(transaction, private_key)
        raw_tx = signed_tx.raw_transaction  # Обратите внимание на snake_case!
        return web3.eth.send_raw_transaction(raw_tx).hex()
    except Exception as e:
        raise Exception(f"Ошибка отправки: {str(e)}")

def main():
    web3 = initialize_web3(RPC_URL)
    private_keys = load_private_keys(PRIVATE_KEYS_FILE)
    
    print(f"Найдено {len(private_keys)} кошельков")
    print(f"Текущий gas price: {web3.from_wei(web3.eth.gas_price, 'gwei'):.2f} Gwei")

    for idx, pk in enumerate(private_keys):
        try:
            account = web3.eth.account.from_key(pk)
            print(f"\nОбработка кошелька {idx+1}/{len(private_keys)}")
            print(f"Адрес: {account.address}")
            
            tx_hash = send_transaction(web3, pk)
            print(f"Успешно! TX Hash: {tx_hash}")
            
            if idx < len(private_keys) - 1:
                delay = random.randint(DELAY_MIN, DELAY_MAX)
                print(f"Задержка {delay} сек...")
                time.sleep(delay)
                
        except Exception as e:
            print(f"Ошибка: {str(e)}")
            continue

if __name__ == "__main__":
    main()