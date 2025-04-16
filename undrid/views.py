from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from .forms import *
from django.db.models import Count, Q
from bson import ObjectId
from django.http import Http404
from django.contrib import messages

def admin_dashboard(request):
    query = request.GET.get('q', '')

    articles = Article.objects.all()
    for article in articles:
        print("Article ID:", article._id, "Article contributor: ", article.contributors.all())

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
            article.save()

            form.save_m2m()  # ✅ This will save contributors properly

            return redirect('article_list')
        else:
            print("Form Errors:", form.errors)
    else:
        form = ArticleForm()

    return render(request, 'create_article.html', {'form': form})


def article_list(request):
    articles = Article.objects.all()
    query = request.GET.get('q')
    if query:
        articles = articles.filter(title__icontains=query)
    return render(request, 'article_list.html', {'articles': articles})


def edit_article(request, pk):
    try:
        article = Article.objects.get(_id=ObjectId(pk))
    except (Article.DoesNotExist, Exception):
        raise Http404("Article not found")

    # Check if user is the owner
    if request.user != article.owner:
        messages.error(request, "You don't have permission to edit this article.")
        return redirect('article_list')

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "Article updated successfully!")
            return redirect('article_detail', pk=pk)
    else:
        form = ArticleForm(instance=article)

    return render(request, 'edit_article.html', {'form': form, 'article': article})


def delete_article(request, pk):
    try:
        article = Article.objects.get(_id=ObjectId(pk))
    except (Article.DoesNotExist, Exception):
        raise Http404("Article not found")

    # Check if user is the owner
    if request.user != article.owner:
        messages.error(request, "You don't have permission to delete this article.")
        return redirect('article_list')

    if request.method == 'POST':
        article.delete()
        messages.success(request, "Article deleted successfully!")
        return redirect('article_list')

    return render(request, 'delete_article_confirm.html', {'article': article})


def toggle_publish(request, pk):
    try:
        article = Article.objects.get(_id=ObjectId(pk))
    except (Article.DoesNotExist, Exception):
        return JsonResponse({'status': 'error', 'message': 'Article not found'}, status=404)

    # Check if user is the owner
    if request.user != article.owner:
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)

    # Toggle the published status
    article.is_published = not article.is_published
    article.save()

    status = 'published' if article.is_published else 'unpublished'
    return JsonResponse({
        'status': 'success',
        'is_published': article.is_published,
        'message': f'Article {status} successfully!'
    })


def article_detail(request, pk):

    try:
        article = Article.objects.select_related('department', 'owner').prefetch_related('contributors').get(_id=ObjectId(pk))
        contributors = article.contributors.all()
        print('contributor is ', Article.objects.get(_id=ObjectId(pk)).contributors.all())
    except (Article.DoesNotExist, Exception):
        raise Http404("Article not found")
    return render(request, 'article_detail.html', {'article': article, 'contributors': contributors})


def search_contributors(request):
    query = request.GET.get('q', '')
    contributors = Contributor.objects.all()
    if query:
        contributors = contributors.filter(name__icontains=query) | contributors.filter(email__icontains=query)
    return render(request, 'search_contributors.html', {'contributors': contributors, 'query': query})

def add_contributor(request):
    if request.method == 'POST':
        form = ContributorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('contributor_list')
    else:
        form = ContributorForm()
    return render(request, 'add_contributor.html', {'form': form})


def contributor_list(request):
    query = request.GET.get('q', '')

    if query:
        contributors = Contributor.objects.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(bio__icontains=query)
        ).order_by('name')
    else:
        contributors = Contributor.objects.all().order_by('name')

    context = {
        'contributors': contributors,
        'search_query': query
    }
    return render(request, 'contributor_list.html', context)


def view_contributor(request, pk):
    contributor = get_object_or_404(Contributor, _id=ObjectId(pk))

    # Count where they are the lead researcher
    lead_count = Article.objects.filter(researcher=contributor).count()

    # Count where they are a contributor (but not lead)
    contribution_count = Article.objects.filter(contributors=contributor).exclude(researcher=contributor).count()

    return render(request, 'view_contributor.html', {'contributor': contributor, 'lead_count': lead_count,
        'contribution_count': contribution_count,})


def articles_by_researcher(request, pk):
    contributor = get_object_or_404(Contributor, _id=ObjectId(pk))

    articles = Article.objects.filter(researcher=contributor)

    return render(request, 'articles_by_researcher.html', {
        'contributor': contributor,
        'articles': articles
    })