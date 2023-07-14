import json
import sys
from web3 import Web3
from decouple import config

# Definir la función setContract
def setContract(buyer, seller, price):
    setup_txn = Escrow_contract.functions.setupContract(buyer, seller, price).buildTransaction({"gasPrice": w3.eth.gasPrice, "chainId": chain_id, "from": my_address, "nonce": nonce})
    signed_setup_txn = w3.eth.account.sign_transaction(setup_txn, private_key=private_key)

    tx_hash = w3.eth.send_raw_transaction(signed_setup_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Transaction Hash:\n" + str(tx_receipt.transactionHash))


# Cargar el archivo abi
with open("abi_escrow.json", "r") as file:
    abi = json.load(file)

# Obtener los valores de configuración de las variables de entorno
provider = config("WEB3_PROVIDER", default="http://127.0.0.1:7545")
chain_id = int(config("CHAIN_ID", default="5777"))
my_address = config("MY_ADDRESS", default="0x08074D9883cD3172c2156c862EdcAB8f284b3B20")
private_key = config("PRIVATE_KEY", default="0x193fad3b1982d13295c619634dd203315d9ffc7d73b355a901deac3e09a11b72")

# Crear una instancia de Web3
w3 = Web3(Web3.HTTPProvider(provider))
nonce = w3.eth.get_transaction_count(my_address)  # Agregar esta línea

# Crear una instancia del contrato Escrow
contract_address = sys.argv[1]  # La dirección del contrato se pasa como argumento en línea de comandos
Escrow_contract = w3.eth.contract(address=contract_address, abi=abi)

# Obtener los datos del contrato
owner = Escrow_contract.functions.dataStore(my_address, 0).call()
current_state = Escrow_contract.functions.dataStore(my_address, 1).call()
buyer = Escrow_contract.functions.dataStore(my_address, 2).call()
seller = Escrow_contract.functions.dataStore(my_address, 3).call()

# Imprimir los datos obtenidos
print("\nOwner: " + owner)
print("State: " + str(current_state))
print("Buyer: " + str(buyer))
print("Seller: " + str(seller))

# Verificar si el contrato ya está configurado
if current_state == 0:
    do_setup = input("\nDo you want to setup Contract? (Y/N)")
    if do_setup == 'Y':
        print("Setting up contract")
        setContract("0x29554bA62503d1A8974F95323a7d7c4655f5c450", "0xC7753b920E48c252225ef766a63Fcdd47EB3DDD2", 5)
else:
    print("\nContract Already Setup")
