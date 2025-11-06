from django.db.models import Q
from .models import Profile, Skill
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateProfiles(request, profiles, results):
    page = request.GET.get('page')
    results_per_page = results

    paginator = Paginator(profiles, results_per_page)
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        profiles = paginator.page(1)
    except EmptyPage:
        profiles = paginator.page(paginator.num_pages)

    current_page = profiles.number
    leftIndex = current_page - 4 if current_page - 4 > 1 else 1
    rightIndex = current_page + 5 if current_page + 5 < paginator.num_pages else paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, profiles




def searchProfiles(request):
    serch_query =  ''

    if request.GET.get('search_query'):
        serch_query = request.GET.get('search_query')

        print('SERCH:', serch_query)

    skills= Skill.objects.filter(name__icontains=serch_query)

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=serch_query) | 
        Q(short_intro__icontains=serch_query) |
        Q(skill__in=skills)
        )
    
    return profiles, serch_query