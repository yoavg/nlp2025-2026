from bs4 import BeautifulSoup, Tag
import glob
import os
import re
from markdownify import MarkdownConverter

class CustomConverter(MarkdownConverter):
    # don't format markdown links, return only their text, not their URL
    def convert_a(self, el, text, convert_as_inline):
        return text

    # skip tables
    def convert_table(self, el, text, convert_as_inline):
        return "[טבלה]"

# BeautifulSoup is a very strong package that allows you to target and extract very specific parts of the page,
# using tag-names, ids, css-selectors, and more. It is worth reading its documentation. Here, we use it very basically:
# - we extract the "title" and the "main" tags in the document
# - we then pass "main" to a custom MarkdownConverter to convert its content to markdown, while skipping table formatting and formatting links as text only.
# - We then manually split the markdown string into sections.
# You can do much more with BeautifulSoup and its worth looking at its documentation.
# You probably also want to not print everything to the same unformatted string as we do here, but create some data-structure,
# or save to a structured file (say where each item you care about is a jsonl string) or to multiple files.

for i, fname in enumerate(glob.iglob("created_kol_zchut_corpus/pages/*.html")):
    doc = BeautifulSoup(open(fname).read(), "html.parser")
    doc_id = fname.split("/")[-1].replace(".html", "")
    print(f"--------------------------------{doc_id}-------------------------------------")
    title = doc.title.contents[0]
    print("Title:", title)
    main = doc.main
    as_md = CustomConverter(heading_style="ATX", bullets="*").convert_soup(doc.main)
    as_md = re.sub(r"\n\n+", "\n\n", as_md)
    sections = as_md.split("\n#")
    for section in sections:
        if not section.strip(): continue # skip the before-first section if empty.
        section = "#" + section # add back the "#" we split on.
        sec_title, sec_body = section.split("\n", 1)
        print(f"SEC--{sec_title}--------------------")
        print(sec_body)
    
