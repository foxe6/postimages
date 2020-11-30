__version__ = "0.1.0"
__keywords__ = ["postimages postimagesorg host upload images photos"]


if not __version__.endswith(".0"):
    import re
    print(f"version {__version__} is deployed for automatic commitments only", flush=True)
    print("install version " + re.sub(r"([0-9]+\.[0-9]+\.)[0-9]+", r"\g<1>0", __version__) + " instead")
    import os
    os._exit(1)


import requests
import re
import json
import datetime
import time
import math
import lxml.html
import omnitools


__ALL__ = ["upload"]


postimages_domain = "https://postimages.org"


def upload(urls):
    session_upload = str(math.floor(time.time()*1000))
    timestamp = datetime.datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")
    s = requests.Session()
    r = s.get(postimages_domain + "/web")
    token = re.search(r"\{.token.:'(.*?)'", r.content.decode())[1]
    upload_session = omnitools.randstr(32)
    gallery = ""
    numfiles = len(urls)
    album = ""
    for url in urls:
        r = s.post(postimages_domain + "/json/rr", headers={
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "x-requested-with": "XMLHttpRequest"
        }, data={
            "token": token,
            "upload_session": upload_session,
            "url": url,
            "numfiles": numfiles,
            "gallery": gallery,
            "ui": json.dumps([24, 1920, 1080, "true", "", "", timestamp]),
            "optsize": "0",
            "expire": "0",
            "session_upload": session_upload
        })
        if r.status_code != 200:
            raise Exception("upload failed", r.status_code, r.content.decode())
        if numfiles > 1 and not gallery:
            gallery = r.json()["gallery"]
        if not album:
            album = r.json()["url"]
    r = s.get(album)
    r = lxml.html.fromstring(r.content.decode())
    imgs = [re.search(r"\(.(.*?).\)", img)[1] for img in r.xpath("//div[@class='thumb']/a[@class='img'][@href]/@style")]
    return imgs

