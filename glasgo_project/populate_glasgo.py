import os
import shutil
import tempfile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "glasgo_project.settings")

import django
from django.core.files import File
import urllib.request
from urllib.parse import urlparse

django.setup()
from glasgo.models import Attraction, Tag
from glasgo_project import settings


TEMP_DIR = os.path.join(settings.MEDIA_DIR, "temp")


tags = {
    "Museum": [],
    "Festival": [],
    "Cultural Landmark": [],
    "Natural Landmark": [],
    "Park": [],
    "Sports": [],
    "Monument": [],
    "Free": ["Cheap", "Moderate", "Expensive"],
    "Cheap": ["Free", "Moderate", "Expensive"],
    "Moderate": ["Free", "Cheap", "Expensive"],
    "Expensive": ["Free", "Cheap", "Moderate"],
    "Family-friendly": [],
    "Disabled Access": [],
    "Parking Availability": [],
}

attractions = {
    "Celtic Park Stadium": {
        "link": "http://www.celticfc.net/mainindex",
        "image": "https://cdn.getyourguide.com/img/tour_img-1222909-148.jpg",
        "description": "Celtic Park in the Parkhead area of Glasgow, Scotland, is the home ground of Celtic Football Club. With a capacity of 60,411, it is the largest football stadium in Scotland, and the eighth-largest stadium in the United Kingdom. It is known by Celtic fans as Parkhead or Paradise.",
        "location": "Celtic Park Stadium, The Celtic Way, Parkhead, Glasgow, G40 3RE",
        "price_range": "MO",
        "family_friendly": True,
        "disabled_access": True,
        "parking": True,
        "multi_language": False,
        "tags": ["Sports", "Cultural Landmark",],
    },
    "George Square": {
        "image": "https://upload.wikimedia.org/wikipedia/commons/a/ad/City_Chambers%2C_George_Square%2C_Glasgow_05.jpg",
        "description": "George Square is the principal civic square in the city of Glasgow, Scotland. It is one of six squares in the city centre, the others being Cathedral Square, St Andrew's Square, St Enoch Square, Royal Exchange Square, and Blythswood Square on Blythswood Hill.",
        "location": "George Square, Glasgow, G2 1DH",
        "price_range": "FR",
        "family_friendly": True,
        "disabled_access": True,
        "parking": False,
        "multi_language": False,
        "tags": ["Cultural Landmark", "Monument",],
    },
    "Kelvingrove Art Gallery and Museum": {
        "image": "https://peoplemakeglasgow.com/images/Things_to_do/Museums_and_galleries/Kelvingrove-995.jpg",
        "description": "Kelvingrove Art Gallery and Museum is a museum and art gallery in Glasgow, Scotland. It reopened in 2006 after a three-year refurbishment and since then has been one of Scotland's most popular visitor attractions. The museum has 22 galleries, housing a range of exhibits, including Renaissance art, taxidermy, and artifacts from ancient Egypt.",
        "location": "Kelvingrove Art Gallery and Museum, Argyle St, Glasgow, G3 8AG",
        "price_range": "FR",
        "family_friendly": True,
        "disabled_access": True,
        "parking": False,
        "multi-language": True,
        "tags": ["Cultural Landmark", "Museum",]
    },
}


def populate_tags():
    for tag in tags.keys():
        add_tag(tag)
    for tag, mutex_tags in tags.items():
        add_mutex_tags(tag, mutex_tags)


def populate_attractions():
    for attraction, kwargs in attractions.items():
        add_attraction(attraction, **kwargs)


def add_tag(name):
    Tag.objects.get_or_create(name=name)[0].save()


def add_mutex_tags(name, mutex_tags=()):
    tag = Tag.objects.get_or_create(name=name)[0]
    mutex_tag_ids = (Tag.objects.get(name=mutex_tag).id for mutex_tag in mutex_tags)
    tag.mutex_tags.add(*mutex_tag_ids)
    tag.save()


def add_attraction(title, **kwargs):
    att = Attraction.objects.get_or_create(title=title)[0]

    att.link = kwargs.get("link")

    image_url = kwargs["image"]
    filename = os.path.basename(urlparse(image_url).path)
    with urllib.request.urlopen(image_url) as response:
        with tempfile.NamedTemporaryFile() as tmp_img:
            shutil.copyfileobj(response, tmp_img)
            image_file = File(tmp_img)
            att.image.save(filename, image_file, save=False)

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
    populate_tags()
    for tag in Tag.objects.all():
        print(tag)
    populate_attractions()
    for attraction in Attraction.objects.all():
        print(attraction)
