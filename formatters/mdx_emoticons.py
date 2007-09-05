"""
Emoticon Extension for python-markdown
======================================

Converts defined emoticon symbols to images, with the symbols as their ``alt``
text. Requires python-markdown 1.6+.

Basic usage:

    >>> import markdown
    >>> text = 'Some text with a pre-defined emoticon :p.'
    >>> markdown.markdown(text, ['emoticons'])
    '\\n<p>Some text with a pre-defined emoticon <img src="tongue.gif" alt=":p"/>.\\n</p>\\n\\n\\n'

Simple custom settings:

    >>> md = markdown.markdown(text,
    ...     ['emoticons(BASE_URL=/emoticons/,FILE_EXTENSION=jpg)']
    ... )
    >>> md
    '\\n<p>Some text with a pre-defined emoticon <img src="/emoticons/tongue.jpg" alt=":p"/>.\\n</p>\\n\\n\\n'

Complex custom settings:

    >>> md = markdown.Markdown(text,
    ...     extensions=['emoticons'],
    ...     extension_configs={'emoticons': [
    ...             ('EMOTICONS', {':p': 'cheeky'}),
    ...             ('BASE_URL', 'http://supoib-emoticons.com/'),
    ...             ('FILE_EXTENSION', 'png'),
    ...         ]})
    >>> md.toString()
    '\\n<p>Some text with a pre-defined emoticon <img src="http://supoib-emoticons.com/cheeky.png" alt=":p"/>.\\n</p>\\n\\n\\n'

"""
import re

import markdown

class EmoticonExtension(markdown.Extension):
    def __init__ (self, configs):
        self.config = {
            'EMOTICONS': [{
                    ':angry:':    'angry',
                    ':blink:':    'blink',
                    ':D':         'grin',
                    ':huh:':      'huh',
                    ':lol:':      'lol',
                    ':o':         'ohmy',
                    ':ph34r:':    'ph34r',
                    ':rolleyes:': 'rolleyes',
                    ':(':         'sad',
                    ':)':         'smile',
                    ':p':         'tongue',
                    ':unsure:':   'unsure',
                    ':wacko:':    'wacko',
                    ';)':         'wink',
                    ':wub:':      'wub',
                }, 'A mapping from emoticon symbols to image names.'],
            'BASE_URL': ['', 'The base URL at which emoticons are accessible.'],
            'FILE_EXTENSION': ['gif', 'The file extension to be used for emoticon images.'],
        }

        for key, value in configs :
            self.config[key][0] = value

    def extendMarkdown(self, md, md_globals):
        self.md = md
        EMOTICON_RE = '(?P<emoticon>%s)' % '|'.join(
            [re.escape(emoticon) \
             for emoticon in self.getConfig('EMOTICONS').keys()])
        md.inlinePatterns.append(EmoticonPattern(EMOTICON_RE, self))

class EmoticonPattern(markdown.Pattern):
    def __init__ (self, pattern, emoticons):
        markdown.Pattern.__init__(self, pattern)
        self.emoticons = emoticons

    def handleMatch(self, m, doc):
        emoticon = m.group('emoticon')
        el = doc.createElement('img')
        el.setAttribute('src', '%s%s.%s' % (
            self.emoticons.getConfig('BASE_URL'),
            self.emoticons.getConfig('EMOTICONS')[emoticon],
            self.emoticons.getConfig('FILE_EXTENSION')))
        el.setAttribute('alt', emoticon)
        return el

def makeExtension(configs=None) :
    return EmoticonExtension(configs=configs)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
