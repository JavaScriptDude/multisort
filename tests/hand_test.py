
from multisort import multisort, mscol
import test_util as util
pc = util.pc


def main():

    test_multisort_dict_single()
    test_multisort_obj_single()
    test_multisort_tuple_single()
    test_multisort_dict_multi()
    test_multisort_dict_multi_no_mscol()
    test_multisort_obj_multi()
    test_multisort_tuple_multi()
    test_list_basic()


students_dict = [
     {'idx': 0, 'name': 'joh', 'grade': None, 'attend': 100},
     {'idx': 1, 'name': 'jan', 'grade': 'a', 'attend': 80},
     {'idx': 2, 'name': 'dav', 'grade': 'B', 'attend': 85},
     {'idx': 3, 'name': 'bob', 'grade': 'C', 'attend': 85},
     {'idx': 4, 'name': 'jim', 'grade': 'F', 'attend': 55},
     {'idx': 5, 'name': 'joe', 'grade': None, 'attend': 55}
]


class Student():
    def __init__(self, idx, name, grade, attend):
        self.idx = idx
        self.name = name
        self.grade = grade
        self.attend = attend

    def __str__(self):
        return f"name: {self.name}, grade: {self.grade}, attend: {self.attend}"

    def __repr__(self):
        return self.__str__()


students_obj = [
    Student(0, 'joh', 'C', 100),
    Student(1, 'jan', 'a', 80),
    Student(2, 'dav', 'B', 85),
    Student(3, 'bob', 'C', 85),
    Student(4, 'jim', 'F', 55),
    Student(5, 'joe', None, 55),
]

student_tuple = [
     (0, 'joh', 'C', 100),
     (1, 'jan', 'a', 80),
     (2, 'dav', 'B', 85),
     (3, 'bob', 'C', 85),
     (4, 'jim', 'F', 55),
     (5, 'joe', None, 55)
]
(COL_IDX, COL_NAME, COL_GRADE, COL_ATTEND) = range(0, 4)


def test_multisort_dict_single():
    _sorted = multisort(students_dict, 'grade', reverse=False)
    _print_res(_sorted)


def test_multisort_obj_single():
    _sorted = multisort(students_obj, 'attend', reverse=False)
    _print_res(_sorted)


def test_multisort_tuple_single():
    _sorted = multisort(student_tuple, COL_ATTEND, reverse=False)
    _print_res(_sorted)


def test_multisort_dict_multi():
    _sorted = multisort(students_dict, [
            mscol('grade', reverse=True, clean=lambda s: None if s is None else 
                  s.upper(), default='0', required=True),
            mscol('attend', reverse=False),
    ], reverse=False)
    _print_res(_sorted)


def test_multisort_dict_multi_no_mscol():
    _sorted = multisort(students_dict, [
            ('grade', True, lambda s: None if s is None else s.upper(),
             '0', True),
            ('attend', False),
    ], reverse=False)
    _print_res(_sorted)


def test_multisort_obj_multi():
    _sorted = multisort(students_obj, [
            mscol('grade', reverse=True),
            mscol('attend')
    ], reverse=False)
    _print_res(_sorted)


def test_multisort_tuple_multi():
    _sorted = multisort(student_tuple, [
            mscol(COL_GRADE, reverse=True),
            mscol(COL_ATTEND)
    ], reverse=False)
    _print_res(_sorted)


def test_list_basic():
    _print_res(multisort([1, 4, 3, 6, 5], reverse=False))
    _print_res(multisort([1, 4, 3, 6, 5], reverse=True))


def _print_res(rows):
    print(f"\n{util.getFuncName(2)}() Results:")
    for row in rows:
        print(util.pre(str(row)))
    print('\n')


if __name__ == '__main__':
    main()
