# Ticket System for Raspberry Pi

## Features

- Touchscreen GUI (Tkinter) for entry/exit
- On-screen keyboard for touch input
- Ticketless (phone number) and ticketed (QR code) entry
- Secure, random ticket code generation
- Prints QR code ticket (ESC/POS thermal printer)
- Gate control via Arduino Uno (USB serial)
- Works offline; can sync to central server (expandable)

## Hardware Requirements

- Raspberry Pi (with RPi OS)
- Touchscreen display
- USB thermal printer (ESC/POS compatible)
- Arduino Uno (USB connection for gate relay)
- 2D barcode scanner (USB; acts as keyboard)

## Quick Install

```bash
sudo ./install_ticket_system.sh
```

## Usage

- The system auto-starts on boot.
- For ticketed entry, press "Print Ticket & Enter". Present the QR code or enter the ticket code at exit.
- For ticketless, enter your phone number.
- For exit, scan the QR code or enter the ticket code/phone number.

## Development

- Python code is in `pi/`
- Arduino sketch is in `arduino/`
- Systemd service auto-starts the GUI

## Customization

- Update USB Vendor/Product IDs in `printer.py` for your printer.
- Edit udev rules in `install_ticket_system.sh` as needed.

## Security

- Tickets use cryptographically secure random codes
- QR code displayed and printed for easy scanning

---