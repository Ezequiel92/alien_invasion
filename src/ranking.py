import operator
from datetime import datetime

####################################################################################################
# Order and formating of ranking rows functions
####################################################################################################


def sort_scores(score_dict):
    """
    Sorts an score dictionary, the priority is
    'high_score' (higher first) ->
    'lives_left' (higherfirst) ->
    'date' (sooner first)
    """

    score_list = list(score_dict.items())

    # scores = [[Username, Highest score, Lives left, Date]]
    scores = [
        [
            item[0],
            item[1]["high_score"],
            item[1]["lives_left"],
            _srt_date_to_milliseconds(item[1]["date"]),
        ]
        for item in score_list
    ]

    # Sort by date first, sooner first.
    scores.sort(key=operator.itemgetter(3))

    # Sort by score and lives left, higher first.
    scores.sort(key=operator.itemgetter(1, 2), reverse=True)

    return scores


def set_date_and_idx(rows):
    """
    Adds the ranking index to each row and
    convert the date in milliseconds to a string
    """
    i = 1
    for row in rows:
        # Add the ranking index.
        row.insert(0, i)
        # Get the date as string from the date in Unix milliseconds.
        row[4] = _milliseconds_to_str_date(row[4])
        i += 1

    return rows


def get_max_len(data, idx):
    """
    Returns the maximum length among elements
    of index idx[i] in data, for every i
    """
    max_len = []
    for i in idx:
        maxim = max([len(str(item[i])) for item in data])
        max_len.append([i, maxim])

    return max_len


def get_str_for_ranking(scores, maxim):
    """Constructs the string for a row of the ranking"""

    # Get the white space necessary to generate equal length rows.
    sep = _get_white_spaces(scores, maxim)

    row = (
        f"{sep[0]}{scores[0]}   {scores[1]}{sep[1]}  {sep[2]}{scores[2]}"
        + f"   {sep[3]}{scores[3]}   {scores[4]}{sep[4]}"
    )
    return row


####################################################################################################
# Auxiliary functions
####################################################################################################


def _srt_date_to_milliseconds(srt_date):
    """Returns the date in Unix milliseconds from the date as string"""

    # The input format is YYYY-MM-DD, HH:MM:SS.
    date = datetime.strptime(srt_date, "%Y-%m-%d, %H:%M:%S")

    return date.timestamp() * 1000


def _milliseconds_to_str_date(milliseconds):
    """Returns the date as a string from the date in Unix milliseconds"""

    # The output format is HH:MM, YYYY-MM-DD.
    date = datetime.fromtimestamp(milliseconds / 1000).strftime("%H:%M, %Y-%m-%d")

    return date


def _get_white_spaces(row, max):
    """
    Calculates the necessary whitespace to add to each
    element of data, given the maximum length between the
    elements in each corresponding position of data
    """

    # e.g. max = [[idx_1, max_len_1], [idx_2, max_len_2], ...]
    # e.g. spaces = {"1": "  ", "2": "", ...}
    whitespaces = {}
    for i in max:
        whitespace = i[1] - len(str(row[i[0]]))
        sep = "".join(" " for j in range(whitespace))
        whitespaces[i[0]] = sep

    return whitespaces
