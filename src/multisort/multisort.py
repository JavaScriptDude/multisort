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


# .: msorted :.
# spec is a list one of the following
#    <key>
#    (<key>,)
#    (<key>, <opts>)
# where:
#  <key> Property, Key or Index for 'column' in row
#  <opts> dict. Options:
#       reverse: opt - reversed sort (defaults to False)
#       clean: opt - callback to clean / alter data in 'field'
#       none_first: opt - If True, None will be at top of sort. Default is False (bottom)
class Comparator:
    @classmethod
    def new(cls, *args):
        if len(args) == 1 and isinstance(args[0], (int,str)):
            _c = Comparator(spec=args[0])
        else:
            _c = Comparator(spec=args)
        return cmp_to_key(_c._compare_a_b)

    def __init__(self, spec): 
        if isinstance(spec, (int, str)):
            self.spec = ( (spec, False, None, False), )
        else:
            a=[]
            for s_c in spec:
                if isinstance(s_c, (int, str)):
                    a.append((s_c, None, None, False))
                else:
                    assert isinstance(s_c, tuple) and len(s_c) in (1,2),\
                        f"Invalid spec. Must have 1 or 2 params per record. Got: {s_c}"
                    if len(s_c) == 1:
                        a.append((s_c[0], None, None, False))
                    elif len(s_c) == 2:
                        s_opts = s_c[1]
                        assert not s_opts is None and isinstance(s_opts, dict), f"Invalid Spec. Second value must be a dict. Got {getClassName(s_opts)}"
                        a.append((s_c[0], s_opts.get('reverse', False), s_opts.get('clean', None), s_opts.get('none_first', False)))

            self.spec = a

    def _compare_a_b(self, a, b):
        if a is None: return 1
        if b is None: return -1
        for k, desc, clean, none_first in self.spec:
            try:
                try:
                    va = a[k]; vb = b[k]
                except Exception as ex:
                    va = getattr(a, k); vb = getattr(b, k)

            except Exception as ex:
                raise KeyError(f"Key {k} is not available in object(s) given a: {a.__class__.__name__}, b: {a.__class__.__name__}")

            if clean:
                va = clean(va)
                vb = clean(vb)

            if va != vb:
                if va is None: return -1 if none_first else 1
                if vb is None: return 1 if none_first else -1
                if desc:
                    return -1 if va > vb else 1
                else:
                    return 1 if va > vb else -1

        return 0


def msorted(rows, spec, reverse:bool=False):
    if isinstance(spec, (int, str)):
        _c = Comparator.new(spec)
    else:
        _c = Comparator.new(*spec)
    return sorted(rows, key=_c, reverse=reverse)

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

