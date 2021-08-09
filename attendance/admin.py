import datetime
from django.contrib import admin
from .models import SlackPayload, CheckIn, CheckOut, Timesheet
from django.utils import timezone

class SlackPayloadAdmin(admin.ModelAdmin):
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields] + \
               [field.name for field in obj._meta.many_to_many]

class CheckInInline(admin.TabularInline):
    model = CheckIn
    fields = ('time', 'message')
    extra = 1

class CheckOutInline(admin.TabularInline):
    model = CheckOut
    fields = ('time', 'message')
    extra = 1

class TimeSheetAdmin(admin.ModelAdmin):
    readonly_fields = ('name','date')
    list_display = ('date', 'name', 'last_check_in', 'last_check_out', 'total_work_hour')
    list_filter = ('name', 'date')
    inlines = [CheckInInline, CheckOutInline]

    @admin.display(description='Last check in')
    def last_check_in(self, obj):
        check_in = CheckIn.objects.filter(timesheet=obj).last()
        try:
            return check_in.time
        except CheckIn.DoesNotExist:
            return "-"
    @admin.display(description='Last check out')
    def last_check_out(self, obj):
        check_out = CheckOut.objects.filter(timesheet=obj).last()
        try:
            return check_out.time
        except CheckOut.DoesNotExist:
            return "-"

    @admin.display(description='Total work hour')
    def total_work_hour(self, obj):
        check_out = CheckOut.objects.filter(timesheet=obj)
        check_in = CheckIn.objects.filter(timesheet=obj)
        date = datetime.date(1, 1, 1)

        total = datetime.timedelta(0)
        for i in range(check_out.count()):
            start_time = check_in[i].time
            stop_time = check_out[i].time
            datetime1 = datetime.datetime.combine(date, start_time)
            datetime2 = datetime.datetime.combine(date, stop_time)
            time_elapsed = datetime2 - datetime1

            total = total + time_elapsed    

        return str(total).split('.')[0]


admin.site.register(SlackPayload, SlackPayloadAdmin)
admin.site.register(Timesheet, TimeSheetAdmin)