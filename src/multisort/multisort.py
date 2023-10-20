#########################################
# .: multisort.py :.
# Simplified Multi-Column Sorting For Lists of records
# Installation:
# . pip install multisort
# Author: Timothy C. Quinn
# Home: https://pypi.org/project/multisort
# Licence: MIT
#########################################
from functools import cmp_to_key
from typing import Union
cmp_func = cmp_to_key


# multisort - Non-destructive sorter with multi column support
# [rows] list of records to sort
# [spec] list/tuple one of <key> or <spec> or list/tuple(of <spec>)
#   items by order in tuple:
#     [key] Key or Index for 'column' in row
#     [reverse] reversed sort (defaults to False) (opt)
#     [clean] callback to clean / alter data in 'field' (opt)
#     [default] Value to default if None is found or required = False (opt)
#     [required] Will not fail if key not found (opt)
# [reverse] reverse the sort (defaults to False)
# Other:
#   mscol: Helper to simplify construction of <spec> record(s) eg:
#     multisort(rows, [mscol('colname1', reverse=True),
#                      mscol('colname2', reverse=True, default=1)]
#     # as opposed to:
#     multisort(rows, [('colname1', True),
#                      ('colname2', True, None, 1)]
def multisort(rows: list,
              spec: Union[int, str, list, tuple] = None,
              reverse: bool = False):

    if spec is None:
        _clone = rows[:]
        _clone.sort(reverse=reverse)
        return _clone

    rows_sorted = None
    if isinstance(spec, (int, str)):
        spec = [mscol(spec)]
    for spec_c in reversed(spec):
        spec_c_t = type(spec_c)
        if spec_c_t in (int, str):
            (key, col_reverse, clean, default, required) \
                    = (spec_c, False, None, None, True)
        else:
            assert spec_c_t in (list, tuple), \
                    f"Invalid spec. Got: {spec_c_t.__name__}. See docs"
            if len(spec_c) < 5:
                spec_c = mscol(*spec_c)
            (key, col_reverse, clean, default, required) = spec_c

        def _sort_column(row):  # Throws MSIndexError, MSKeyError
            ex1 = None
            try:
                try:
                    v = row[key]
                except Exception as ex:
                    ex1 = ex
                    v = getattr(row, key)
            except Exception as ex2:
                if isinstance(row, (list, tuple)):  # failfast for tuple / list
                    raise MSIndexError(ex1.args[0], row, ex1)

                elif required:
                    raise MSKeyError(ex2.args[0], row, ex2)

                else:
                    if default is None:
                        v = None
                    else:
                        v = default

            if default:
                if v is None:
                    return default
                return clean(v) if clean else v
            else:
                if v is None:
                    return True, None
                if clean:
                    return False, clean(v)
                return False, v

        try:
            if rows_sorted is None:
                rows_sorted = sorted(rows,
                                     key=_sort_column,
                                     reverse=col_reverse)
            else:
                rows_sorted.sort(key=_sort_column, reverse=col_reverse)

        except Exception as ex:
            sb = []
            msg = None
            row = None
            key_is_int = isinstance(key, int)

            if isinstance(ex, MultiSortBaseExc):
                row = ex.row
                if isinstance(ex, MSIndexError):
                    sb.append(f"Invalid index for {row.__class__.__name__}")
                    sb.append(f" row of length {len(row)}. Row: {row}")
                else:  # MSKeyError
                    sb.append("Invalid key/property for row of type")
                    sb.append(f" {row.__class__.__name__}. Row: {row}")
                msg = ' '.join(sb)
            else:
                msg = ex.args[0]

            msg = "Sort failed on key {0}{1}{2}. {3}".format(
                            "int" if key_is_int else "str '",
                            key,
                            '' if key_is_int else "' ",
                            msg)
            raise MultiSortError(msg, row, ex)

    return reversed(rows_sorted) if reverse else rows_sorted


def mscol(key, reverse=False, clean=None, default=None, required=True):
    return (key, reverse, clean, default, required)


class MultiSortBaseExc(Exception):
    def __init__(self, msg, row, cause):
        self.message = msg
        self.row = row
        self.cause = cause


class MSIndexError(MultiSortBaseExc):
    def __init__(self, msg, row, cause):
        super(MSIndexError, self).__init__(msg, row, cause)


class MSKeyError(MultiSortBaseExc):
    def __init__(self, msg, row, cause):
        super(MSKeyError, self).__init__(msg, row, cause)


class MultiSortError(MultiSortBaseExc):
    def __init__(self, msg, row, cause):
        super(MultiSortError, self).__init__(msg, row, cause)

    def __str__(self):
        return self.message

    def __repr__(self):
        return f"<MultiSortError> {self.__str__()}"


# reversor() For use in the multi column sorted
#                syntax to sort by 'grade'and then 'attend' descending
#  Dict example:
#     rows_sorted = sorted(rows,
#                   key=lambda o: (\
#                        (None if o['grade'] is None else o['grade'].lower()),\
#                         reversor(o['attend'])), reverse=True)
#  Object example:
#     rows_sorted = sorted(rows,
#         key = lambda o: ((None if o.grade is None else o.grade.lower()), \
#                                reversor(o.attend)),
#         reverse = True)
#  List, Tuple example:
#     rows_sorted = sorted(rows, key=lambda o:\
#              ((None if o[COL_GRADE] is None else o[COL_GRADE].lower()),
#              reversor(o[COL_ATTEND])), reverse=True)
#     where: COL_GRADE and COL_ATTEND are column indexes for values


class reversor:
    def __init__(self, obj):
        self.obj = obj

    def __eq__(self, other):
        return other.obj == self.obj

    def __lt__(self, other):
        return False if self.obj is None else \
               True if other.obj is None else \
               other.obj < self.obj


def getClassName(o):
    return None if o is None else type(o).__name__