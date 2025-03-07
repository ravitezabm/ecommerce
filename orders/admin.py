from django.contrib import admin
from orders.models import Order,OrderedItem

class OrderAdmin(admin.ModelAdmin):
    list_filter = [
        "owner",
        "order_status",
        "created_at"
    ]
    search_fields = [
        "owner",
        "id"
    ]

admin.site.register(Order,OrderAdmin)
