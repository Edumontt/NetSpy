# NetSpy - Spyware em Python

**NetSpy** é um Spyware desenvolvido em Python que captura eventos de teclado / clipboard e execução de comandos backdoor com execução através da rede.

## 🛠️ Funcionalidades

- Execuções do keylogger independente do listener.
- Captura de teclas pressionadas (keylogging).
- Monitoramento do clipboard (copia e cola).
- Envio de dados capturados para um servidor remoto via socket.
- Execução de comandos no PowerShell através de uma conexão de rede.

## 🛠️ Funções

**Utilização da função: função=arg1,arg2**
- **keylogrede=<ip>,<porta>** - Inicia o Keylogger e envia as teclas para um ip e porta.
- **keyloglocal=<caminho>** - Inicia o Keylogger e salva as teclas no arquivo do argumento.
- **exe=<cmd>** - Executa comandos no powershell.
- **sair** - fecha o listener do NetSpy.

## ⚙️ Como Usar

1. **Configuração do NetSpy**:
   - Defina o endereço IP e a porta onde o spyware irá escutar.
   - Exemplo:
     ```python
     ip_local = "127.0.0.1"
     porta_local = 4444 #padrão
     ```
--
2. **Inicie**:
   - Execute o script Python que contém o código do spyware.
   - O spyware começará a escutar a porta especificada.
--
3. **Chame as Funções**:
   - Utilize os comandos de controle, como `keylogrede` para iniciar o keylogger ou `exe` para executar comandos no PowerShell.
--
## 📋 Requisitos

```bash
pip install -r requirements.txt
```

## ⚠️ Aviso

Este software foi desenvolvido para fins educacionais ;).

