from django.dispatch import Signal

order_created = Signal(providing_args = ['order'])
