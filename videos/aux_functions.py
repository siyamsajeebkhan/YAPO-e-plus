import os
import sys
import re
import urllib.request
from videos.models import *
from configuration import Config, Constants
from dateutil.parser import parse
import datetime
import requests.packages.urllib3
import http.client
import urllib3
import shutil
from utils.printing import Logger
log = Logger()

def progress (count: int, total: int, suffix=''):
    bar_len = 42
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '\u2588' * filled_len + '\u2591' * (bar_len - filled_len)
    #bar = '█' * filled_len + '░' * (bar_len - filled_len)
    sys.stdout.write(f"\r{bar} [{percents}%] - {suffix}                    \r")


def progress_end ():
    sys.stdout.flush()


def getMemory ():
    import psutil
    vmem = round(psutil.virtual_memory().total / 1000000000, 0)
    return vmem  # "{:.2}".format(vmem.total/100000000) #shold that be 102400000?


def getCPU ():
    import psutil
    cpufreq = round(psutil.cpu_freq().max / 1000, 1)
    return cpufreq


def getCPUCount ():
    import psutil
    return psutil.cpu_count(logical=False)  # set Logical to true if treads are to be included


def send_piercings_to_actortag (actor):
    piercings = actor.piercings
    if piercings:
        if ("navel" or "belly button" or "bellybutton") in piercings.lower():
            insert_actor_tag(actor, "Pierced navel")
        if "clit" in piercings.lower():
            insert_actor_tag(actor, "Pierced clitoris")
        if ("nipples" or "nipple rings") in piercings.lower():
            insert_actor_tag(actor, "Pierced nipples")
        elif "nipple" in piercings.lower():
            insert_actor_tag(actor, "Pierced single nipple")
        if "septum" in piercings.lower():
            insert_actor_tag(actor, "Pierced septum")
        if "nose" in piercings.lower():
            insert_actor_tag(actor, "Pierced nose")
        if "nostril" in piercings.lower():
            insert_actor_tag(actor, "Pierced nostril")
        if "tongue" in piercings.lower():
            insert_actor_tag(actor, "Pierced tongue")
        if "tragus" in piercings.lower():
            insert_actor_tag(actor, "Pierced tragus")
        if "helix" in piercings.lower():
            insert_actor_tag(actor, "Pierced helix")
        if ("earlobe" or "ear lobe") in piercings.lower():
            insert_actor_tag(actor, "Pierced ear lobe")
        if "lower lip" in piercings.lower():
            insert_actor_tag(actor, "Pierced lower lip")
        if "upper lip" in piercings.lower():
            insert_actor_tag(actor, "Pierced upper lip")
        if "monroe" in piercings.lower():
            insert_actor_tag(actor, "Pierced Monroe")
        if ("dermal" or "surface") in piercings.lower():
            insert_actor_tag(actor, "Pierced dermal")
        if "wrists" in piercings.lower():
            insert_actor_tag(actor, "Pierced wrists")
        elif "wrist" in piercings.lower():
            insert_actor_tag(actor, "Pierced single wrist")
        if "hip" in piercings.lower():
            insert_actor_tag(actor, "Pierced hip")
        elif "hips" in piercings.lower():
            insert_actor_tag(actor, "Pierced hips")
        if "labia" in piercings.lower():
            insert_actor_tag(actor, "Pierced labia")
        if "back dimples" in piercings.lower():
            insert_actor_tag(actor, "Pierced back dimples")
        if ("right brow" or "right eyebrow") in piercings.lower():
            insert_actor_tag(actor, "Pierced right eyebrow")
        elif ("left brow" or "left eyebrow") in piercings.lower():
            insert_actor_tag(actor, "Pierced left eyebrow")
        elif "brow" in piercings.lower():
            insert_actor_tag(actor, "Pierced eyebrow")
        if "ears" in piercings.lower():
            insert_actor_tag(actor, "Pierced ears")
        elif "left ear" in piercings.lower():
            insert_actor_tag(actor, "Pierced left ear")
        elif "right ear" in piercings.lower():
            insert_actor_tag(actor, "Pierced right ear")
        if "chest" in piercings.lower():
            insert_actor_tag(actor, "Pierced dermal on chest")
        if any([piercings.lower() == "none", piercings.lower() == "no piercings", piercings.lower() == "no"]):
            insert_actor_tag(actor, "No piercings")

def addactor (current_scene, actor_to_add):

    if not current_scene.actors.filter(name=actor_to_add):
        current_scene.actors.add(actor_to_add)
        print(f"Added Actor '{actor_to_add.name}' to scene '{current_scene.name}'")

    if actor_to_add.actor_tags.count() > 0:
        for actor_tag in actor_to_add.actor_tags.all():
            if not current_scene.scene_tags.filter(name=actor_tag.name):
                current_scene.scene_tags.add(
                    actor_tag.scene_tags.first()
                )
                print(
                    f"Added Scene Tag '{actor_tag.scene_tags.first().name}' to scene '{current_scene.name}'"
                )

    current_scene.save()


