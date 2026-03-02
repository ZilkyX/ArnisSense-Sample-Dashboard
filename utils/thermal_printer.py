import win32print
from PIL import Image
import math
from datetime import datetime


# ===============================
# Thermal Printer Engine Class
# ===============================
class ThermalPrinter:
    def __init__(self, printer_name):
        self.printer_name = printer_name

        self.ESC = b'\x1b'
        self.GS = b'\x1d'

        self.initialize = self.ESC + b'@'
        self.cut = self.GS + b'V' + b'\x41' + b'\x10'

    # ---------- Image Converter ----------
    def image_to_escpos(self, image_path):
        img = Image.open(image_path)

        max_width = 384
        width, height = img.size

        if width > max_width:
            ratio = max_width / float(width)
            height = int(height * ratio)
            img = img.resize((max_width, height))

        img = img.convert("1")

        width, height = img.size
        width_bytes = math.ceil(width / 8)

        raster_header = self.GS + b'v0' + b'\x00' + \
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

    # ---------- Text Alignment ----------
    def center(self):
        return self.ESC + b'a' + b'\x01'

    def left(self):
        return self.ESC + b'a' + b'\x00'

    def bold_on(self):
        return self.ESC + b'E' + b'\x01'

    def bold_off(self):
        return self.ESC + b'E' + b'\x00'

    # ---------- Raw Printer Output ----------
    def print_raw(self, data_bytes):
        hPrinter = win32print.OpenPrinter(self.printer_name)

        try:
            win32print.StartDocPrinter(hPrinter, 1, ("Receipt", None, "RAW"))
            win32print.StartPagePrinter(hPrinter)
            win32print.WritePrinter(hPrinter, data_bytes)
            win32print.EndPagePrinter(hPrinter)
            win32print.EndDocPrinter(hPrinter)

        finally:
            win32print.ClosePrinter(hPrinter)


class ArnisenseReceipt:
    def __init__(self, printer: ThermalPrinter, logo_path):
        self.printer = printer
        self.logo_path = logo_path

    def format_line(self, left, right, width=32):
        space = width - len(left) - len(right)
        if space < 0:
            space = 0
        return left + (" " * space) + right + "\n"

    def build_receipt(self, player1, player2, round_no, score1, score2):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Winner logic
        if score1 > score2:
            winner = player1
        elif score2 > score1:
            winner = player2
        else:
            winner = "DRAW"

        text = ""

        # Tournament Header
        text += "🥋 ARNISENSE ELECTRONIC SCORING 🥋\n"
        text += "--------------------------------\n"
        text += "Official Match Result Receipt\n"
        text += f"Date : {now}\n"
        text += f"Match: {round_no}\n"
        text += "--------------------------------\n\n"

        # Match Scores Box
        text += self.format_line(player1, str(score1))
        text += self.format_line(player2, str(score2))

        text += "\n"
        text += "--------------------------------\n"
        text += self.format_line("ROUND WINNER", winner)
        text += "--------------------------------\n\n"

        text += "Powered by Arnisense Scoring System\n"
        text += "Thank you for participating!\n\n"

        return text

    def print_match(self, player1, player2, round_no, score1, score2):
        printer = self.printer

        logo_bytes = printer.image_to_escpos(self.logo_path)
        content_text = self.build_receipt(
            player1, player2,
            round_no, score1, score2
        )

        receipt_bytes = (
            printer.initialize +
            printer.center() +
            logo_bytes + b"\n" +
            printer.bold_on() +
            content_text.encode("ascii", "ignore") +
            printer.bold_off() +
            printer.cut
        )

        printer.print_raw(receipt_bytes)

        print("Professional Receipt Printed Successfully!")


if __name__ == "__main__":
    printer_engine = ThermalPrinter("POS-58(copy of 6)")

    receipt = ArnisenseReceipt(
        printer_engine,
        r"assets\logo\Arnisense_Logo.png"
    )

    receipt.print_match(
        player1="Red Fighter",
        player2="Blue Fighter",
        round_no=1,
        score1=5,
        score2=3
    )