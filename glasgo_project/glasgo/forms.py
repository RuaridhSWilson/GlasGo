from django import forms
from django.db.utils import OperationalError

from glasgo.models import Attraction, Tag


try:
    # AttractionForm class - specifies all the fields in the Add Attraction form
    class AttractionForm(forms.ModelForm):
        # approved is a boolean hidden field that admins change to approve the attraction
        approved = forms.BooleanField(widget=forms.HiddenInput(), required=False)

        title = forms.CharField(max_length=Attraction.TITLE_MAX_LENGTH)

        # slug is a hidden char field in the Add Attraction form, determined after the attraction is submitted
        slug = forms.CharField(widget=forms.HiddenInput(), required=False)

        link = forms.URLField(max_length=254, label="Website", required=False)
        image = forms.ImageField()
        description = forms.TextInput(attrs={"size": "30"})
        location = forms.TextInput()

        # price_range is a choice field which will be specified by radio buttons
        price_range = forms.ChoiceField(
            choices=Attraction.PRICE_RANGE_CHOICES,
            required=False,
            widget=forms.RadioSelect,
        )

        # The Accessibility tags are boolean fields each specified by a checkbox
        family_friendly = forms.BooleanField(required=False, label="Family-friendly")
        disabled_access = forms.BooleanField(required=False)
        parking = forms.BooleanField(required=False)
        multi_language = forms.BooleanField(required=False, label="Multi-language")

        starts = forms.DateTimeField(required=False)
        ends = forms.DateTimeField(required=False)

        # added and rating are hidden fields in the Add Attraction form - they are determined after the attraction is submitted
        added = forms.DateTimeField(widget=forms.HiddenInput(), required=False)
        rating = forms.IntegerField(widget=forms.HiddenInput(), required=False)

        # tags is a multiple choice field whose choices are all the tags, specified by checkboxes
        tags = forms.MultipleChoiceField(
            choices=[(tag.id, tag.name) for tag in Tag.objects.all()],
            widget=forms.CheckboxSelectMultiple,
            label="Tags",
            required=False,
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
            # Return a cleaned link (starts with "http://")
            cleaned_data = self.cleaned_data
            link = cleaned_data.get("link")
            if link and not (link.startswith("http://") or link.startswith("https://")):
                link = f"http://{link}"
                cleaned_data["link"] = link

            return cleaned_data


except OperationalError:
    pass  # allows this file to be imported when the database doesn't exist
