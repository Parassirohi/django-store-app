
from django.dispatch import Signal

# creating a custom signals, although we already have in built signals
# we define our signals here

order_created = Signal()  # signals() is simply an instance of signal class,
# now we need to fire this signals when order is created
