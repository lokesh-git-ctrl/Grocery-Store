from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CustomerDetail)
admin.site.register(Cart)
admin.site.register(OrderPlaced)
admin.site.register(Payment)



