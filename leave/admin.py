from django.contrib import admin

from leave.models import Category, Application, Approval

class TypeAdmin(admin.ModelAdmin):
    model = Category

class ApprovalAdmin(admin.StackedInline):
    model = Approval

class ApplicationAdmin(admin.ModelAdmin):
    model = Application
    inlines = [ApprovalAdmin]

admin.site.register(Category, TypeAdmin)
admin.site.register(Application, ApplicationAdmin)
# admin.site.register(Approval, ApprovalAdmin)