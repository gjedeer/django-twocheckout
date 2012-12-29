from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
import pickle
import syslog

import parser
import signals

@csrf_exempt
def ins(request):
    obj = {'GET': dict(request.GET), 'POST': dict(request.POST)}
    pickle.dump(obj, open('/tmp/%s.pickle' % datetime.datetime.now().strftime('%Y-%m-%d-%I-%M-%S'), 'w'))
    try:
        parsed = parser.parse(request.POST)
        pickle.dump(parsed, open('/tmp/parsed_%s.pickle' % datetime.datetime.now().strftime('%Y-%m-%d-%I-%M-%S'), 'w'))
        signals.order_created.send(parsed)
    except parser.ChecksumError, e:
        syslog.syslog(str(e))
    return HttpResponse('hello')
