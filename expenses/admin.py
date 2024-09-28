from django.contrib import admin

# Register your models here.
from .models import ExpenseType , Expense


class ExpenseTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'expense_type','created_at',)
    list_filter = ('name','expense_type__name', 'created_at','created_by')
    search_fields = ('name', 'expense_type__name', )


admin.site.register(ExpenseType,ExpenseTypeAdmin)
admin.site.register(Expense, ExpenseAdmin)
