import os
from datetime import datetime

import pytz
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


# Returns a path to the specified file
def image_path(instance, filename):
    return os.path.join("attractions", instance.slug, filename)


# Tag Model
class Tag(models.Model):
    TAG_MAX_LENGTH = 64
    name = models.CharField(max_length=TAG_MAX_LENGTH, unique=True)
    slug = models.SlugField(unique=True)

    # Mutually exclusive tags have a ManyToMany relationship with Tag (itself)
    mutex_tags = models.ManyToManyField("self")

    # Override
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


# Attraction Model
class Attraction(models.Model):
    TITLE_MAX_LENGTH = 128
    approved = models.BooleanField(default=False)
    title = models.CharField(max_length=TITLE_MAX_LENGTH, unique=True)
    slug = models.SlugField(unique=True)

    link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to=image_path)

    description = models.TextField()
    location = models.TextField()

    # price_range is a limited choice field
    PRICE_RANGE_CHOICES = [
        ("FR", "Free"),
        ("CH", "Cheap"),
        ("MO", "Moderate"),
        ("EX", "Expensive"),
    ]
    price_range = models.CharField(
        max_length=2, choices=PRICE_RANGE_CHOICES, blank=True, null=True
    )

    # The Accessibility tags are boolean fields
    family_friendly = models.BooleanField(default=False)
    disabled_access = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    multi_language = models.BooleanField(default=False)

    starts = models.DateTimeField(blank=True, null=True)
    ends = models.DateTimeField(blank=True, null=True)

    added = models.DateTimeField(blank=True, null=True)

    rating = models.IntegerField(default=0)

    # Each Attraction can have many Tags, and each Tag can describe many Attractions
    tags = models.ManyToManyField(Tag)

    # Returns a correctly formatted time since this attraction was added
    @property
    def time_since_added(self):
        seconds_since = datetime.now(pytz.utc) - self.added
        if seconds_since.seconds < 60:          # seconds in a min
            return "Less than a minute ago"
        elif seconds_since.seconds < 3600:      # seconds in an hour
            return f"added {seconds_since.seconds/60:.0f} minutes ago"
        elif seconds_since.seconds < 86400:     # seconds in a day
            return f"added {seconds_since.seconds/3600:.0f} hours ago"
        elif seconds_since.seconds < 31557600:  # seconds in a year
            return f"added {seconds_since.seconds/86400:.0f} days ago"
        else:
            return "added over a year ago"

    # Adds a Price tag (one of the PRICE_RANGE_CHOICES) to this attraction
    def add_price_tag(self):
        # Iterate through the PRICE_RANGE_CHOICES to remove all price tags and
        # add only the tag specified by the price_range field
        for i in self.PRICE_RANGE_CHOICES:
            tag = Tag.objects.get(name=i[1])
            if self.price_range == i[0]:
                self.tags.add(tag)
            else:
                self.tags.remove(tag)

    # Adds Accessibility tags to this attraction, depending on whether the boolean fields are set
    def add_access_tags(self):
        access_tags = {
            "Family-friendly": self.family_friendly,
            "Disabled Access": self.disabled_access,
            "Parking": self.parking,
            "Multi-language": self.multi_language,
        }
        # Iterate through the Accessibility tags and add them if the respective
        # boolean field is set in this attraction, and remove them if not
        for name, condition in access_tags.items():
            tag = Tag.objects.get(name=name)
            if condition:
                self.tags.add(tag)
            else:
                self.tags.remove(tag)

    # Adds the Event tag if this attraction has a Start/End Date specified
    def add_event_tag(self):
        tag = Tag.objects.get(name="Event")
        if self.starts != None or self.ends != None:
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


# Vote Model
class Vote(models.Model):
    # The user who added the vote
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # The attraction the vote is for
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE)

    # A boolean field indicating whether this vote is positive or negative
    like = models.BooleanField()

    def __str__(self):
        return f"{self.user} - {self.attraction} - {self.like}"
