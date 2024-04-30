# -*- coding: utf-8 -*-
#
# Conversion of Mueller dictionaries to the DICT format
#
# (c) 2006,2019 Mikhail Gusarov <dottedmag@dottedmag.net>
# Based on Andrew Comech <comech@math.sunysb.edu> work.
#
# GPLv2
#

import re, sys, textwrap, io

# -- Transcription conversion --

#
# Mapping Mueller's transcription characters to IPA alphabet.
#
letters = {
    'A' : '\N{LATIN SMALL LETTER ALPHA}',
    'D' : '\N{LATIN SMALL LETTER ETH}',
    'E' : 'e',
    'I' : '\N{LATIN LETTER SMALL CAPITAL I}',
    'N' : '\N{LATIN SMALL LETTER ENG}',
    'Q' : '\N{LATIN SMALL LETTER AE}',
    'S' : '\N{LATIN SMALL LETTER ESH}',
    'T' : '\N{GREEK SMALL LETTER THETA}',
    'Z' : '\N{LATIN SMALL LETTER EZH}',
    'e' : '\N{LATIN SMALL LETTER OPEN E}',
    'u' : '\N{LATIN SMALL LETTER UPSILON}',
    '█' : '\N{LATIN SMALL LETTER REVERSED E}', # 0x8B
    '╚' : '\N{LATIN SMALL LETTER REVERSED OPEN E}', # 0xAB
    'ц' : '\N{LATIN SMALL LETTER TURNED V}',
    'г' : '\N{SOUTH EAST ARROW}',
    'х' : '\N{NORTH EAST ARROW}',
    'Ы' : ':',
}

def transcription_to_ipa(s):
    """Converts Mueller's transcription to the IPA"""
    return ''.join(map(lambda c: letters.get(c, c), s))

# -- Parsing the single word

line_re = re.compile('^(.*?)  (.*)')
transcription_re = re.compile('\[(.*?)\]')

def parse_line(s):
    """Given a string from dictionary returns pair (word, article).

    word is the word defined. Article is the source article with transcription
    converted to IPA.
    """

    res = re.match(line_re, s)
    if not res:
        raise RuntimeError("Malformed line "+s)

    (word, article) = res.groups()

    # Splits article to the parts, converting transcription to Unicode
    article_parts = []

    last_processed = 0
    for r in re.finditer(transcription_re, article):
        if r.start() > last_processed:
            article_parts.append(article[last_processed:r.start()])
        article_parts.append(transcription_to_ipa(article[r.start():r.end()]))
        last_processed = r.end()

    if last_processed != len(article):
        article_parts.append(article[last_processed:len(article)])

    return word, ''.join(article_parts)

# -- Formatting single text block with indentation

TEXT_WIDTH = 75
INDENT_WIDTH = 3

# list-name -> (regexp matching the head of the list, maximum length)
list_types = { 'r': (re.compile('_[IV]{1,3}'), 4),
               'd': (re.compile('\d{1,2}\.'), 3),
               'n': (re.compile('\d{1,2}>'), 3),
               'a': (re.compile('[а-я]>'), 3) }

def format_block(s, indentation, header, header_width):
    s = s.strip()
    header = header

    first_line = ((INDENT_WIDTH*indentation) * ' ') + header.ljust(header_width)
    other_lines = (INDENT_WIDTH*indentation + header_width) * ' '

    w = textwrap.TextWrapper(width = TEXT_WIDTH,
                             initial_indent = first_line,
                             subsequent_indent = other_lines)

    return '\n'.join(w.wrap(s))

# -- Converting an article into DICT format

def convert_line(s):
    """Given the article from the dictionary, format it and indentation and wrap to
    page width.
    """

    (word, article) = parse_line(s)

    # Find all list heads occurences
    list_heads = []
    for list_name, (list_re, list_header_width) in list_types.items():
        for i in re.finditer(list_re, article):
            head = i.group()
            if head.endswith('>'):
                head = head[:-1] + ')'
            list_heads.append((i.start(), i.end(), list_name, head))

    list_heads.sort(key=lambda x: x[0])

    # Figure out the lists indentation
    list_levels = {}
    level = 0
    for list_head in list_heads:
        if list_head[2] not in list_levels:
           list_levels[list_head[2]] = level
           level += 1

    # Indent and encode each text block
    result = []
    if len(list_heads) == 0:
        result.append(format_block(article, 0, '', 0))
    else:
        if list_heads[0][0] > 0:
            result.append(format_block(article[0:list_heads[0][0]], 0, '', 0))
        for i in range(0, len(list_heads)-1):
            list_type = list_heads[i][2]
            result.append(format_block(article[list_heads[i][1]:list_heads[i+1][0]],
                                       list_levels[list_type],
                                       list_heads[i][3], list_types[list_type][1]))
        list_type = list_heads[-1][2]
        result.append(format_block(article[list_heads[-1][1]:len(s)],
                                   list_levels[list_type],
                                   list_heads[-1][3], list_types[list_type][1]))

    return word, result

def convert_dictionary(fh):
    # Copyright line
    print("%h 00-database-info\n%d")
    print("\n".join(textwrap.wrap(fh.readline(), 75)))

    for s in fh:
        # Technical information, discard
        if s.startswith(' (C) '):
            continue
        (word, article_lines) = convert_line(s)
        print("%h " + word + "\n%d")
        for l in article_lines:
            print("   "+l)

if __name__ == '__main__':
    with io.open(sys.argv[1], 'r', encoding='koi8-r') as fh:
        convert_dictionary(fh)
