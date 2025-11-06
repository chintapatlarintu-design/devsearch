from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import conf
from django.db.models import Q
from .models import Profile, Skill, Message
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from django.core.exceptions import ObjectDoesNotExist
from .utils import searchProfiles, paginateProfiles
from django.shortcuts import render, redirect, get_object_or_404



from .models import Message


# Create your views here.


    
# Create your views here.
def loginUser(request):
    page = 'login'

  
    if request.user.is_authenticated:
        return redirect('profiles')


    if request.method == 'POST':
        # print(request.POST) 
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')
           
            # messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET ['next'] if 'next' in request.GET else 'account')
        else:
            # print('Username OR password is incorrect')
            messages.error(request, 'Username OR password is incorrect')

    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out')
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')

            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request, 'An error occurred during registration')

    context = {'page': page , 'form': form}
    return render(request, 'users/login_register.html',context)     

# def create_message(request):
#     if request.method == 'POST':
#         recipient_id = request.POST.get('recipient_id')
#         subject = request.POST.get('subject')
#         body = request.POST.get('body')

#         try:
#             recipient = Profile.objects.get(id=recipient_id)
#         except ObjectDoesNotExist:
#             messages.error(request, 'Recipient does not exist.')
#             return redirect('inbox')

#         message = Message(
#             sender=request.user.profile,
#             recipient=recipient,
#             subject=subject,
#             body=body
#         )
#         message.save()
#         messages.success(request, 'Message sent successfully!')
#         return redirect('inbox')



def profiles(request):
    profiles, serch_query = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request, profiles, 3)

    context = {'profiles': profiles, 'search_query': serch_query, 
               'custom_range': custom_range}
    return render(request, 'users/profiles.html' , context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="") 

    context = {'profile': profile, 'topSkills': topSkills, 'otherSkills': otherSkills }
    return render(request, 'users/user-profile.html', context)

skill = "profile.skill_set.all()"


# @login_required(login_url='login')
# def userAccount(request):
#      Profile = request.user.profile

#      context = "{%'profile': Profile,'Skills': skills %}"
#      return render(request, 'users/account.html', context)

@login_required(login_url='login')
def userAccount(request):
    """
    Displays the current logged-in user's account page.
    This function was corrected to use a dictionary for context.
    """
    # Use lowercase for the variable name for convention
    profile = request.user.profile

    Skills = profile.skill_set.all()
     

    # Fetch all skills associated with the profile
    skills = profile.skill_set.all()

    projects = profile.project_set.all()

    # CORRECTED: context is defined as a Python DICTIONARY
    context = {
        'profile': profile,'Skills': Skills, 'projects': projects}
    
    
    return render(request, 'users/account.html', context)

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = { 'form': form}
    return render(request, 'users/profile_form.html', context)




@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile

    form = SkillForm() 
    
    # This is the line where the error was pointing (or close to it)
    if request.method == 'POST':
        # ALL code in this block MUST be indented (4 spaces is standard)
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save() 
            messages.success(request, 'Skill was added successfully!')
            return redirect('account')
    
    # This code is outside the 'if' block
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)



@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill) 
    
    # This is the line where the error was pointing (or close to it)
    if request.method == 'POST':
        # ALL code in this block MUST be indented (4 spaces is standard)
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
           
            form.save() 
            messages.success(request, 'Skill was added successfully!')
            return redirect('account')
    
    # This code is outside the 'if' block
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)

def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted successfully!')
        return redirect('account')

    context = {'object': skill}
    return render(request, 'delete_template.html', context)


    
@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)




# @login_required(login_url='login')
# def viewMessage(request, pk):
#     profile = request.user.profile
#     message = profile.messages.get(id=pk)

#     if message.is_read == False:
#         message.is_read = True
#         message.save()
    
#     context = {'message': message}
#     return render(request, 'users/message.html', context)




    
@login_required(login_url='login')
def viewMessage(request, pk):
    try:
        message = Message.objects.get(id=pk)
        
        if message.recipient == request.user:
            message.is_read = True
            message.save()
            context = {'message': message}
            return render(request, 'users/message.html', context)
        else:
            messages.error(request, 'You do not have permission to view this message')
            return redirect('inbox')
            
    except Message.DoesNotExist:
        messages.error(request, 'Message not found')
        return redirect('inbox')

@login_required(login_url='login')
def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Your message was successfully sent!')
            return redirect('user-profile', pk=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', context)