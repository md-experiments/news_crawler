
import os
import re
import json


with open(os.path.join(os.path.dirname(__file__), 'domain_to_allowed_subdomains.json'), 'r') as f:
    ALLOWED_SUBDOMAINS = json.load(f)

# FOR HANNAH
PROPAGANDA_SUBDOMAINS = {'wnd.com': True, 'infowars.com': True, 'breitbart.com': True, 'dailycaller.com': True,
                         'yournewswire.com': True, 'prageru.com': True, 'newsmax.com': True, 'twitchy.com': True,
                         'dailywire.com': True, 'dailysignal.com': True, 'bigleaguepolitics.com': True,
                         'redstate.com': True, 'townhall.com': True, 'bients.com': True, 'thegatewaypundit.com': True,
                         'nationalreport.net': True, 'naturalnews.com': True, 'prntly.com': True,
                         'worldnewsdailyreport.com': True,
                         'libertywriters.com': True, 'globalresearch.ca': True,
                         }

BANNED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'php', 'css', 'ico', 'xml', 'woff', 'swf', 'jpg', 'svg', 'ttf', 'tif',
                     'bmp', 'js', 'pdf', 'amp', 'rss', 'mp3', 'eot', 'jsp', 'woff2', 'json', 'com', 'axd', 'php3',
                     'bin', 'mp4', 'img', 'xhtml', 'dll', 'm4v', 'vov', 'phtml', 'flv', 'pl', 'jpe', 'otf', 'php\'',
                     'wmv', 'wav', 'xls', 'doc', 'photo', 'gallery', 'bg', 'ece', 'feed', 'xmlhttp', 'video', 'eml',
                     'xnf', 'prt', 'docx', 'file', 'vpx', 'cur', 'data', 'jhtml', 'xlsx', 'map', 'fb', 'webp', 'ppt',
                     'rdf', 'bio', 'exe', 'jar', 'net', 'open', 'ogg', 'wma', '7u', 'res', 'dwr', 'pjpeg', 'gz', 'ajax',
                     'psd', 'zip', 'coffee', 'tabs', 'cls', 'step', 'jp'}

BANNED_STRINGS = ['slideshow.',
                  'slideshowImage', 'associatedcontent.com',
                  '/videoid/', 'sodahead.com', 'b92.net',
                  'isna.ir', 'prnewswire.com', 'slashdot.org', 'suite101.com', 'tv.com', 'news.yahoo.com',
                  '/video/', '/image/', 'bbb.org', 'yle.fi', 'ImageId', 'slideshow_files', '/slideshows/',
                  '/videos/', '/video-', '/videoid/', '/wp-json/', '/search/', 'videoID=', '/portableplayer/',
                  'video.aspx', '/allvideo/', 'width=', 'height=', '/PhotoGallery/', 'ArticleSlideshowServlet',
                  '/storyimage/', '/image.html', '/photos/', '.jpeg', '.jpg', '/em_image', 'maxw=', 'maxh=',
                  '/flashplayers/', '/apps/', '/gallery/', 'photogallery', 'imageViewer', '.jpg', 'img=',
                  '/forums/', '/users/', '/tags/', '/audio/', '/resources/', '/metrics/', '/images/', '/products/',
                  'com.pe', '/agencia/', '/resizer/', '/user?', '/tag/', '/bookmark/', '/plugins/', '/blogs/',
                  '/advertising/', 'blockbuster.co.uk', '/oembed/', '/needlogin', 'type=login', '/mailto/', '/feed',
                  'sendtofriend.aspx', '/ajax/', 'bloggernews.net', '/topics/', 'view_gallery', '/event.asp', '/forum/',
                  '/posts/', '/cgi-bin/', '/member/', 'news_tool_v2.cfm', '/database/', '/Default.aspx',
                  '/Search/', '/Slideshow/', '/slideshow/', '/user/', '/register/', '/donate/', '/calendar/',
                  'send-to-friend',
                  '/enter/', '/photo-gallery/', '/news_email.asp', '/Flash.aspx', '/findlocal/', '/ads/', '/reply/',
                  '/events/', '/picture-gallery/', '/slideshow?', '/Mozilla/', '/sendtoafriend.asp', '/blog/',
                  '/mailStory/', 'admin.asp?', '.ads/', '/used_cars/'
                  ]
BANNED_STRINGS = [re.escape(x) for x in BANNED_STRINGS]
is_banned_regex = re.compile(r'(' + r'|'.join(BANNED_STRINGS) + r')')
