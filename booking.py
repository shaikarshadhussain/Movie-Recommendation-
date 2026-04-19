import webbrowser

from database import get_platform_links


def get_primary_link(movie_id, preferred_type="streaming_search"):
    links = get_platform_links(movie_id)
    for link in links:
        if link["link_type"] == preferred_type:
            return link
    return links[0] if links else None


def open_primary_link(movie_id):
    link = get_primary_link(movie_id)
    if not link:
        return False, None

    webbrowser.open(link["url"], new=2)
    return True, link


def open_link(url):
    webbrowser.open(url, new=2)
