import os
import random
import shutil
import tempfile
import sqlite3

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "glasgo_project.settings")

import django
from django.core.files import File
from django.db.models import Max
import urllib.request
from urllib.parse import urlparse

django.setup()
from django.contrib.auth.models import User
from glasgo.models import Attraction, Tag, Vote
from glasgo_project import settings
from population_data.tags import tags
from population_data.attractions import attractions
from population_data.users import users


TEMP_DIR = os.path.join(settings.MEDIA_DIR, "temp")


def populate_tags():
    for tag in tags.keys():
        add_tag(tag)
    for tag, mutex_tags in tags.items():
        add_mutex_tags(tag, mutex_tags)


def populate_attractions():
    for attraction, kwargs in attractions.items():
        add_attraction(attraction, **kwargs)


def populate_users():
    for username in users:
        user, cond = User.objects.get_or_create(username=username)
        if cond:
            user.password = username + "_password"
            user.save()


def populate_votes():
    random.seed(1)
    max_id = Attraction.objects.all().aggregate(max_id=Max("id"))["max_id"]
    for user in User.objects.all():
        for i in range(max_id // 2):
            try:
                att = Attraction.objects.get(id=random.randint(1, max_id))
            except Attraction.DoesNotExist:
                continue

            if not Vote.objects.filter(user=user, attraction=att).exists():
                Vote.objects.create(
                    user=user, attraction=att, like=random.choice((True, False))
                )


def add_tag(name):
    Tag.objects.get_or_create(name=name)[0].save()


def add_mutex_tags(name, mutex_tags=()):
    tag = Tag.objects.get_or_create(name=name)[0]
    mutex_tag_ids = (Tag.objects.get(name=mutex_tag).id for mutex_tag in mutex_tags)
    tag.mutex_tags.add(*mutex_tag_ids)
    tag.save()


def add_attraction(title, **kwargs):
    att, new = Attraction.objects.get_or_create(title=title)

    att.link = kwargs.get("link")

    if new:
        image_url = kwargs["image"]
        filename = os.path.basename(urlparse(image_url).path)
        with urllib.request.urlopen(image_url) as response:
            with tempfile.NamedTemporaryFile() as tmp_img:
                shutil.copyfileobj(response, tmp_img)
                image_file = File(tmp_img)
                att.image.save(filename, image_file, save=False)

    att.approved = True;
    att.description = kwargs["description"]
    att.location = kwargs["location"]

    att.price_range = kwargs.get("price_range")

    att.family_friendly = kwargs["family_friendly"]
    att.disabled_access = kwargs["disabled_access"]
    att.parking = kwargs["parking"]
    att.multi_language = kwargs["multi_language"]

    att.starts = kwargs.get("starts")
    att.ends = kwargs.get("ends")

    tag_ids = (Tag.objects.get(name=tag).id for tag in kwargs["tags"])
    att.tags.add(*tag_ids)

    att.save()


if __name__ == "__main__":
    print("Populating GlasGo Database . . . ")

    print("Populating Tags . . . ")
    populate_tags()
    for tag in Tag.objects.all():
        print(tag)

    print("Populating Attractions . . . ")
    populate_attractions()
    for attraction in Attraction.objects.all():
        print(attraction)

    print("Populating Users . . . ")
    populate_users()
    print(User.objects.all().count(), "users")

    print("Populating Votes . . . ")
    populate_votes()
    print(Vote.objects.all().count(), "votes")
