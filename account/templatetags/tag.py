# -*- coding: UTF-8 -*-
from django import template
from django.contrib.auth.models import Group 
from teacher.models import Classroom

register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, group_name):
    group =  Group.objects.get(name=group_name) 
    return group in user.groups.all() 
  
@register.filter()
def teacher_id(classroom_id):
    if classroom_id > 0 :
        teacher_id = Classroom.objects.get(id=classroom_id).teacher_id
        return teacher_id
    else : 
        return 0