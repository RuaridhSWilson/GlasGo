import os

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


def image_path(instance, filename):
    return os.path.join("attractions", instance.slug, filename)


class Tag(models.Model):
    TAG_MAX_LENGTH = 64
    name = models.CharField(max_length=TAG_MAX_LENGTH, unique=True)
    slug = models.SlugField(unique=True)

    mutex_tags = models.ManyToManyField("self")

    # Override
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Attraction(models.Model):
    TITLE_MAX_LENGTH = 128
    title = models.CharField(max_length=TITLE_MAX_LENGTH, unique=True)
    slug = models.SlugField(unique=True)

    link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to=image_path)

    description = models.TextField()
    location = models.TextField()

    PRICE_RANGE_CHOICES = [
        ("FR", "Free"),
        ("CH", "Cheap"),
        ("MO", "Moderate"),
        ("EX", "Expensive"),
    ]
    price_range = models.CharField(
        max_length=2, choices=PRICE_RANGE_CHOICES, blank=True, null=True
    )

    family_friendly = models.BooleanField(default=False)
    disabled_access = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    multi_language = models.BooleanField(default=False)

    starts = models.DateTimeField(blank=True, null=True)
    ends = models.DateTimeField(blank=True, null=True)

    added = models.DateTimeField(auto_now_add=True)

    rating = models.IntegerField(default=0)

    tags = models.ManyToManyField(Tag)

    def add_price_tag(self):
        for i in self.PRICE_RANGE_CHOICES:
            tag = Tag.objects.get(name=i[1])
            if self.price_range == i[0]:
                self.tags.add(tag)
            else:
                self.tags.remove(tag)

    def add_access_tags(self):
        access_tags = {
            "Family-friendly": self.family_friendly,
            "Disabled Access": self.disabled_access,
            "Parking": self.parking,
            "Multi-language": self.multi_language,
        }
        for name, condition in access_tags.items():
            tag = Tag.objects.get(name=name)
            if condition:
                self.tags.add(tag)
            else:
                self.tags.remove(tag)

    # Override
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        try:
            self.add_price_tag()
            self.add_access_tags()
        except (Attraction.DoesNotExist, ValueError):
            pass
        super(Attraction, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE)
    like = models.BooleanField()

    def __str__(self):
        return f"{self.user} - {self.attraction} - {self.like}"
