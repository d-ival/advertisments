from django_filters import rest_framework as filters

from advertisements.models import Advertisement, AdvertisementStatusChoices

class AdvertismentFilterBackend(filters.DjangoFilterBackend):

    def filter_queryset(self, request, queryset, view):
        allowed_by_status = queryset.exclude(status=AdvertisementStatusChoices.DRAFT)
        if not request.user.is_anonymous:
            allowed_by_owner = queryset.filter(creator=request.user, status=AdvertisementStatusChoices.DRAFT)
            queryset = allowed_by_status | allowed_by_owner
        else:
            queryset = allowed_by_status
        return super().filter_queryset(request, queryset, view)


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    status = filters.ChoiceFilter(choices=AdvertisementStatusChoices.choices)
    created_at = filters.DateFromToRangeFilter(field_name='created_at')

    class Meta:
        model = Advertisement
        fields = ("id", "status", "created_at", "creator")
