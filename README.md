django-twocheckout
==================

Half-baked 2checkout.com INS support for Django

1. Add urls.py code 
<pre>
  (r'^2checkout/', include('twocheckout.urls')),
</pre>

2. Add /2checkout/ins to notifications tab in 2co
3. Add the following to settings.py: <code>TWOCHECKOUT_SECRET = 'tango'</code>

4. Connect to a signal in your app:
<pre>
  from twocheckout import signals
  @receiver(signals.order_created)
  def order_created(sender, **kwargs):
    ...
</pre>


