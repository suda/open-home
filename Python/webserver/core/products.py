class Clarus01Product:
    def send_command(self, serial, command, logger):
        if (command.kind != 1) and (command.kind != 2):
            logger.error(u'Unsupported command')
        payload = command.device.get_payload()
        message = str(payload['pulse_length']) + str(payload['tri_state_code'])
        message += '01' if command.kind == 1 else '10'
        try:
            serial.write(str(message))
        except:
            logger.debug(u'Error when writing to serial')
        logger.info(u'Command %s sent' % (unicode(command), ))
        logger.debug(u'Message: %s' % (message,))