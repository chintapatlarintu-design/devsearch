from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Project
from .forms import ProjectForm, ReviewForm
from .utils import searchProjects, paginateProjects

def searchProjects(request):
    search_query = request.GET.get('search', '')
    if search_query:
        projects = Project.objects.filter(title__icontains=search_query)
    else:
        projects = Project.objects.all()
    return projects, search_query

def projects(request):
    projects, search_query = searchProjects(request)

    page = request.GET.get('page')
    results_per_page = 3
    paginator = Paginator(projects, results_per_page)

    try:
        projects_page = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects_page = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects_page = paginator.page(page)

    current_page = int(page)
    leftIndex = current_page - 4
    rightIndex = current_page + 5

    if leftIndex < 1:
        leftIndex = 1
    if rightIndex > paginator.num_pages + 1:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    context = {
        'projects': projects_page,
        'search_query': search_query,
        'paginator': paginator,
        'custom_range': custom_range,
    }
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.project = projectObj
            review.owner = request.user.profile
            review.save()

            projectObj.getVoteCount  # Ensure this is a method call if intended (e.g., projectObj.getVoteCount())
            messages.success(request, 'Your review was successfully submitted!')

            return redirect('project', pk=projectObj.id)

    return render(request, 'projects/single-project.html', {'project': projectObj, 'form': form})

@login_required(login_url="login")
def createproject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('projects')

    return render(request, 'projects/project_form.html', {'form': form})

@login_required(login_url="login")
def updateproject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')

    return render(request, 'projects/project_form.html', {'form': form})

@login_required(login_url="login")
def deleteproject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)  # Fixed calling get() on profile.project_set queryset

    if request.method == 'POST':
        project.delete()
        return redirect('projects')

    return render(request, 'projects/delete_template.html', {'object': project})

def projects(request):
    
    # 1. Search and Paginator setup

    projects, serch_query = searchProjects(request)
   
    page = request.GET.get('page')
    results = 3
    paginator = Paginator(projects, results)

    # 2. Handle Page Exceptions (Assigning 'projects' and getting 'current_page')
    try:

        projects = paginator.page(page)
    except PageNotAnInteger:
        # Default to page 1 if page number is not an integer
        page = 1 
        projects = paginator.page(page)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        page = paginator.num_pages
        projects = paginator.page(page)
									  
							
    # Convert the effective page number to an integer for calculations
    # Note: 'page' is now guaranteed to be a string or an integer (from exceptions)
    current_page = int(page)
    
   
    leftIndex = current_page - 4
    rightIndex = current_page + 5

    # Adjust the left boundary
    if leftIndex < 1:
        leftIndex = 1

    # Adjust the right boundary
    if rightIndex > paginator.num_pages + 1:
        # If the right index exceeds the total pages, set it to one past the last page
        rightIndex = paginator.num_pages + 1 

    custom_range = range(leftIndex, rightIndex)

    # 4. Render the context
    context = {'projects': projects, 'search_query': serch_query, 'paginator': paginator, 'custom_range': custom_range}
    return render(request, 'projects/projects.html', context)

 
def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    # Tags = projectObj.tags.all()
    # print("projectObj:", projectObj)
    return render(request, 'projects/single-project.html',{'project': projectObj} )


@login_required(login_url="login")
def createproject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        # print(request.POST)
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project =form.save(commit=False)
            project.owner = profile
            project.save() 
            return redirect('projects')

    context={'form': form}
    return render (request, "projects/project_form.html", context)

@login_required(login_url="login")
def updateproject(request, pk):
    profile = request.user.profile
    project= profile.project_set.get(id=pk) 
    form = ProjectForm(instance=project) 

    if request.method == 'POST':
        # print(request.POST)
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')

    context={'form': form}
    return render (request, "projects/project_form.html", context)
    
@login_required(login_url="login")
def deleteproject(request, pk):
    profile = request.user.profile
    # FIX: Use get() on the queryset, not objects.get()
    project = profile.project_set.get(id=pk) 
    # project = Project.bjects.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'object': project}
    return render(request, 'projects/delete_template.html', context)