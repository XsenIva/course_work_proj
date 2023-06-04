import socket

domain_name = input()

def scan_port(ip, port):
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  if client.connect_ex((ip, port)):
    print(f"Порт {port} закрыт")
  else: print(f"Порт {port} открыт")

def scan_port_start(domain_name):
  ip = socket.gethostbyname(domain_name)
  for i in range(250):
    scan_port(ip, i)

scan_port_start(domain_name)