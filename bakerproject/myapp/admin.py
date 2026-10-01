from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(Contact)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItems)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=('id','user','full_name','phone','total_amount','payment_method','status','created_at')
    list_filter=('status','payment_method','created_at')
    search_fields=('full_name','phone','user__username')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display=('order','product','quentity','price')
    

    



