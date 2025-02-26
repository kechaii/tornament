from itertools import combinations_with_replacement

TITLE = 'Название'
FONTNAME = 'Groboldov'
QUANTILY_LEAGUE = 6
QUANTILY_GROUP = 6
QUANTILY_GROUP_ONLY = 10
NAME_LEAGUE = ['ММ', 'ЖЖ', 'МЖ']
NAME_LETTER = [chr(65 + i) for i in range(26)]
FORMAT_GAME = ['1/11', '1/15', '1/21', '2/15/11', '2/21/15', '3/11', '3/15', '3/21']
FORMAT_GROUP = {i: ['-'.join(list(j)) for j in
                    list(combinations_with_replacement('6543', i))
                    if sum(map(int, list(j))) <= 24] for i in range(1, QUANTILY_GROUP + 1)}
FORMAT_GROUP_ONLY = {i: ['-'.join(list(j)) for j in
                         list(combinations_with_replacement('6543', i))]
                     for i in range(1, QUANTILY_GROUP_ONLY + 1)}
