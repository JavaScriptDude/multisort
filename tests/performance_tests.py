import asyncio
import pandas
from random import randint
from multisort import msorted, cmp_func, reversor
import test_util as util
pc = util.pc

students = [
     {'idx': 0, 'name': 'joh', 'grade': 'C', 'attend': 100}
    ,{'idx': 1, 'name': 'jan', 'grade': 'a', 'attend': 80}
    ,{'idx': 2, 'name': 'dav', 'grade': 'B', 'attend': 85}
    ,{'idx': 3, 'name': 'bob' , 'grade': 'C', 'attend': 85}
    ,{'idx': 4, 'name': 'jim' , 'grade': 'F', 'attend': 55}
    ,{'idx': 5, 'name': 'joe' , 'grade': None, 'attend': 55}
]
ITERATIONS = 10
EXTRA_ROW = 500

def main():
    results = asyncio.get_event_loop().run_until_complete(run_tests())
    rrows = []
    for result in results:
        if isinstance(result, Exception): raise result
        rrows.append(result)

    rrows = msorted(rrows, 1)
    table = util.quickTT(['test', 's/iter'])
    for rrow in rrows: table.add_row([rrow[0], f"{(rrow[1] / ITERATIONS):.7f}"])
    print(f"\nSummary for {ITERATIONS} iteration{'s' if ITERATIONS > 1 else ''} with {len(students)} rows:\n{table.draw()}\n")


async def run_tests():
    global students
    
    # Add an additional number of records for testing
    if EXTRA_ROW > 0:
        for i in range(1,EXTRA_ROW+1): 
            students.append({'idx': len(students), 'name':'rnd', 'grade': 'ABCDEF'[randint(0,5)], 'attend': randint(0,100)})

    coroutines = [
        run_cmp_func(students[:]),
        run_msorted(students[:]),
        run_reversor(students[:]),
        run_reversor_func(students[:]),
        run_pandas(students[:]),
    ]
    res = await asyncio.gather(*coroutines, return_exceptions=True)

    return res



async def run_cmp_func(rows):
    sw = util.StopWatch()
    def cmp_student(a,b):
        k='grade'; va=a[k]; vb=b[k]
        if va != vb: 
            if va is None: return -1
            if vb is None: return 1
            return -1 if va > vb else 1
        k='attend'; va=a[k]; vb=b[k]; 
        if va != vb: return -1 if va < vb else 1
        return 0

    for i in range(0,ITERATIONS):
        rows_sorted = sorted(rows, key=cmp_func(cmp_student), reverse=True)
    
    return ('cmp_func', sw.elapsed(prec=7))



async def run_msorted(rows):
    sw = util.StopWatch()
    for i in range(0,ITERATIONS):
        rows_sorted = msorted(rows, spec=(
                ('grade', {'reverse': True, 'clean': lambda v: None if v is None else v.lower()})
               ,('attend', {'reverse': True})
        ), reverse=True)
    return ('msorted', sw.elapsed(prec=7))

async def run_reversor(rows):
    sw = util.StopWatch()
    for i in range(0,ITERATIONS):
        rows_sorted = sorted(rows, key=lambda o: (
                     reversor(None if o['grade'] is None else o['grade'].lower())
                    ,reversor(o['attend'])
        ), reverse=True)
    return ('reversor', sw.elapsed(prec=7))

async def run_reversor_func(rows):
    sw = util.StopWatch()
    def _student_sort(o):
        return ( reversor(None if o['grade'] is None else o['grade'].lower())
                ,reversor(o['attend'])
        )
    for i in range(0,ITERATIONS):
        rows_sorted = sorted(rows, key=_student_sort, reverse=True)

    return ('reversor func', sw.elapsed(prec=7))

async def run_pandas(rows):
    sw = util.StopWatch()

    for i in range(0,ITERATIONS):
        df = pandas.DataFrame(rows[:])
        df.sort_values(by = ['grade', 'attend'], ascending = [False, False], na_position = 'last')
        # d_rows_sorted = list(df.T.to_dict().values())

    return ('pandas', sw.elapsed(prec=7))


if __name__ == '__main__':
  main()