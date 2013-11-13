"""
Simple Web server used to send Tri-State commands to Arduino Bridge via serial port.

Part of Open Home https://github.com/appsome/open-home
"""

import sys, getopt, os
from os import path
from time import sleep

import tornado.ioloop
import tornado.web
from tornado import template
from serial import Serial
from serial.tools import list_ports

class MainHandler(tornado.web.RequestHandler):
    def get(self):
    	loader = template.Loader(path.join(path.dirname(__file__), 'templates'))
        self.write(loader.load("index.html").generate())

class SendHandler(tornado.web.RequestHandler):
    def get(self):
        message = self.get_argument('message')
        
        # Try to reopen connection
        try:
            serial.getCTS()
        except IOError:
            serial.close()
            serial.open()

        serial.write(str(message))
        print 'Sent ' + str(message)

        sleep(0.5)

        self.set_header('Content-Type', 'application/json')
        self.write('{ response: "ok" }')

application = tornado.web.Application([    
    (r"/", MainHandler),
    (r"/api/send", SendHandler),
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': path.join(path.dirname(__file__), 'static')}),
])

device = None
serial = None
baudrate = 9600
port = 9876

def list_serial_ports():
    # Windows
    if os.name == 'nt':
        # Scan for available ports.
        available = []
        for i in range(256):
            try:
                s = serial.Serial(i)
                available.append('COM'+str(i + 1))
                s.close()
            except serial.SerialException:
                pass
        return available
    else:
        # Mac / Linux
        return [port[0] for port in list_ports.comports()]

def main(argv):
    global device
    global serial
    global baudrate
    global port
    list_ports = False

    usage = 'usage: python ' + path.basename(__file__) + ' [-h] [-l] [-p port] [-b baudrate] <serialdevice>'

    try:
        opts, args = getopt.getopt(argv, 'hlp:b:', ['port=', 'baudrate='])
    except getopt.GetoptError:
        print usage
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print usage
            sys.exit()
        if opt == '-l':
            list_ports = True
        elif opt in ('-p', '--port'):
            port = int(arg)
        elif opt in ('-b', '--baudrate'):
            baudrate = int(arg)

    if list_ports:
        for available_port in list_serial_ports():
            print available_port
        sys.exit()        
    else:
        if len(argv) == 0:
            print usage
            sys.exit(2)

        device = args[0]
        serial = Serial(device, baudrate)
        application.listen(port)
        tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
   main(sys.argv[1:])