from gpiozero import Servo, OutputDevice
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

# Configuration des servomoteurs et de l'électrovanne
servo_flush = Servo(17)
servo_seeds = Servo(27)
electrovalve_water = OutputDevice(22)

def flush_glass():
    servo_flush.max()
    time.sleep(1)
    servo_flush.min()

def dispense_seeds():
    servo_seeds.max()
    time.sleep(3)
    servo_seeds.min()

def add_water():
    electrovalve_water.on()
    time.sleep(2)
    electrovalve_water.off()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/flush':
            flush_glass()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Glass flushed")
        elif self.path == '/seeds':
            dispense_seeds()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Seeds dispensed")
        elif self.path == '/water':
            add_water()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Water added")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Command not found")

server_address = ('', 8080)
httpd = HTTPServer(server_address, RequestHandler)
print("Server running on port 8080...")
httpd.serve_forever()