import django_filters
from .models import Community


class CommunityFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    content = django_filters.CharFilter(lookup_expr='icontains')
    author = django_filters.CharFilter(field_name='author__username', lookup_expr='icontains')

    class Meta:
        model = Community
        fields = ['category', 'title', 'content', 'author']

