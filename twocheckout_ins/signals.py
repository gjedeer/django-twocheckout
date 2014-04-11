from django.dispatch import Signal

order_created = Signal(providing_args = ['order'])
fraud_status_pass = Signal(providing_args = ['order'])
fraud_status_fail = Signal(providing_args = ['order'])
