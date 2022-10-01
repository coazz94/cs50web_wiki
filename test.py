import re


name = """# CSS

CSS is a language that can be used to add style to an [HTML](/wiki/HTML) page."""


test = "abc"

matches = re.search(r"^[#]\s.*\n\n(.*)", name, re.MULTILINE)


print(matches.groups())