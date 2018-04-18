from django.contrib import admin

# Register your models here.
from .models import Brand, Glass, booking, GlassInstance, imagepic,Order,OrderDetail,UserDetail

#admin.site.register(Book)
#admin.site.register(Author)
#admin.site.register(Type)

#admin.site.register(BookInstance)
# Define the admin class
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name','brand_pic')
    fields = ['name','brand_pic','detail']

# Register the admin class with the associated model
admin.site.register(Brand, BrandAdmin)
# Register the Admin classes for Book using the decorator
class imagepicAdmin(admin.ModelAdmin):
    list_display = ('bytes','filename','mimetype')
    fields = ['bytes','filename','mimetype']

# Register the admin class with the associated model
admin.site.register(imagepic, imagepicAdmin)



class GlassAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand','pk')
    class GlassInstanceInline(admin.TabularInline):
        model = GlassInstance
    inlines = [GlassInstanceInline]

admin.site.register(Glass, GlassAdmin)

# Register the Admin classes for BookInstance using the decorator


class GlassInstanceAdmin(admin.ModelAdmin):
    list_display = ('glass',  'id')
    fieldsets = (
        (None, {
            'fields': ('glass','imprint', 'id')
        }),
    )
admin.site.register(GlassInstance, GlassInstanceAdmin)
class bookingAdmin(admin.ModelAdmin):
    list_display = ('glass',  'user','bookdate')
    fieldsets = (
        (None, {
            'fields': ('user','glass','booknovalue')
        }),
    )
admin.site.register(booking, bookingAdmin)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user',  'orderdate','active')

admin.site.register(Order, OrderAdmin)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('glass',  'orderno','orderuser')

admin.site.register(OrderDetail, OrderDetailAdmin)
class UserDetailAdmin(admin.ModelAdmin):
    list_display = ('user',  'location')

admin.site.register(UserDetail, UserDetailAdmin)
