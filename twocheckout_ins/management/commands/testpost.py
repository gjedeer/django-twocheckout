from django.core.management.base import BaseCommand, CommandError
import pickle
from twocheckout_ins.parser import parse

class Command(BaseCommand):
    args = '<filename>'
    help = 'Load request from a file and process'

    def handle(self, *args, **options):
        file = open(args[0])
        request = pickle.load(file)
        file.close()

        post = {key: request['POST'][key][0] for key in request['POST']}

        parse(post, False)
