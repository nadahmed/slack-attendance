from django.contrib import admin

from leave.models import LeaveType, LeaveForm, Approval

@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    model = LeaveType
    
@admin.register(Approval)
class ApprovalAdmin(admin.ModelAdmin):
    model = Approval

@admin.register(LeaveForm)
class LeaveFormAdmin(admin.ModelAdmin):
    model = LeaveForm
    exclude = ('approval',)

# admin.site.register(Application, ApplicationAdmin)
# admin.site.register(Approval, ApprovalAdmin)