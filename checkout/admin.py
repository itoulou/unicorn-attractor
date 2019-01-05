from django.contrib import admin
from checkout.models import SinglePayment, SinglePaymentLineItem


# Register your models here.
# class SinglePaymentInline(admin.TabularInline):
#     model = PaymentLineItem
    
# class SinglePaymentAdmin(admin.ModelAdmin):
#     inlines = (SinglePaymentInline, )
class FeatureLineAdminInline(admin.TabularInline):
    model = SinglePaymentLineItem

class FeatureAdmin(admin.ModelAdmin):
    inlines = (FeatureLineAdminInline, )
    
admin.site.register(SinglePayment, FeatureAdmin)    