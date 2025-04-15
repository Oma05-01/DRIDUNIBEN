from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.db.models import Count, Q
from bson import ObjectId
from django.http import Http404

def admin_dashboard(request):
    query = request.GET.get('q', '')

    articles = Article.objects.all()
    for article in articles:
        print("Article ID:", article._id)

    if query:
        articles = articles.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

    category_counts = {
        'Research': Article.objects.filter(category='Research').count(),
        'Innovation': Article.objects.filter(category='Innovation').count(),
        'Development': Article.objects.filter(category='Development').count(),
    }

    recent_articles = articles.order_by('-publish_date')[:5]

    context = {
        'category_counts': category_counts,
        'recent_articles': recent_articles,
        'query': query,
    }

    return render(request, 'dashboard.html', context)


def faculty_list_view(request):
    faculties = Faculty.objects.all()
    return render(request, 'faculty_list.html', {'faculties': faculties})

def faculty_detail_view(request, code):
    faculty = get_object_or_404(Faculty, pk=code)
    return render(request, 'faculty_detail.html', {'faculty': faculty})


# Department Views
def department_list_view(request):
    departments = Department.objects.all()
    return render(request, 'department_list.html', {'departments': departments})

def department_detail_view(request, code):
    department = get_object_or_404(Department, pk=code)
    return render(request, 'department_detail.html', {'department': department})


def create_article(request):
    if request.method == 'POST':
        print("POST data:", request.POST)
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.owner = request.user
            article.save()  # Save first to create the article

            # Manually handle contributors
            contributor_ids = request.POST.getlist('contributors')
            if contributor_ids and contributor_ids != ['None'] and contributor_ids != ['on']:
                # Convert string IDs to ObjectIds
                obj_ids = [ObjectId(cid) for cid in contributor_ids if cid]
                contributors = Contributor.objects.filter(_id__in=obj_ids)
                for contributor in contributors:
                    article.contributors.add(contributor)

            return redirect('article_list')
    else:
        form = ArticleForm()

    return render(request, 'create_article.html', {'form': form})


def article_list(request):
    articles = Article.objects.all()
    query = request.GET.get('q')
    if query:
        articles = articles.filter(title__icontains=query)
    return render(request, 'article_list.html', {'articles': articles})


def article_detail(request, pk):

    try:
        article = Article.objects.select_related('department', 'owner').prefetch_related('contributors').get(_id=ObjectId(pk))
        contributors = article.contributors.all()
        print('contributor is ', Article.objects.get(_id=ObjectId(pk)).contributors.all())
    except (Article.DoesNotExist, Exception):
        raise Http404("Article not found")
    return render(request, 'article_detail.html', {'article': article, 'contributors': contributors})