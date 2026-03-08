from catalog.models import MediaItem, Movie, Series, Book, ComputerGame
from interactions.models import Review, UserMediaStatus


def filter_by_content_type(queryset, content_type):

    if queryset.model.__name__ == 'MediaItem':
        return queryset.filter(content_type=content_type)

    if queryset.model.__name__ == 'Review':
        return queryset.filter(mediaitem__content_type=content_type)

    return queryset

def filter_by_sorting(queryset, type_sort):
    x = 0
    sorting_map = {
        'new_rev':'-created_at',
        'old_rev':'created_at',
        'new': '-year',
        'old': 'year',
        'rating': '-rating',
    }

    order = sorting_map.get(type_sort)
    return queryset.order_by(order) if order else queryset

def filter_main(tab, user):
    tabs = {
        'completed': MediaItem.objects.filter(
            usermediastatus__status=UserMediaStatus.Status.COMPLETED,
            usermediastatus__user=user
        ),
        'reviews': Review.objects.filter(user=user),
        'planned': MediaItem.objects.filter(
            usermediastatus__status=UserMediaStatus.Status.PLANNED,
            usermediastatus__user=user
        ),
    }

    return tabs.get(tab, MediaItem.objects.none())


def completed_counts(user):
    media_class= [Movie,Series,Book,ComputerGame]
    result = {}
    for media in media_class:
       result[media.__name__] = len(media.objects.filter(
           usermediastatus__status=UserMediaStatus.Status.COMPLETED
            ,usermediastatus__user=user))
    return result
