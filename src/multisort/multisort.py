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
cmp_func = cmp_to_key


# .: multisort :.
# spec is a list one of the following
#    <key>
#    (<key>,)
#    (<key>, <opts>)
# where:
#  <key> Property, Key or Index for 'column' in row
#  <opts> dict. Options:
#       reverse: opt - reversed sort (defaults to False)
#       clean: opt - callback to clean / alter data in 'field'
def multisort(rows, spec, reverse:bool=False):
    key=clean=rows_sorted=default=None
    col_reverse=False
    required=True
    for s_c in reversed([spec] if isinstance(spec, (int, str)) else spec):
        if isinstance(s_c, (int, str)):
            key = s_c
        else:
            if len(s_c) == 1:
                key = s_c[0]
            elif len(s_c) == 2:
                key = s_c[0]
                s_opts = s_c[1]
                assert not s_opts is None and isinstance(s_opts, dict), f"Invalid Spec. Second value must be a dict. Got {getClassName(s_opts)}"
                col_reverse = s_opts.get('reverse', False)
                clean = s_opts.get('clean', None)
                default = s_opts.get('default', None)
                required = s_opts.get('required', True)

        def _sort_column(row): # Throws MSIndexError, MSKeyError
            ex1=None
            try:
                try:
                    v = row[key] 
                except Exception as ex:
                    ex1 = ex
                    v = getattr(row, key)
            except Exception as ex2:
                if isinstance(row, (list, tuple)): # failfast for tuple / list
                    raise MSIndexError(ex1.args[0], row, ex1)

                elif required:
                    raise MSKeyError(ex2.args[0], row, ex2)

                else:
                    if default is None: 
                        v = None
                    else:
                        v = default

            if default:
                if v is None: return default
                return clean(v) if clean else v
            else:
                if v is None: return True, None
                if clean: return False, clean(v)
                return False, v

        try:
            if rows_sorted is None:
                rows_sorted = sorted(rows, key=_sort_column, reverse=col_reverse)
            else:
                rows_sorted.sort(key=_sort_column, reverse=col_reverse)

                
        except Exception as ex:
            msg=None
            row=None
            key_is_int=isinstance(key, int)

            if isinstance(ex, MultiSortBaseExc):
                row = ex.row
                if isinstance(ex, MSIndexError):
                    msg = f"Invalid index for {row.__class__.__name__} row of length {len(row)}. Row: {row}"
                else: # MSKeyError
                    msg = f"Invalid key/property for row of type {row.__class__.__name__}. Row: {row}"
            else:
                msg = ex.args[0]
            
            raise MultiSortError(f"""Sort failed on key {"int" if key_is_int else "str '"}{key}{'' if key_is_int else "' "}. {msg}""", row, ex)


    return reversed(rows_sorted) if reverse else rows_sorted
        

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

# For use in the multi column sorted syntax to sort by 'grade' and then 'attend' descending
# dict example:
#    rows_sorted = sorted(rows, key=lambda o: ((None if o['grade'] is None else o['grade'].lower()), reversor(o['attend'])), reverse=True)
# object example:
#    rows_sorted = sorted(rows, key=lambda o: ((None if o.grade is None else o.grade.lower()), reversor(o.attend)), reverse=True)
# list, tuple example:
#    rows_sorted = sorted(rows, key=lambda o: ((None if o[COL_GRADE] is None else o[COL_GRADE].lower()), reversor(o[COL_ATTEND])), reverse=True)
#    where: COL_GRADE and COL_ATTEND are column indexes for values
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
    return None if o == None else type(o).__name__

