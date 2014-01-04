from __future__ import absolute_import
from celery.utils.log import get_task_logger
from django.conf import settings
from django.utils.timezone import now
from serial import Serial

from core.models import Command
from webserver.celery import app

logger = get_task_logger(__name__)

@app.task
def send_command(pk):
    try:
        command = Command.objects.get(pk=pk)
        identifier = command.device.product.identifier
        classname = identifier.title() + u'Product'
        module = __import__('core.products', fromlist=[classname])
        try:
            cl = getattr(module, classname)
            product = cl()
            serial = Serial(settings.SERIAL_DEVICE, settings.SERIAL_BAUDRATE)
            product.send_command(serial, command, logger)
            serial.close()
            command.sent_on = now()
            command.save(send_command=True)
        except AttributeError:
            logger.error(u'Unsupported product "%s"' % (identifier, ))
    except Command.DoesNotExist:
        logger.error(u'Task delayed but no commands waiting')