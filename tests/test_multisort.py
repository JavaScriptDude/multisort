import sys
import unittest
from multisort import multisort
import test_util as util
pc = util.pc

FAILFAST = True

STUDENTS_BASE = [
     (0, 'joh', 'a'  , 100)
    ,(1, 'joe', 'B'  , 80)
    ,(2, 'dav', 'A'  , 85)
    ,(3, 'bob', 'C'  , 85)
    ,(4, 'jim', None , 55)
    ,(5, 'jan', 'B'  , 70)
]
(COL_IDX, COL_NAME, COL_GRADE, COL_ATTEND) = range(0,4)
STUDENT_COLS=['idx', 'name', 'grade', 'attend']

def clean_grade(v):
    if v is None: return v
    return v.upper()


MSORTED_TESTS=[
    ( (2,0,5,1,3,4), [(COL_GRADE, {'reverse': False, 'clean': clean_grade}) , (COL_ATTEND, {'reverse': False})]),
    ( (0,2,1,5,3,4), [(COL_GRADE, {'reverse': False, 'clean': clean_grade}) , (COL_ATTEND, {'reverse': True})]),
    ( (0,2,1,5,3,4), [(COL_GRADE, {'reverse': False, 'clean': clean_grade}) , (COL_ATTEND, {'reverse': True})]),
    ( (4,3,1,5,0,2), [(COL_GRADE, {'reverse': True , 'clean': clean_grade}) , (COL_ATTEND, {'reverse': True})]),
    ( (4,3,5,1,2,0), [(COL_GRADE, {'reverse': True , 'clean': clean_grade}) , (COL_ATTEND, {'reverse': False})]),
    ( (2,1,5,3,0,4), COL_GRADE),
    ( (2,1,5,3,0,4), [COL_GRADE]),
    ( (2,5,1,3,0,4), [COL_GRADE, COL_NAME]),
]


class Student():
    def __init__(self, idx, name, grade, attend): 
        self.idx = idx
        self.name = name
        self.grade = grade
        self.attend = attend
    def __str__(self): return f"[{self.idx}] name: {self.name}, grade: {self.grade}, attend: {self.attend}"
    def __repr__(self): return f"<Student> {self.__str__()}"

class MultiSortBase(unittest.TestCase):

    def _run_tests(self, rows_as, row_as, rows_in):
        test_name = sys._getframe(1).f_code.co_name
        for i, (expected, spec) in enumerate(MSORTED_TESTS):
            for j in range(0,1):
                if j == 0:
                    reverse = False
                else:
                    reverse = True
                    expected = reversed(expected)

                spec = self._fix_SORT_TESTS_spec(spec, row_as)

                if i > 4:
                    pc()

                rows_sorted = multisort(rows_in, spec, reverse=reverse)

                if rows_as == 'list':
                    self.assertIsInstance(rows_in, list)
                elif rows_as == 'tuple':
                    self.assertIsInstance(rows_in, tuple)

                bOk = self._check_sort(expected, rows_sorted, row_as)

                _dump = dump_sort(i, spec, rows_sorted, rows_as, row_as, expected, reverse)

                if not bOk: 
                    self.fail(msg=f"\nTest Name: {test_name}\nTestSet: {i}\n{_dump}\n")
                else:
                    pass
                    # pc(f'\n.: sort_dump :.\n{_dump}\n')

    def _fix_SORT_TESTS_spec(self, spec, row_as):
        if row_as in ('list', 'tuple'):
            return spec
        elif row_as in ('dict', 'object'):
            pass
        else:
            raise Exception(f"Unexpected row_as: {row_as}")

        if isinstance(spec, (int)):
            return STUDENT_COLS[spec]

        a = []
        for spec_c in spec:
            if isinstance(spec_c, int):
                a.append(STUDENT_COLS[spec_c])
            else:
                spec_c = [*spec_c]
                spec_c[0] = STUDENT_COLS[spec_c[0]]
                a.append(tuple(spec_c))
        spec = a

        return tuple(spec)


    def _check_sort(self, expected, rows, row_as) -> bool:
        assert len(expected) == len(STUDENTS_BASE), f"Invalid expected length ({len(expected)}). got: {len(STUDENTS_BASE)} ({expected})"
        indexable = row_as in ('list', 'tuple')
        for i, row in enumerate(rows):
            if row_as == 'list' and not isinstance(row, list):
                self.fail(f"Expecting list but got {util.getClassName(row)}")
            elif row_as == 'tuple' and not isinstance(row, tuple): 
                self.fail(f"Expecting tuple but got {util.getClassName(row)}")
            elif row_as == 'dict' and not isinstance(row, dict): 
                self.fail(f"Expecting dict but got {util.getClassName(row)}")
            elif row_as == 'object' and not isinstance(row, object): 
                self.fail(f"Expecting object but got {util.getClassName(row)}")

            idx = row[0] if indexable else row.idx if row_as == 'object' else row['idx']
            if not expected[i] == idx: return False
        return True



