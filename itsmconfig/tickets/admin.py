from django.contrib import admin
from .models import Status, Priority, Category, Ticket, TicketComment

# Register your models here.


admin.site.register(Status)
admin.site.register(Priority)
admin.site.register(Category)
admin.site.register(Ticket)
admin.site.register(TicketComment)
