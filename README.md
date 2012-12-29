django-twocheckout
==================

Half-baked 2checkout.com INS support for Django

1. Add urls.py: 
  (r'^2checkout/', include('twocheckout.urls')),

2. Connect to a signal in your app:
  @receiver(signals.order_created)
  def order_created(sender, **kwargs):

3. ???
4. PROFIT!

