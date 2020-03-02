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
    "Glasgow Cathedral": {
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Glasgow-cathedral-may-2007.jpg/800px-Glasgow-cathedral-may-2007.jpg",
        "description": "Glasgow Cathedral, also called the High Kirk of Glasgow or St Kentigern's or St Mungo's Cathedral, is the oldest cathedral on mainland Scotland and is the oldest building in Glasgow. Since the Reformation the cathedral continues in public ownership, within the responsibility of Historic Environment Scotland. The congregation is part of the Church of Scotland's Presbytery of Glasgow and its services and associations are open to all. ",
        "location": "Cathedral Precinct, Castle Street, Glasgow, G4 0QZ",
        "price_range": "FR",
        "family_friendly": True,
        "disabled_access": True,
        "parking": False,
        "multi-language": True,
        "tags": ["Cultural Landmark", "Monument", ]
    },
    "Glasgow Botanic Gardens": {
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Wfm_glasgow_botanic_gardens.jpg/1024px-Wfm_glasgow_botanic_gardens.jpg",
        "description": "Glasgow Botanic Gardens is a botanical garden located in the West End of Glasgow, Scotland. It features several glasshouses, the most notable of which is the Kibble Palace. The Gardens has a wide variety of temperate and tropical flora, a herb garden, a chronological bed with plants arranged according to their introduction to Scotland, the UK's national collection of tree ferns, and a world rose garden officially opened in 2003 by Princess Tomohito of Mikasa.",
        "location": "730 Great Western Road, Glasgow, G12 0UE",
        "price_range": "FR",
        "family_friendly": True,
        "disabled_access": True,
        "parking": False,
        "multi-language": True,
        "tags": ["Natural Landmark", "Park", ]
    },
    "Pollock Country Park": {
        "image": "https://peoplemakeglasgow.com/images/Things_to_do/Parks_and_gardens/PollokHouse-995.jpg",
        "description": "The park is Glasgow's largest park and the only Country Park within Glasgow. Its extensive woodlands and gardens provide a quiet sanctuary for both visitors and wildlife. The park is rich in rural history formerly being part of the Old Pollok Estate and ancestral home to the Maxwell Family. The park is also home to the world famous Burrell Collection.",
        "location": "2060 Pollokshaws Road, Glasgow, G43 1AT",
        "price_range": "FR",
        "family_friendly": True,
        "disabled_access": True,
        "parking": True,
        "multi-language": True,
        "tags": ["Natural Landmark", "Cultural Landmark", "Park", ]
    },
    "The Riverside Museum of Transport and Travel": {
        "image": "https://media-cdn.tripadvisor.com/media/photo-s/05/29/a9/44/the-riverside-museum.jpg",
        "description": "Riverside Museum is Glasgow's award-winning transport museum. With over 3,000 objects on display there's everything from skateboards to locomotives, paintings to prams and cars to a Stormtrooper. There are over 90 large touch screens panels full of images, memories and films that tell the fascinating stories behind the objects.",
        "location": "100 Pointhouse Place, Glasgow, G3 8RS",
        "price_range": "FR",
        "family_friendly": True,
        "disabled_access": True,
        "parking": True,
        "multi-language": True,
        "tags": ["Cultural Landmark", "Museum"]
    },
    "University of Glasgow": {
        "image": "https://www.telegraph.co.uk/content/dam/education/2016/08/01/21590241universityofglasgowm-xlarge_trans_NvBQzQNjv4BqvHvVfV1SJqTMKlHaE5FBlnzInX02uMnPr3P1UZfzc14.jpg",
        "description": "The University of Glasgow is a public research university in Glasgow, Scotland. Founded by papal bull in 1451, it is the fourth-oldest university in the English-speaking world and one of Scotland's four ancient universities. Along with the universities of Edinburgh, Aberdeen, and St Andrews, the university was part of the Scottish Enlightenment during the 18th century. ",
        "location": "University Avenue, West End, Glasgow, G12 8QQ",
        "price_range": "FR",
        "family_friendly": True,
        "disabled_access": True,
        "parking": True,
        "multi-language": True,
        "tags": ["Cultural Landmark", ]
    },
    "Tennents Wellpark Brewery": {
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Tennents_Brewery.jpg/1200px-Tennents_Brewery.jpg",
        "description": "Wellpark Brewery in Glasgow is home to more than 450 years of brewing tradition and award winning beers. This is a chance to learn about the rich heritage of one of the country's most loved brands as well as about the production processes that have taken place at Wellpark from through the centuries up to today. ",
        "location": "161 Duke Street, Glasgow, G31 1JD",
        "price_range": "",
        "family_friendly": True,
        "disabled_access": False,
        "parking": True,
        "multi-language": False,
        "tags": ["Cultural Landmark", ]
    },
    "The Necropolis": {
        "image": "https://assets.atlasobscura.com/media/W1siZiIsInVwbG9hZHMvcGxhY2VfaW1hZ2VzL2EzNjkzMjlhMmM2Y2Y1MTdiMzM3NTI3NjU1MTIzMWVjN2ZmOTU2ZTkuanBnIl0sWyJwIiwiY29udmVydCIsIi1xdWFsaXR5IDkxIC1hdXRvLW9yaWVudCJdLFsicCIsInRodW1iIiwiNjAweD4iXV0/a369329a2c6cf517b3375276551231ec7ff956e9.jpg",
        "description": "The Glasgow Necropolis is a Victorian cemetery in Glasgow, Scotland. It is on a low but very prominent hill to the east of Glasgow Cathedral (St. Mungo's Cathedral). Fifty thousand individuals have been buried here. Typical for the period, only a small percentage are named on monuments and not every grave has a stone. Approximately 3500 monuments exist here. ",
        "location": "50 Cathedral Square, Glasgow, G4 0UZ",
        "price_range": "FR",
        "family_friendly": True,
        "disabled_access": False,
        "parking": True,
        "multi-language": False,
        "tags": ["Cultural Landmark", "Park", ]
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
