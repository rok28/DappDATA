from flask import Flask, render_template, request, send_from_directory
import subprocess
from web3 import Web3
from eth_utils import to_checksum_address

from os import system


#----------------------------------------------------------------------------------------------------
# Configurar conexión con Ganache o Ethereum
ganache_url = "http://127.0.0.1:7545"  # Actualiza con la URL correcta

web3 = Web3(Web3.HTTPProvider(ganache_url))
# Comprueba que la conexión se ha realizado correctamente
 

 
 

# Dirección del contrato InfuraDataStore
contract_address = "0x41319bb3084B7fB82c230148941f71C403913090"  # Actualiza con la dirección correcta
contract_abi =[
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "value",
				"type": "string"
			}
		],
		"name": "storeString",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getString",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "storedString",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

# Crear una instancia del contrato
contract = web3.eth.contract(address=contract_address, abi=contract_abi)
#----------------------------------------------------------------------------------------------------
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

#----------------------------------------------------------------------------------------------------
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        file.save('static/uploads/' + file.filename)

        # Obtener el CID del archivo cargado
        cmd_ipfs = f'ipfs add "static/uploads/{file.filename}"'
        process = subprocess.run(cmd_ipfs, shell=True, capture_output=True, text=True)

        if process.returncode != 0:
            message = "Error al cargar el archivo a IPFS: " + process.stderr
            return render_template('index.html', message=message)

        cid = process.stdout.strip().split(' ')[-2]

        # Guardar el CID en un archivo
        with open("static/cid.txt", "w") as cid_file:
            cid_file.write(cid)

        message = f"¡Archivo '{file.filename}' cargado y creado exitosamente!\nCID generado y guardado en Ethereum: {cid}"

        # La cuenta del remitente es la dirección del nodo en Ganache
        sender_account = "0x08074D9883cD3172c2156c862EdcAB8f284b3B20"
        private_key = '0x193fad3b1982d13295c619634dd203315d9ffc7d73b355a901deac3e09a11b72'

        # Crear una transacción para llamar a la función 'storeString' con el valor de cadena
        transaction = contract.functions.storeString(cid).build_transaction({
            'from': sender_account,
            'gas': 200000,  # Actualiza el límite de gas según sea necesario
            'nonce': web3.eth.get_transaction_count(sender_account),
        })

        # Firmar la transacción con la clave privada del remitente
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)

        # Enviar la transacción a la red Ethereum
        transaction_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        # Esperar a que la transacción sea minada
        transaction_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)

        print('Transacción completada. Hash de la transacción:', transaction_receipt.transactionHash.hex())
        return render_template('index.html', message=message, show_message=True)

    return render_template('index.html', show_message=False)

#----------------------------------------------------------------------------------------------------

@app.route('/download')
def download():
    try:
        with open("static/cid.txt", "r") as file:
            cid = file.read()

        cmd_ipfs = f'ipfs get "{cid}" -o static/downloads/{cid}'
        process = subprocess.run(cmd_ipfs, shell=True, capture_output=True, text=True)

        if process.returncode != 0:
            message = "Error al descargar el archivo de IPFS: " + process.stderr
            return render_template('index.html', message=message)

        message = "¡Archivo descargado con éxito!"
        return render_template('index.html', message=message)

    except FileNotFoundError:
        message = "No se encontró el archivo CID. Por favor, carga un archivo primero."
        return render_template('index.html', message=message)

#_------------------------------------------------------------------------------

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('static/uploads', filename)

#------------------------------------------------------------------------------
@app.route('/get-data', methods=['POST'])
def get_data():
    # Crear instancia del contrato utilizando el ABI y la dirección del contrato
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    # Llamar a la función 'getString' para recuperar el valor de cadena almacenado
    string_value = contract.functions.getString().call()

    # Obtén el número de página de los parámetros de solicitud, si existe.
    # Usa la página 1 por defecto si no se proporciona ningún número de página.
    page = request.args.get('page', default = 1, type = int)

    # Decide la cantidad de datos a recuperar en función del número de página.
    start = (page - 1) * 100
    end = start + 100

    cmd_ipfs = f'ipfs cat "{string_value}"'
    process = subprocess.run(cmd_ipfs, shell=True, capture_output=True, text=True)

    if process.returncode != 0:
        message = "Error al recuperar los datos de IPFS: " + process.stderr
        return render_template('index.html', message=message)

    # Divida la salida en líneas y tome solo el rango de líneas que nos interesa
    output_lines = process.stdout.splitlines()
    output_lines = output_lines[start:end]
    output = '\n'.join(output_lines)

    message = f"Datos obtenidos exitosamente:\n" + output

    try:
        # Obtener el valor de myString del contrato
        my_string = contract.functions.getString().call()
        message += f"\n\nEl identificador CID almacenado en Ethereum es: {my_string}"

        return render_template('index.html', message=message, my_string=my_string)

    except Exception as e:
        message += f"\n\nError al obtener los datos del contrato: {str(e)}"
        return render_template('index.html', message=message)

#------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
