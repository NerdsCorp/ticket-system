from escpos.printer import Usb
import qrcode
from io import BytesIO

def print_ticket(ticket_code):
    # Generate QR code image
    qr = qrcode.QRCode(box_size=6, border=2)
    qr.add_data(ticket_code)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    buf = BytesIO()
    img.save(buf, format='PNG')
    qr_data = buf.getvalue()

    # Print ticket with code and QR
    p = Usb(0x04b8, 0x0e15)  # Update for your printer
    p.text("Parking Ticket\n")
    p.text(f"Ticket Code: {ticket_code}\n")
    p.image(BytesIO(qr_data))  # Print QR code image
    p.text("Scan QR on exit\n")
    p.cut()