def insert_actor_tag (actor_to_insert, actor_tag_name):
    actor_tag_name = strip_bad_chars(actor_tag_name)

    if not ActorTag.objects.filter(name=actor_tag_name):
        actor_tag = ActorTag()
        actor_tag.name = actor_tag_name
        actor_tag.save()
        actor_to_insert.actor_tags.add(actor_tag)
    #        print("Added new tag: " + actor_tag_name + " for " + actor_to_insert.name)
    else:
        actor_tag = ActorTag.objects.get(name=actor_tag_name)
        actor_to_insert.actor_tags.add(actor_tag)
        #        print("Added tag: " + actor_tag_name + " for " + actor_to_insert.name)
        actor_tag.save()


def url_is_alive (url):
    """
    Checks that a given URL is reachable.
    :param url: A URL
    :rtype: bool
    """
    request = urllib.request.Request(url)
    request.get_method = lambda: "HEAD"

    try:
        urllib.request.urlopen(request)
        return True
    except urllib.request.HTTPError:
        return False


def remove_text_inside_brackets(text, brackets="()[]"):
    count = [0] * (len(brackets) // 2) # count open/close brackets
    saved_chars = []
    for character in text:
        for i, b in enumerate(brackets):
            if character == b: # found bracket
                kind, is_close = divmod(i, 2)
                count[kind] += (-1)**is_close # `+1`: open, `-1`: close
                if count[kind] < 0: # unbalanced bracket
                    count[kind] = 0  # keep it
                else:  # found bracket to remove
                    break
        else: # character is not a [balanced] bracket
            if not any(count): # outside brackets
                saved_chars.append(character)
    return ''.join(saved_chars)


def tpdb_formatter (name):
    trashTitle = (
        'RARBG', 'COM', '\d{3,4}x\d{3,4}', 'HEVC', 'H265', 'AVC', '\dK', '\d{3,4}p', 'TOWN.AG_', 'XXX', 'MP4',
        'KLEENEX', 'SD', 'H264', 'repack', '1500k', '500k', '1000k', 'rq', 'NEW', 'APT'
    )

    name = re.sub(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{2},\s\d{4}', '', name)
    name = re.sub(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s\d{2},\s\d{4}', '', name)
    name = re.sub(r'(\d+)[/\.-](\d+)[/\.-](\d+)', '', name)
    name = re.sub(r'\W', ' ', name)
    for trash in trashTitle:
        name = re.sub(r'\b%s\b' % trash, '', name, flags=re.IGNORECASE)
    name = ' '.join(name.split())

    name = name.replace("(", " ")
    name = name.replace(")", " ")
    name = name.replace("[", " ")
    name = name.replace("]", " ")
    name = name.replace("!", " ")
    name = name.replace("?", " ")
    name = remove_text_inside_brackets(name)
    name = re.sub(' +', ' ', name)

    #name = name.replace(" ","+")
    #name = name.replace(".","+")
    print(f"New name to use for searching: {name}")
    return name



def strip_bad_chars (name):
    bad_chars = { " " }
    for char in bad_chars:
        if char in name:
            # print("Before: " + name)
            name = name.replace(char, "")
            print(f"Adding Data: {name}")
    return name


def save_website_logo (image_link, website, force, *args):
    website = website.strip()
    if image_link:
        if image_link.lower() == "null" or image_link == "":
            print(f"There is no logo registered for {website}.")
            success = False
            return
    else:
        print(f"There is no logo registered for {website}.")
        success = False
        return

    try:
        hasarg = 0
        ws = None
        print("Website scan, method 1...")
        ws = Website.objects.filter(name=website)
        if not ws:
            print("Method unsuccesful, trying method 2...")
            ws = Website.objects.filter(name__iexact=website.replace(" ",""))

        if not ws and Config().tpdb_websites:
            print(f"{website} doesn't exist, and auto-addition is enabled...")
            for arg in args:
                hasarg += 1
                scene = arg
                if hasarg == 1: break

            ws = Website()
            ws.name = website
            ws.website_alias = website.replace(" ","").lower()
            ws.date_added = datetime.datetime.now()
            ws.save()
            log.info(f"Added website: {website.name}")
            ws = Website.objects.get(name=website)
            if hasarg == 1:
                scene.websites.add(ws)
                scene.save()
                log.info(f"A scene was added to {website.name}: {scene.name}")

    except:
        pass
    print(f"Automatic addition of website logos is set to {Config().tpdb_website_logos}...")
    if not Config().tpdb_website_logos:
        return
    if not ws and not Config().tpdb_websites:
        log.warn(f'LOGO ERROR: No website "{website}", and auto-registration of websites is disabled!')
        return
    ws = Website.objects.get(name=website)
    save_path = os.path.join(Config().site_media_path, "websites", str(ws.id))
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        print(f"Created website directory: {save_path}")
    if os.path.splitext(image_link)[1]:
        ext = os.path.splitext(image_link)[1]
    else:
        print("Error in logo filename!")
        success = False
        return
    save_file_name = os.path.join(save_path, "logo" + ext)
    if (not os.path.isfile(save_file_name) and not ws.thumbnail and Config().tpdb_website_logos) or force:
        maxretries = 3
        attempt = 0
        while attempt < maxretries:
            try:
                user_agent = {'user-agent': 'YAPO e+ 0.7'}
                http=urllib3.PoolManager(10,headers=user_agent)
                r1=http.urlopen('GET', image_link)
                if r1.status == 200:
                    #if os.path.exists(save_file_name):
                    #    os.remove(save_file_name)
                    with open(save_file_name, 'w+b') as f:
                        f.write(r1.data)
                        f.close()
            #urllib.request.urlretrieve(image_link, save_file_name)
            except:
                attempt += 1
                dlerror = 1
            else:
                dlerror = 0
                break

        if dlerror == 0:
            print(f"Downloaded website logo for website {ws.id} - {ws.name}")
            rel_path = os.path.relpath(save_file_name, start="videos")
            as_uri = urllib.request.pathname2url(rel_path)
            ws.thumbnail = as_uri
            ws.save()
            success = True
            return success
        else:
            log.error(f"DOWNLOAD ERROR: Logo: {image_link}")

    else:
        log.info(f"LOGO: {ws.name}: Skipping download, because the website already has a logo.")



def save_actor_profile_image_from_web (image_link, actor, force):
    save_path = os.path.join(
        Config().site_media_path, "actor", str(actor.id),"profile/"
    )

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    save_file_name = os.path.join(save_path, "profile.jpg")
    if not os.path.isfile(save_file_name) or force:
        maxretries = 3
        attempt = 0
        while attempt < maxretries:
            try:
                urllib.request.urlretrieve(image_link, save_file_name)
            except http.client.IncompleteRead:
                attempt += 1
                dlerror = 1
            else:
                dlerror = 0
                break

        if dlerror == 0:
            print("Downloaded photo.")
            rel_path = os.path.relpath(save_file_name, start="videos")
            as_uri = urllib.request.pathname2url(rel_path)
            actor.thumbnail = as_uri
        else:
            print("Download error, you need to try again or insert a photo manually.")

    else:
        print("Skipping, because there's already a usable photo.")



def actor_folder_from_name_to_id ():
    actors = Actor.objects.all()

    for actor in actors:
        rel_path = os.path.relpath(
            os.path.join(
                Config().site_media_path,
                "actor",
                str(actor.id),
                "profile",
                "profile.jpg",
            ),
            start="videos",
        )

        as_uri = urllib.request.pathname2url(rel_path)

        print(
           f"Actor {actor.name} thumb path is: {actor.thumbnail} \n and it should be {as_uri}"
        )
        print(actor.thumbnail != as_uri)
        if (actor.thumbnail != Config().unknown_person_image_path) and (
                actor.thumbnail != as_uri
        ):
            try:
                os.rename(
                    os.path.join(Config().site_media_path, "actor", actor.name),
                    os.path.join(Config().site_media_path, "actor", str(actor.id)),
                )

                print(
                    "Renamed %s to %s"%(
                        os.path.join(Config().site_media_path, "actor", actor.name),
                        os.path.join(Config().site_media_path, "actor", str(actor.id)),
                    )
                )
            except FileNotFoundError:

                if os.path.isfile(
                        os.path.join(
                            Config().site_media_path,
                            "actor",
                            str(actor.id),
                            "profile",
                            "profile.jpg",
                        )
                ):

                    rel_path_changed = os.path.relpath(
                        os.path.join(
                            Config().site_media_path,
                            "actor",
                            str(actor.id),
                            "profile",
                            "profile.jpg",
                        ),
                        start="videos",
                    )
                    as_uri_changed = urllib.request.pathname2url(rel_path_changed)
                    actor.thumbnail = as_uri_changed
                    actor.save()
                    print(f"Changed {actor.name} thumb in database to {as_uri_changed}")
                else:
                    print("File %s not found!"%(
                            os.path.join(Config().site_media_path, "actor", actor.name)
                        )
                    )

            rel_path_changed = os.path.relpath(
                os.path.join(
                    Config().site_media_path,
                    "actor",
                    str(actor.id),
                    "profile",
                    "profile.jpg",
                ),
                start="videos",
            )
            as_uri_changed = urllib.request.pathname2url(rel_path_changed)
            actor.thumbnail = as_uri_changed
            actor.save()

            print(f"Changed {actor.name} thumb in database to {as_uri_changed}")

    return True


if __name__ == "__main__":
    print("this is main")
