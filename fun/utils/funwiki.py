# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _

from course_wiki.utils import course_wiki_slug

TEMPLATE = '<li><a href="{link}" target="_blank">{title}</a> <span class="{state}">({revisions} {date})</span></li>'


def get_base_page(course):
    """Returns course base wiki page.
        Args:    course (Mongo object)
        Returns: URLPath
    """
    import wiki.models.urlpath

    root = wiki.models.urlpath.URLPath.get_by_path('/')
    slug = course_wiki_slug(course)
    try:
        base_page = wiki.models.urlpath.URLPath.objects.select_related("article").get(parent=root, slug=slug)  # retrieve base page
    except wiki.models.urlpath.URLPath.DoesNotExist:
        base_page = None
    return base_page


def count_articles(course):
    """Returns course wiki pages count.
       `descendant_objects` is a recursive function from mptt and can be expensive.
        Args:    course (Mongo object)
        Returns: integer
    """
    base_page = get_base_page(course)
    count = len(list(base_page.article.descendant_objects())) + 1
    return count

def get_page_tree(pages):
    """Recursively build a tree of pages.
        Args:    list of pages (URLPath)
        Returns: list of pages (URLPath)
    """
    import wiki.models.urlpath

    for idx, child in enumerate(pages):
        if isinstance(child, wiki.models.urlpath.URLPath):
            children = get_page_tree(list(child.get_children()))
            if children:
                pages.insert(idx + 1, children)
    return pages


def render_html_tree(tree, html):
    """Recursively build HTML tree of wiki pages.
        Args:    tree: list of pages as generated by `get_page_tree`
                 html: string
        Returns: string
    """
    for item in tree:
        if isinstance(item, list):
            html += '<ul>'
            tree, html = render_html_tree(item, html)
            html += '</ul>'
        else:
            state = ''
            if all([item.article.group_write, item.article.other_write]):
                state = 'open'
            elif not all([item.article.group_write, item.article.other_write]):
                state = 'closed'

            html += TEMPLATE.format(
                    title=item.article.current_revision.title,
                    link=item.get_absolute_url(),
                    revisions=item.article.articlerevision_set.count(),
                    date=item.article.current_revision.created.strftime(_('%m/%d/%y %H:%M')),
                    state=state)

    return tree, html


def set_permissions(course, value):
    """Set wiki articles write permissions to True of False.
        Args:    course (Mongo object)
                 value (boolean)
        Returns: URLPath
    """
    import wiki.models.article

    base_page = get_base_page(course)
    if base_page:
        base_page.article.group_write = value
        base_page.article.other_write = value
        base_page.article.save()
        base_page_descendants = base_page.article.descendant_objects()  # will recursively return all URLPath children to this article (whatever the depth)
        wiki.models.article.Article.objects.filter(
                    urlpath__in=base_page_descendants).update(group_write=value, other_write=value)
    return base_page