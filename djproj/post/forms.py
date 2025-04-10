from django import forms
from . import models


class PostCategoryForm(forms.ModelForm):
    class Meta:
        model = models.PostCategory
        fields = ['name']

class CreatePost(forms.ModelForm):
    # Hidden field to signal a new category should be created
    # new_category = forms.CharField(max_length=100, required=False, widget=forms.HiddenInput())
    class Meta:
        model = models.Post
        fields = ['title', 'body', 'slug', 'banner']

# from django import forms
# from django.urls import reverse
# from . import models


# from django.utils.safestring import mark_safe
# from django.forms import widgets
# from django.conf import settings
# from django.utils.translation import gettext as _

# class RelatedFieldWidgetCanAdd(widgets.Select):

#     def __init__(self, related_model, related_url=None, *args, **kw):

#         super(RelatedFieldWidgetCanAdd, self).__init__(*args, **kw)

#         if not related_url:
#             rel_to = related_model
#             info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
#             related_url = 'admin:%s_%s_add' % info

#         # Be careful that here "reverse" is not allowed
#         self.related_url = related_url

#     def render(self, name, value, *args, **kwargs):
#         self.related_url = reverse(self.related_url)
#         output = [super(RelatedFieldWidgetCanAdd, self).render(name, value, *args, **kwargs)]
#         output.append('<a href="%s" class="add-another" id="add_id_%s" onclick="return showAddAnotherPopup(this);"> ' % \
#             (self.related_url, name))
#         output.append('<img src="%smedia/spongebob_PNG52_f6oFo4J.png" width="10" height="10" alt="%s"/></a>' % (settings.STATIC_URL, 'Add Another'))
#         return mark_safe(''.join(output))
    

# class PostCategoryForm(forms.ModelForm):
#     class Meta:
#         model = models.PostCategory
#         fields = ['name']

# class CreatePost(forms.ModelForm):
#     # Hidden field to signal a new category should be created
#     # new_category = forms.CharField(max_length=100, required=False, widget=forms.HiddenInput())
#     category = forms.ModelChoiceField(required=False, queryset=models.PostCategory.objects.all(),widget=RelatedFieldWidgetCanAdd(models.PostCategory, related_url="posts:new-post-category"))
#     class Meta:
#         model = models.Post
#         fields = ['title', 'category', 'body', 'slug', 'banner']

