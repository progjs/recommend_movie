from django.contrib import admin
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from .models import Movie, Genre, Actor, Comment, UserDetail, WishList


class GenreInline(admin.TabularInline):
    model = Genre


class ActorInline(admin.TabularInline):
    model = Actor


class YearListFilter(admin.SimpleListFilter):
    title = '개봉년도로 분류'
    parameter_name = 'release_year'

    def lookups(self, request, model_admin):
        return (
            ('1900s', '2000년도 이전'),
            ('2000s', '2000년도 이후'),
        )

    def queryset(self, request, queryset):
        if self.value() == '1900s':
            return queryset.filter(release_year__lte=1999)
        if self.value() == '2000s':
            return queryset.filter(release_year__gte=2000)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    inlines = [GenreInline, ActorInline, ]
    list_display = ['id', 'title', 'score', 'nation', 'director', 'audience', 'release_year']
    list_display_links = ['id', 'title']
    list_filter = ['genres__genre', YearListFilter,]
    list_per_page = 50
    search_fields = ['title', 'nation', 'release_year', 'genres__genre', 'actors__actor']
    ordering = ['id']

    fieldsets = (
        ('기본 영화 정보', {
            'fields': ('title', 'score', 'nation', 'director', 'release_year', 'audience', 'plot',
                       )
        }),
        ('평점 계산', {
            'fields': ('comment_count', 'score_sum',)
        })
    )


@admin.register(UserDetail)
class UserDetailAdmin(admin.ModelAdmin):
    list_display = ['user', 'sex', 'birth', 'favorite_genre']
    list_display_links = ['user']
    list_filter = ['sex', 'favorite_genre']
    list_per_page = 20
    search_fields = ['sex', 'favorite_genre']
    ordering = ['id']
    fieldsets = (
        ('기본 정보', {
            'fields': ('user', 'password2',)
        }),
        ('추가 정보', {
            'fields': ('sex', 'birth', 'favorite_genre',)
        })
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['movie', 'user', 'comment_score', 'comment', 'published_date']
    list_display_links = ['movie', 'comment']
    list_filter = ['movie', 'user', 'comment_score']
    search_fields = ['movie', 'user', 'comment_score']
    list_per_page = 50
    ordering = ['movie']


@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie']
    list_display_links = ['user', 'movie']
    list_filter = ['user', 'movie']
    search_fields = ['user', 'movie']
    list_per_page = 30
    ordering = ['user']


admin.site.site_header = "Welcome to Admin Portal!"
admin.site.index_title = "방구석스크린 관리자 페이지"

# admin.site.register(Actor)
# admin.site.register(Genre)
