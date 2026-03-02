import win32print
from PIL import Image
import math
from datetime import datetime

PRINTER_NAME = "Thermal Printer"


def format_line(left, right, width=32):
    space = width - len(left) - len(right)
    if space < 0:
        space = 0
    return left + (" " * space) + right + "\n"


def image_to_escpos(image_path):
    ESC = b'\x1b'
    GS = b'\x1d'

    img = Image.open(image_path)

    max_width = 384
    width, height = img.size

    if width > max_width:
        ratio = max_width / float(width)
        height = int(float(height) * ratio)
        img = img.resize((max_width, height))

    img = img.convert("1")

    width, height = img.size
    width_bytes = math.ceil(width / 8)

    raster_header = GS + b'v0' + b'\x00' + \
        width_bytes.to_bytes(2, 'little') + \
        height.to_bytes(2, 'little')

    pixels = img.load()
    image_bytes = b''

    for y in range(height):
        for x in range(0, width, 8):
            byte = 0
            for bit in range(8):
                if x + bit < width:
                    if pixels[x + bit, y] == 0:
                        byte |= (1 << (7 - bit))
            image_bytes += byte.to_bytes(1, 'big')

    return raster_header + image_bytes


def print_round_receipt(player1, player2, round_no, score1, score2):
    ESC = b'\x1b'
    GS = b'\x1d'

    initialize = ESC + b'@'
    center = ESC + b'a' + b'\x01'
    left = ESC + b'a' + b'\x00'
    bold_on = ESC + b'E' + b'\x01'
    bold_off = ESC + b'E' + b'\x00'
    cut = GS + b'V' + b'\x41' + b'\x10'
    logo_bytes = image_to_escpos(r"assets/logo/128x128.jpeg")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Determine winner
    if score1 > score2:
        winner = player1
    elif score2 > score1:
        winner = player2
    else:
        winner = "DRAW"

    receipt_text = ""

    receipt_text += "ARNISENSE MATCH SYSTEM\n"
    receipt_text += "-" * 32 + "\n"
    receipt_text += f"Match No: {round_no}\n"
    receipt_text += f"Date: {now}\n"
    receipt_text += "-" * 32 + "\n"

    receipt_text += format_line(player1, str(score1))
    receipt_text += format_line(player2, str(score2))

    receipt_text += "-" * 32 + "\n"
    receipt_text += format_line("ROUND WINNER", winner)
    receipt_text += "-" * 32 + "\n\n"

    receipt_text += "Official Electronic Scoring\n"
    receipt_text += "Powered by Arnisense\n\n"

    # Load Logo

    receipt_bytes = (
        initialize +
        center +
        logo_bytes + b"\n" +
        bold_on +
        receipt_text.encode("ascii", "ignore") +
        bold_off +
        cut
    )

    hPrinter = win32print.OpenPrinter(PRINTER_NAME)
    try:
        win32print.StartDocPrinter(hPrinter, 1, ("Arnisense Round Receipt", None, "RAW"))
        win32print.StartPagePrinter(hPrinter)
        win32print.WritePrinter(hPrinter, receipt_bytes)
        win32print.EndPagePrinter(hPrinter)
        win32print.EndDocPrinter(hPrinter)
    finally:
        win32print.ClosePrinter(hPrinter)

    print("Round Receipt Printed Successfully!")


# 🥋 TEST SAMPLE
print_round_receipt(
    player1="Player Red",
    player2="Player Blue",
    round_no=1,
    score1=5,
    score2=3
)