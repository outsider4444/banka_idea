import django_filters

from banka_idea.models import Idea


class IdeaFilter(django_filters.FilterSet):
    class Meta:
        model = Idea