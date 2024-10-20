from django.contrib import admin

# Register your models here.
from .models import asset, playbook, policy, scanResult, ticket, vulnerability,scan
admin.site.register(ticket)
admin.site.register(asset)
admin.site.register(vulnerability)
admin.site.register(policy)
admin.site.register(playbook)
admin.site.register(scan)
admin.site.register(scanResult)

