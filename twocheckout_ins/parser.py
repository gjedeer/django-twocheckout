import hashlib
from django.conf import settings
import datetime
from decimal import Decimal

class ChecksumError(ValueError):
    pass

def parse(post, validate_md5=True):
    if validate_md5 and not checksum(post):
        raise ChecksumError('Invalid md5')
    elif not validate_md5:
        print "Warning: not checking MD5 of 2co order"
    if post['message_type'] == 'ORDER_CREATED':
        return OrderCreatedMsg(post)


def checksum(post):
    """
    Return true if md5 hash is valid
    @param dict post Dictionary of post data 
    """
    m = hashlib.md5()
    m.update(post['sale_id'])
    m.update(post['vendor_id'])
    m.update(post['invoice_id'])
    m.update(settings.TWOCHECKOUT_SECRET)
    return m.hexdigest().upper() == post['md5_hash']

class TwoCheckoutMsg:
    def parse_callback_fields(self, post, fields, callback):
        for field in fields:
            setattr(self, field, callback(post[field]))

    def parse_integer_fields(self, post, fields):
        self.parse_callback_fields(post, fields, int)

    def parse_string_fields(self, post, fields):
        self.parse_callback_fields(post, fields, unicode)

    def parse_date_fields(self, post, fields):
        self.parse_callback_fields(post, fields, 
                                   lambda d: datetime.datetime.strptime(d, '%Y-%m-%d %H:%M:%S'))

    def parse_decimal_fields(self, post, fields):
        self.parse_callback_fields(post, fields, Decimal)

class OrderItem(TwoCheckoutMsg):
    def parse_callback_fields(self, post, fields, callback):
        for field in fields:
            setattr(self, field, callback(post['item_' + field + '_' + str(self.n)]))

    def __init__(self, post, n):
        self.n = n
        self.parse_string_fields(post, [
            'name',
            'id',
            'type',
            'duration',
            'recurrence',
            'rec_status',
        ])
        self.parse_decimal_fields(post, [
            'list_amount',
            'usd_amount',
            'cust_amount',
        ])
        if len(self.recurrence) > 0:
            self.parse_decimal_fields(post, [
                'rec_list_amount',
                'rec_install_billed'
            ])
            self.parse_date_fields(post, [
                'rec_date_next',
            ])

class OrderCreatedMsg(TwoCheckoutMsg):
    def __init__(self, post):
        self.parse_date_fields(post, [
            'timestamp',
            'sale_date_placed',
#            'auth_exp',
        ])
        self.parse_integer_fields(post, [
            'message_id',
            'key_count',
            'vendor_id',
            'sale_id',
            'invoice_id',
            'recurring',
            'item_count'
        ])

        self.parse_decimal_fields(post, [
            'invoice_list_amount',
            'invoice_usd_amount',
            'invoice_cust_amount',
        ])

        self.parse_string_fields(post, [
            'message_description',
            'vendor_order_id',
            'payment_type',
            'list_currency',
            'cust_currency',
            'invoice_status',
            'fraud_status',
            'customer_first_name',
            'customer_last_name',
            'customer_name',
            'customer_email',
            'customer_phone',
            'customer_ip',
            'customer_ip_country',
            'bill_street_address',
            'bill_street_address2',
            'bill_city',
            'bill_state',
            'bill_postal_code',
            'bill_country',
            'ship_status',
            'ship_tracking_number',
            'ship_name',
            'ship_street_address',
            'ship_street_address2',
            'ship_city',
            'ship_state',
            'ship_postal_code',
            'ship_country'
        ])

        self.items = []
        for i in xrange(1,self.item_count+1):
            self.items.append(OrderItem(post, i))
