# recon-scanner

A multithreaded network reconnaissance tool built in Python.

## Features
- Fast multithreaded TCP port scanning
- Banner grabbing for service and version detection
- Clean CLI interface
- Color-coded table output

## Installation
pip install -r requirements.txt

## Usage
python3 scanner.py --target <IP> --start <port> --end <port> --threads <n>

## Example
python3 scanner.py --target 192.168.1.1 --start 1 --end 9000