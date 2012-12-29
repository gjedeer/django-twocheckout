from django.core.management.base import BaseCommand, CommandError
import pickle
from twocheckout.parser import parse
from twocheckout import signals

class Command(BaseCommand):
    args = '<filename>'
    help = 'Load request from a file and process'

    def handle(self, *args, **options):
        file = open(args[0])
        object = pickle.load(file)
        file.close()

        signals.order_created.send(sender=None, order=object)
