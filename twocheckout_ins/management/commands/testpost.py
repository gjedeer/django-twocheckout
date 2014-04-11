from django.core.management.base import BaseCommand, CommandError
import pickle
from twocheckout_ins.parser import parse,OrderCreatedMsg, FraudResultMsg
from twocheckout_ins import signals

class Command(BaseCommand):
    args = '<filename>'
    help = 'Load request from a file and process'

    def handle(self, *args, **options):
        file = open(args[0])
        request = pickle.load(file)
        file.close()

        post = {key: request['POST'][key][0] for key in request['POST']}

        parsed = parse(post, False)
        print parsed
        ins = self # leave it alone!
        parsed.send_signal()

