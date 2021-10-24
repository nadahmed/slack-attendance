from django.contrib import admin

from leave.models import LeaveType

@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    model = LeaveType

# class ApprovalAdmin(admin.StackedInline):
#     model = Approval

# class ApplicationAdmin(admin.ModelAdmin):
#     model = Application
#     inlines = [ApprovalAdmin]

# admin.site.register(Application, ApplicationAdmin)
# admin.site.register(Approval, ApprovalAdmin)