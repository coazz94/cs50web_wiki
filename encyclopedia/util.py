import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import random


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    #syntax von diesem return verstehen
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
        Saves an encyclopedia entry, given its title and Markdown
        content. If an existing entry with the same title already exists,
        it is replaced.
    """

    write = "# " + title + "\n" + content.replace("\n", "")

    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(write))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """

    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def clean_name(title):
    """
        Just a small Function to make all the titels of the Pages Capital letter first
    """

    return title[0].upper() + title [1:]


def random_page():
    """
        return a random Page
    """
    return random.choice(list_entries())


def delete_page(title):
    
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
        return True
    else:
        return False
    