# ----------------------
import random
# ----------------------
def get_header():
    # return a random user agent header based on generated number
    list = [
            {
             'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36',
             'Origin': 'http://example.com',
             'Referer': 'http://example.com/some_page'
             },
            {
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
             'Origin': 'http://example.com',
             'Referer': 'http://example.com/some_page'
             },
            {
             'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
             'Origin': 'http://example.com',
             'Referer': 'http://example.com/some_page'
             },
            {
             'User-Agent': 'Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
             'Origin': 'http://example.com',
             'Referer': 'http://example.com/some_page'
            },
            {
             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
             'Origin': 'http://example.com',
             'Referer': 'http://example.com/some_page'
             },
            {
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
             'Origin': 'http://example.com',
             'Referer': 'http://example.com/some_page'
             },
            {
             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
             'Origin': 'http://example.com',
             'Referer': 'http://example.com/some_page'
             },
            {
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36',
             'Origin': 'http://example.com',
             'Referer': 'http://example.com/some_page'
             },
            {
             'User-Agent': 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
             'Origin': 'http://example.com',
             'Referer': 'http://example.com/some_page'
             },
            {
             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
             'Origin': 'http://example.com',
             'Referer': 'http://example.com/some_page'
             },
            {
             'User-Agent': 'Mozilla/5.0 (X11; U; Linux i586; en-US) AppleWebKit/533.2 (KHTML, like Gecko) Chrome/5.0.342.1 Safari/533.2',
             'Origin': 'http://example.com',
             'Referer': 'http://example.com/some_page'
             }
        ]

    # list is of size 11
    curr = random.randrange(0, 10)
    return list[curr]
# ----------------------
