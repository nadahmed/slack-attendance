from django.contrib import admin
from .models import SlackPayload, CheckIn, CheckOut, Timesheet, SlackUser


@admin.register(SlackUser)
class SlackUserAdmin(admin.ModelAdmin):
    pass

class SlackPayloadAdmin(admin.ModelAdmin):
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields] + \
               [field.name for field in obj._meta.many_to_many]

class CheckInInline(admin.TabularInline):
    model = CheckIn
    fields = ('time', 'message')
    extra = 0

class CheckOutInline(admin.TabularInline):
    model = CheckOut
    fields = ('time', 'message')
    extra = 0

class TimeSheetAdmin(admin.ModelAdmin):
    
    list_display = ('date', 'name', 'first_check_in', 'last_check_out', 'total_work_hour', 'is_checked_out')
    list_filter = ('name', 'date')
    inlines = [CheckInInline, CheckOutInline]

    @admin.display(description='First check in')
    def first_check_in(self, obj):
        check_in = CheckIn.objects.filter(timesheet=obj).first()
        if check_in != None:
            return check_in.time
        else:
            return "-"
    @admin.display(description='Last check out')
    def last_check_out(self, obj):
        check_out = CheckOut.objects.filter(timesheet=obj).last()
        if check_out != None:
            return check_out.time
        else:
            return "-"

    @admin.display(description='Total work hour')
    def total_work_hour(self, obj):
        return obj.total_work_hour()

    @admin.display(description='Checked out?')
    def is_checked_out(self, obj) -> bool:
        return obj.is_checked_out()
    is_checked_out.boolean = True

admin.site.register(SlackPayload, SlackPayloadAdmin)
admin.site.register(Timesheet, TimeSheetAdmin)