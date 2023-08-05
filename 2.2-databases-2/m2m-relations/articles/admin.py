from django.contrib import admin
from django.forms import BaseInlineFormSet
from .models import Article, Tag, Scope
from django.core.exceptions import ValidationError


class ScopeInlineFormSet(BaseInlineFormSet):

    def clean(self):
        self.main_tag_counter = 0

        if len(self.forms) == 0:
            raise ValidationError('Не указан тег')
        for form in self.forms:
            if self.main_tag_counter > 0 and form.cleaned_data.get('is_main'):
                raise ValidationError('Основной тег только один')
            else:
                if form.cleaned_data.get('is_main'):
                    self.main_tag_counter += 1
                else:
                    continue
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormSet
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', )
    inlines = (ScopeInline,)
