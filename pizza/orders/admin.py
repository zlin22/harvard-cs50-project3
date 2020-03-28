from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _

# Register your models here.
class OrderItemAdmin(admin.ModelAdmin):
    filter_horizontal = ("menu_item_addition",)

class OrderIsPlacedFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('orders that have been placed')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'is_placed'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            (None, _('Order is placed')),
            ('N', _('Order is NOT placed')),
            ('all', _('All')),
        )
    
    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value
        # to decide how to filter the queryset.
        if self.value() in ('N',):
            return queryset.filter(is_placed=self.value())    
        elif self.value() == None:
            return queryset.filter(is_placed='Y')

class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    filter_horizontal = ("menu_item_addition",)

class OrderAdmin(admin.ModelAdmin):
    list_filter = (OrderIsPlacedFilter, )
    inlines = [OrderItemInLine]
    readonly_fields=('id', )


admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(MenuItemAddition)
admin.site.register(MenuItem)
admin.site.register(Order, OrderAdmin)
