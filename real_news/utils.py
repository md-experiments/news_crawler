
import tldextract
from urllib.parse import urlparse
import os
import re
import newspaper
import datetime
from variable_defaults import PROPAGANDA_SUBDOMAINS, BANNED_EXTENSIONS, BANNED_STRINGS, ALLOWED_SUBDOMAINS, is_banned_regex

def _url_seems_ok(url, domain_to_allowed_subdomains, allow_all = None):
    """
    Check if the URL seems ok. if it does then we'll return a tuple of
    CLEAN URL, main domain.
    :param url:
    :return:
    """
    # Long URLs are usually bad
    if len(url) > 200:
        return False

    # FIRST check if the domain is OK
    ext = tldextract.extract(url)
    main_domain = ext.domain + '.' + ext.suffix
    allowed_subdomains = domain_to_allowed_subdomains.get(main_domain, allow_all)
    if allowed_subdomains is None:
        return False

    if isinstance(allowed_subdomains, list) and not ext.subdomain in allowed_subdomains:
        return False

    # Check for banned extensios
    parsed = urlparse(url)
    parsed = parsed._replace(query="", fragment="")
    path_to_use = parsed.path
    file_extension = os.path.splitext(path_to_use)[1]
    if file_extension in BANNED_EXTENSIONS:
        return False

    # If there are two dotcoms then that's probably bad!
    endings = len(re.findall(r'(\.com|\.co\.uk|\.net|\.org)', url))
    if endings > 1:
        return False

    # Check for banned words
    if not (is_banned_regex.search(url) is None):
        return False

    # AT A LATER DATE: we need to check if the URL was banned
    return (parsed.geturl(), main_domain)


def _filter_excessive_newlines(text):
    return re.sub(r'\n\s+', r'\n', text)


class Article(object):
    """ NEWSPAPER VERSION """

    def __init__(self, html):
        self.html = html if html is not None else ""

        self.dummy_article = newspaper.Article(url='', fetch_images=False, verbose=True)
        self.dummy_article.set_html(html)
        self.dummy_article.parse()

        self.text = _filter_excessive_newlines(self.dummy_article.text)
        self.authors = self.dummy_article.authors
        self.authors = [x for x in self.authors if len(x.split(' ')) < 10]
        self.title = self.dummy_article.title

        # sometimes the text started with the title... that's bad
        if self.text.startswith(self.title + '\n'):
            self.text = self.text[len(self.title):].lstrip('\n')

        if self.dummy_article.publish_date and not isinstance(self.dummy_article.publish_date, str):
            try:
                self.publish_date = self.dummy_article.publish_date.date().strftime(
                    "%m-%d-%Y")
            except AttributeError:
                self.publish_date = None
        else:
            self.publish_date = None

        self._extract_summary()

    def _extract_summary(self):
        self.summary = None
        for good2bad in [('og', 'description'), ('twitter', 'description'), ('description',)]:
            curr_dict = self.dummy_article.meta_data
            for key in good2bad[:-1]:
                curr_dict = curr_dict.get(key, {})
            summary = str(curr_dict.get(good2bad[-1], '')).strip()

            if len(summary) > 30:
                self.summary = summary
                return

    def num_empty_fields(self):
        num_empty = 0
        for k, v in self.serialize().items():
            if not v:
                num_empty += 1
        return num_empty

    def serialize(self):
        """
        Return simple page object to JSONify and write to file.
        """
        return {
            'meta_lang': self.dummy_article.meta_lang,
            'title': self.title,
            'text': self.text,
            'summary': self.summary,
            'authors': self.authors,
            'publish_date': self.publish_date
        }

    def __repr__(self):
        return str(self.serialize())


def parse_record(record, propaganda=False, allow_all=None):
    if record.rec_type != 'response':
        return
    if record.content_type != 'application/http; msgtype=response':
        return

    url_was_ok = _url_seems_ok(record.rec_headers['WARC-Target-URI'],
                               domain_to_allowed_subdomains=PROPAGANDA_SUBDOMAINS if propaganda else ALLOWED_SUBDOMAINS, allow_all=allow_all)
    if not url_was_ok:
        return

    url, domain = url_was_ok

    try:
        html = record.content_stream().read().decode('utf-8')
    except UnicodeDecodeError:
        # yield {'status': 'fail', 'url': url, 'reason': 'parse'}
        return

    if not html:
        # yield {'status': 'fail', 'url': url, 'reason': 'parse'}
        return

    try:
        article = Article(html).serialize()
    except ValueError:
        # yield {'status': 'fail', 'url': url, 'reason': 'parse'}
        return

    # Check if is good
    if article['publish_date'] is None:
        # yield {'status': 'fail', 'url': url, 'reason': 'date'}
        return
    if len(article['text']) < 1000:
        # yield {'status': 'fail', 'url': url, 'reason': 'len'}
        return
    if len(article['title']) < 30:
        # yield {'status': 'fail', 'url': url, 'reason': 'title'}
        return

    if article.pop('meta_lang') != 'en':
        # yield {'status': 'fail', 'url': url, 'reason': 'lang'}
        return

    article['status'] = 'success'
    article['url'] = url
    article['domain'] = domain
    article['warc_date'] = record.rec_headers['WARC-Date']
    yield article


def get_timestamp(out = None):
    if out == None:
        out = datetime.datetime.now()
    out = str(out).replace('-','').replace(' ','_').replace(':','')[:15]
    return out

def get_keys(file_key = 'aws_key_list.txt'):
    # Looks for credentials in local file
    if os.path.exists(file_key):
        with open(file_key,'r') as f:
            secrets = f.readlines()
        secrets = [s[:-1] if s.endswith('\n') else s for s in secrets]
        secrets_dict = {s.split('=')[0]:s.split('=')[1] for s in secrets}
        AWS_ACCESS_KEY = secrets_dict['AWS_ACCESS_KEY']
        AWS_SECRET_KEY = secrets_dict['AWS_SECRET_KEY']
    # Looks for credentials as environment variables (recommended)
    else:
        AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
        AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']
    return AWS_ACCESS_KEY, AWS_SECRET_KEY