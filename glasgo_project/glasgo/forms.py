from django import forms

from glasgo.models import Attraction, Tag


class AttractionForm(forms.ModelForm):
    title = forms.CharField(max_length=Attraction.TITLE_MAX_LENGTH, help_text="Title")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    link = forms.URLField(max_length=254, help_text="Website", required=False)
    image = forms.ImageField(help_text="Image")

    description = forms.TextInput()
    location = forms.TextInput()

    price_range = forms.ChoiceField(
        choices=Attraction.PRICE_RANGE_CHOICES, required=False
    )

    family_friendly = forms.BooleanField(required=False)
    disabled_access = forms.BooleanField(required=False)
    parking = forms.BooleanField(required=False)
    multi_language = forms.BooleanField(required=False)

    starts = forms.DateTimeField(required=False)
    ends = forms.DateTimeField(required=False)

    added = forms.DateTimeField(widget=forms.HiddenInput(), required=False)

    rating = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    tags = forms.MultipleChoiceField(
        choices=[(tag.id, tag.name) for tag in Tag.objects.all()],
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Attraction

        exclude = (
            "slug",
            "added",
            "rating",
        )

    # Override
    def clean(self):
        cleaned_data = self.cleaned_data
        link = cleaned_data.get("link")
        if link and not (link.startswith("http://") or link.startswith("https://")):
            link = f"http://{link}"
            cleaned_data["link"] = link

        return cleaned_data