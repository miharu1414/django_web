import sys
import requests
from bs4.element import Tag, NavigableString
from bs4 import BeautifulSoup

"""dfsdfs"""
def _parse_li(li):
    """
    リストアイテム(li)のテキストを返す。
    ※ li内の入れ子リストは除外する (重複するため)
    """
    buffer = []
    for child in li:
        if type(child) == NavigableString:
            buffer.append(child.string)
        elif type(child) == Tag:
            # リスト構造ではない child のみ返り値に含める
            if child.find_all('li') == []:
                buffer.append(child.get_text())
    return ''.join(buffer)


def get_blog_texts(url: str):
    """get blog texts from url"""
    # get html source
    response = requests.get(url)
    # parse html
    soup = BeautifulSoup(response.text, 'html.parser')
    contents = soup.find('div')
    # extract all <p>...</p> texts
    texts = [c.get_text() for c in contents.find_all('p')]
    # extract all <li>...</li> texts
    texts = texts + [_parse_li(li) for li in contents.find_all('li')]
    # processing
    texts = [t.replace('\n', '') for t in texts]

    return texts


if __name__ == "__main__":
    url = sys.argv[1]
    [print(t) for t in get_blog_texts(url)]