# -*- coding: utf-8 -*-
import os
import serial
from serial.tools import list_ports
from django.core.management.base import BaseCommand

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

class Command(BaseCommand):
    args = ''
    help = 'Lists all available serial ports'

    def handle(self, *args, **options):
        for available_port in list_serial_ports():
            print available_port