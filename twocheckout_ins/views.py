from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from parser import parse,OrderCreatedMsg, FraudResultMsg
import datetime
import pickle
import syslog

import parser
import signals

@csrf_exempt
def ins(request):
    obj = {'GET': dict(request.GET), 'POST': dict(request.POST)}
    try:
        pickle.dump(obj, open('/srv/massivescale.net/pickles/%s.pickle' % datetime.datetime.now().strftime('%Y-%m-%d-%I-%M-%S'), 'w'))
    except Exception, e:
        print "ERROR SAVING POST PICKLE DUMP"
        print e
    try:
        parsed = parser.parse(request.POST)
        if not parsed:
            return HttpResponse('yeah')
        try:
            pickle.dump(parsed, open('/srv/massivescale.net/pickles/parsed_%s.pickle' % datetime.datetime.now().strftime('%Y-%m-%d-%I-%M-%S'), 'w'))
        except Exception, e:
            print "ERROR SAVING PARSED PICKLE DUMP"
            print e
        
        parsed.send_signal()

    except parser.ChecksumError, e:
        syslog.syslog(str(e))
        print e
    return HttpResponse('hello')
