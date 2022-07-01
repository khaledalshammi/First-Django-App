from django.contrib import admin
from .models import Board,Topic,Post
from django.contrib.auth.models import Group
admin.site.site_header = "khaled"
admin.site.site_title = "me"
class TopicAdmin(admin.ModelAdmin):
    fields = ('subject','board') #to display inside it
    list_display = ('subject','c_s',) #columns
    list_filter = ('created_by','board')
    search_fields = ('board','created_by')
    def c_s(self,obj):
        return "{} - {}".format(obj.subject,obj.board)
admin.site.register(Board)
admin.site.register(Topic,TopicAdmin)
admin.site.register(Post) 
admin.site.unregister(Group)