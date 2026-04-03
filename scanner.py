import socket
import concurrent.futures
from rich.console import Console
from rich.table import Table
import argparse

console = Console()

def scan_port(host, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return port, "open" if result == 0 else "closed"
    except Exception as e:
        return port, f"error: {e}"

def grab_banner(host, port, timeout=2):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = sock.recv(1024).decode("utf-8", errors="ignore").strip()
        sock.close()
        return banner if banner else "no banner"
    except:
        return "no banner"

def scan_range(host, start_port, end_port, threads=100):
    console.print(f"\n[bold cyan][*] Scanning {host} ports {start_port}-{end_port}...[/bold cyan]\n")
    open_ports = []
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(scan_port, host, port): port for port in range(start_port, end_port + 1)}
        for future in concurrent.futures.as_completed(futures):
            port, status = future.result()
            if status == "open":
                banner = grab_banner(host, port)
                open_ports.append(port)
                results.append((port, banner))

    table = Table(title=f"Scan Results — {host}", show_lines=True)
    table.add_column("Port", style="bold green", width=10)
    table.add_column("Status", style="green", width=10)
    table.add_column("Banner", style="yellow")

    for port, banner in sorted(results):
        table.add_row(str(port), "OPEN", banner)

    console.print(table)
    console.print(f"\n[bold green][*] Scan complete. {len(open_ports)} open port(s) found.[/bold green]\n")
    return sorted(open_ports)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Recon Scanner — Python port scanner with banner grabbing"
    )
    parser.add_argument("--target", required=True, help="Target IP address")
    parser.add_argument("--start", type=int, default=1, help="Start port (default: 1)")
    parser.add_argument("--end", type=int, default=1024, help="End port (default: 1024)")
    parser.add_argument("--threads", type=int, default=100, help="Number of threads (default: 100)")
    args = parser.parse_args()

    scan_range(args.target, args.start, args.end, args.threads)