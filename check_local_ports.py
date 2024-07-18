import socket
from concurrent.futures import ThreadPoolExecutor

# Function to scan a single port
def scan_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((ip, port))
        return port, True
    except:
        return port, False
    finally:
        s.close()

# Function to scan a range of ports
def scan_ports(ip, start_port, end_port):
    open_ports = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        future_to_port = {executor.submit(scan_port, ip, port): port for port in range(start_port, end_port + 1)}
        for future in future_to_port:
            port, is_open = future.result()
            if is_open:
                open_ports.append(port)
    return open_ports

# Function to assess security status based on open ports
def assess_security(open_ports):
    if open_ports:
        return "Found open ports, which may pose a security risk. Open ports: " + ", ".join(map(str, open_ports))
    else:
        return "No open ports found. The system appears to be secure."

# Main program
if __name__ == "__main__":
    # Get the local computer's IP address
    target_ip = socket.gethostbyname(socket.gethostname())
    start_port = 1
    end_port = 1024  # Scanning popular ports

    print(f"Scanning ports from {start_port} to {end_port} on {target_ip}...")
    open_ports = scan_ports(target_ip, start_port, end_port)

    status = assess_security(open_ports)
    print(status)
