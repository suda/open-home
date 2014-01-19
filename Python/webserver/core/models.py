import json
from django.db import models

class Vendor(models.Model):
    """
    Model containing different product vendors
    """
    identifier = models.CharField(max_length=32, db_index=True, unique=True)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return unicode(self.name)

class Product(models.Model):
    """
    Model containing different product models
    """
    ROLE_CHOICES = (
        (1, u'Receiver'),       # Device can only receive commands (i.e. light switch)
        (2, u'Transmitter'),    # Device can only send updates (i.e. thermometer)
        (3, u'Transceiver'),    # Device is bi-directional
    )

    vendor = models.ForeignKey(Vendor)
    identifier = models.CharField(max_length=32, db_index=True, unique=True)
    name = models.CharField(max_length=255)
    role = models.SmallIntegerField(choices=ROLE_CHOICES)

    def __unicode__(self):
        return unicode(self.name)

class Group(models.Model):
    """
    Model containing logical groups for Devices (i.e. rooms or floors)
    """
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return unicode(self.name)

class Device(models.Model):
    """
    Model containing devices added by user
    """
    STATE_CHOICES = (
        (1, u'On'),             # Device confirmed it's On
        (2, u'Off'),            # Device confirmed it's Off
        (3, u'Unknown'),        # Device is write-only or it never reported
        (4, u'Failed'),         # Device updated with some kind of error (check last report)
        (5, u'Battery low'),    # Device updated battery running low
        (6, u'Sleeping'),       # Device is in low-power mode. It won't send/receive anything until woken up
    )

    product = models.ForeignKey(Product)
    group = models.ForeignKey(Group)
    name = models.CharField(max_length=255)
    state = models.SmallIntegerField(choices=STATE_CHOICES, default=3)
    payload = models.TextField()    # JSON payload containing device parameters (i.e. ID)

    def __unicode__(self):
        return unicode(self.group) + u' ' + unicode(self.name)

    def get_last_command(self):
        try:
            return self.command_set.order_by('-added_on')[:1].get()
        except:
            return None

    def get_last_sent_command(self):
        try:
            return self.command_set.order_by('-added_on').filter(sent_on__isnull=False)[:1].get()
        except:
            return None

    def get_last_update(self):
        try:
            return self.update_set.order_by('-received_on')[:1].get()
        except:
            return None

    def get_payload(self):
        return json.loads(self.payload)

class Command(models.Model):
    """
    Model containing commands sent/scheduled for sending
    """
    KIND_CHOICES = (
        (1, u'On'),             # Turn on this device
        (2, u'Off'),            # Turn off this device
        (3, u'Update'),         # Ask device to update it's status
        (4, u'Sleep'),          # Ask device to go into sleep mode
        (5, u'Wake up'),        # Ask device to wake up from sleep mode
    )

    device = models.ForeignKey(Device)
    added_on = models.DateTimeField(auto_now_add=True)
    sent_on = models.DateTimeField(null=True, blank=True)
    kind = models.SmallIntegerField(choices=KIND_CHOICES)

    def __unicode__(self):
        return self.get_kind_display() + u' to ' + unicode(self.device)

    def save(self, command_sent=False, *args, **kwargs):
        super(Command, self).save(*args, **kwargs)

        if not command_sent:
            from .tasks import send_command
            send_command.delay(self.pk)

class Update(models.Model):
    """
    Model containing updates received from devices
    """
    KIND_CHOICES = (
        (1, u'Turned on'),      # Device has turned on
        (2, u'Turned off'),     # Device has turned off
        (3, u'Update'),         # Device updated its status
        (4, u'Went to sleep'),  # Device has went to sleep
        (5, u'Woken up'),       # Device has woken up
    )

    device = models.ForeignKey(Device)
    received_on = models.DateTimeField(auto_now_add=True)
    kind = models.SmallIntegerField(choices=KIND_CHOICES)
    payload = models.TextField(null=True, blank=True)    # JSON payload containing update values