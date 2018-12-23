from django.contrib import admin
from checkout.models import Payment, PaymentLineItem

# Register your models here.
class SinglePaymentInline(admin.TabularInline):
    model = PaymentLineItem
    
class SinglePaymentAdmin(admin.ModelAdmin):
    inlines = (SinglePaymentInline, )
    
admin.site.register(Payment, SinglePaymentAdmin)    