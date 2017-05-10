# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from forms import LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group
# 網站首頁
def homepage(request):
    return render_to_response('homepage.html', context_instance=RequestContext(request))

# 網站大廳
def dashboard(request):
        return render_to_response('account/dashboard.html', context_instance=RequestContext(request))
# 使用者登入功能
def user_login(request):
                message = None
                test = ""
                if request.method == "POST":
                                form = LoginForm(request.POST)
                                if form.is_valid():
                                                username = request.POST['username']
                                                password = request.POST['password']
                                                user = authenticate(username=username, password=password)
                                                if user is not None:
                                                                if user.is_active:
                                                                                if user.id == 1:
                                                                                        if user.first_name == "":
                                                                                                user.first_name = "管理員"
                                                                                                user.save()
                                                                                # 登入成功，導到大廳
                                                                                login(request, user)
                                                                                return redirect('/account/dashboard')
                                                                else:
                                                                                message = "帳號未啟用!"
                                                else:
                                                        message = "無效的帳號或密碼!"
                else:
                                form = LoginForm()
                return render_to_response('registration/login.html', {'test': test, 'message': message, 'form': form}, context_instance=RequestContext(request))

# 註冊帳號
def register(request):
        if request.method == 'POST':
                form = RegistrationForm(request.POST)
                if form.is_valid():
                        # Create a new user object but avoid saving it yet
                        new_user = form.save(commit=False)
                        # Set the chosen password
                        new_user.set_password(form.cleaned_data['password'])
                        # Save the User object
                        new_user.save()
                        return render_to_response('registration/register_done.html',{'new_user': new_user}, context_instance=RequestContext(request))
        else:
                form = RegistrationForm()
        return render_to_response('registration/register.html', {'form': form}, context_instance=RequestContext(request))

# 超級管理員可以查看所有帳號
class UserListView(ListView):
    context_object_name = 'users'
    paginate_by = 20
    template_name = 'account/userlist.html'
    
    def get_queryset(self):      
        if self.request.GET.get('account') != None:
            keyword = self.request.GET.get('account')
            queryset = User.objects.filter(Q(username__icontains=keyword) | Q(first_name__icontains=keyword)).order_by('-id')
        else :
            queryset = User.objects.all().order_by('-id')				
        return queryset

def make(request, action, user_id):
    user = User.objects.get(id=user_id)           
    try :
        group = Group.objects.get(name="teacher")	
    except ObjectDoesNotExist :
        group = Group(name="teacher")
        group.save()
    if action == "1":            
        group.user_set.add(user)
    else : 
        group.user_set.remove(user)  
    return redirect("/account/userlist")        
      