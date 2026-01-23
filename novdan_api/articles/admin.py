from django.contrib import admin

from .models import Article, Medium, MediumDonationAmount, MediumLink


class MediumLinkInline(admin.TabularInline):
    model = MediumLink
    extra = 0


class MediumDonationAmountInline(admin.TabularInline):
    model = MediumDonationAmount
    extra = 0


@admin.register(Medium)
class MediumAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    search_fields = ("id", "name", "url")
    inlines = [MediumLinkInline, MediumDonationAmountInline]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "medium", "published_at")
    search_fields = ("id", "title", "medium__name", "medium__url")
    list_filter = ("medium",)
