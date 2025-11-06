
from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateProjects(request, projects, results):
    page = request.GET.get('page')
    results_per_page = results

    paginator = Paginator(projects, results_per_page)
    try:
        projects_page = paginator.page(page)
    except PageNotAnInteger:
        projects_page = paginator.page(1)
    except EmptyPage:
        projects_page = paginator.page(paginator.num_pages)

    current_page = projects_page.number
    leftIndex = current_page - 4 if current_page - 4 > 1 else 1
    rightIndex = current_page + 5 if current_page + 5 < paginator.num_pages else paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, projects_page

def searchProjects(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_query)  

    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)
    ) 

    return projects, search_query