class TupleTests(MultiSortBase):
    # TupleTests.test_list_of_tuples
    def test_list_of_tuples(self):
        (rows_as, row_as, rows_in) = _get_rows_in(rows_list=True, row_as_tuple=True)
        self._run_tests(rows_as, row_as, rows_in)

    # TupleTests.test_tuple_of_tuples
    def test_tuple_of_tuples(self):
        (rows_as, row_as, rows_in) = _get_rows_in(rows_tuple=True, row_as_tuple=True)
        self._run_tests(rows_as, row_as, rows_in)


class DictTests(MultiSortBase):
    # DictTests.test_list_of_dicts
    def test_list_of_dicts(self):
        (rows_as, row_as, rows_in) = _get_rows_in(rows_list=True, row_as_dict=True)
        self._run_tests(rows_as, row_as, rows_in)

    # DictTests.test_tuple_of_dict
    def test_tuple_of_dict(self):
        (rows_as, row_as, rows_in) = _get_rows_in(rows_tuple=True, row_as_dict=True)
        self._run_tests(rows_as, row_as, rows_in)


class ObjectTests(MultiSortBase):
    # ObjectTests.test_list_of_objects
    def test_list_of_objects(self):
        (rows_as, row_as, rows_in) = _get_rows_in(rows_list=True, row_as_obj=True)
        self._run_tests(rows_as, row_as, rows_in)

    # ObjectTests.test_tuple_of_objects
    def test_tuple_of_objects(self):
        (rows_as, row_as, rows_in) = _get_rows_in(rows_tuple=True, row_as_obj=True)
        self._run_tests(rows_as, row_as, rows_in)


def norm_spec_item(spec_c):
    if isinstance(spec_c, (int, str)):
        return (spec_c, None, None)
    else:
        assert isinstance(spec_c, tuple) and len(spec_c) in (1,2),\
            f"Invalid spec. Must have 1 or 2 params per record. Got: {spec_c}"
        if len(spec_c) == 1:
            return (spec_c[0], None, None)
        elif len(spec_c) == 2:
            s_opts = spec_c[1]
            assert not s_opts is None and isinstance(s_opts, dict), f"Invalid Spec. Second value must be a dict. Got {util.getClassName(s_opts)}"
            return (spec_c[0], s_opts.get('reverse', False), s_opts.get('clean', None))


def dump_sort(stest_no, spec, rows, rows_as, row_as, expected, reverse):
    sb = util.StringBuffer('Rows of ')
    sb.a(rows_as)
    sb.a(' sorted by ')
    indexable = row_as in ('list', 'tuple')
    if isinstance(spec, (int, str)):
        sb.a(spec).a(" (a)")
    else:
        for i, spec_c in enumerate(spec):
            (key, desc, clean) = norm_spec_item(spec_c)
            if i > 0: sb.a(", ")
            if indexable:
                sb.a(STUDENT_COLS[key])
            else:
                sb.a(key)
            sb.a(' (d)' if desc else ' (a)')

    if reverse: sb.a(' (reversed)')

    sb.a(':\n')
    
    table = util.quickTT(STUDENT_COLS)

    bOk = True
    for i, row in enumerate(rows):
        if indexable:
            table.add_row(row)
            idx = row[0]
        else:
            if row_as == 'object':
                table.add_row([row.idx, row.name, row.grade, row.attend])
                idx = row.idx
            else:
                table.add_row([row['idx'], row['name'], row['grade'], row['attend']])
                idx = row['idx']
        if not expected[i] == idx: bOk = False

    sb.a(util.pre(table.draw()))
    if bOk:
        sb.a("\n check: pass")
    else:
        sb.a('\n check: FAIL! expected: ').a(expected)

    return sb.ts()




    
def _get_rows_in(rows_list=False, rows_tuple=False, row_as_dict=False, row_as_obj=False, row_as_list=False, row_as_tuple=False):
    if row_as_dict:
        rows_in = [{'idx': r[COL_IDX], 'name': r[COL_NAME], 'grade': r[COL_GRADE], 'attend': r[COL_ATTEND]} for r in STUDENTS_BASE]
    elif row_as_obj:
        rows_in = [Student(*r) for r in STUDENTS_BASE]
    elif row_as_tuple:
        rows_in = [tuple(r) for r in STUDENTS_BASE]
    elif row_as_list:
        rows_in = STUDENTS_BASE

    return ( 'list' if rows_list else 'tuple'
            ,'tuple' if row_as_tuple else 'list' if row_as_list else 'dict' if row_as_dict else 'object'
            ,tuple(rows_in) if rows_tuple else rows_in)


if __name__ == "__main__":
    unittest.main()
    sys.exit(0)


