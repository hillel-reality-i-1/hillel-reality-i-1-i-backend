from django import forms
from ..models.post import Post


class PostValidateAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"

    def clean_country(self):
        value = self.cleaned_data.get("country")
        if value.count() > 5:
            raise forms.ValidationError("Ви можете обрати не більше 5 країн")
        return value
