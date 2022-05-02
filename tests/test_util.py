import sys
import time
import texttable as tt

def pc(*args):
    if len(args) == 0: return
    if len(args) == 1: print(args[0]); return
    a = []
    for i, v in enumerate(args): a.append( ( v if i == 0 or isinstance(v, (int, float, complex, str)) else str(v) ) )
    print( a[0].format(*a[1:]) )

def quickTT(header:list, max_width:int=120) -> tt:
    table = tt.Texttable(max_width=max_width)
    table.set_cols_align(list('r'*len(header)))
    table.set_cols_dtype(list('t'*len(header)))
    table.set_deco(table.VLINES)
    table.header(header)
    return table

def pre(s, iChars=2):
    sPad = ' ' * iChars
    iF = s.find('\n')
    if iF == -1:
        return sPad + s
    sb = []
    iFL = 0
    while iF > -1:
        sb.append(sPad + s[iFL:iF])
        iFL = iF + 1
        iF = s.find('\n', iF + 1)
    sb.append('' if iF == len(s) else sPad + s[iFL:])
    return '\n'.join(sb)

class StringBuffer:
    def __init__(self, s:str=None):
        self._a=[] if s is None else [s]
    def a(self, v):
        self._a.append(str(v))
        return self
    def al(self, v):
        self._a.append(str(v) + '\n')
        return self
    def ts(self, delim=''):
        return delim.join(self._a)

def getClassName(o):
    if o == None: return None
    return type(o).__name__

def getFuncName(depth=1):
    return sys._getframe(depth).f_code.co_name

class StopWatch:
    def __init__(self):
        self.start()
    def start(self):
        self._startTime = time.time()
    def getStartTime(self):
        return self._startTime
    def elapsed(self, prec=3):
        prec = 3 if prec is None or not isinstance(prec, int) else prec
        diff= time.time() - self._startTime
        return round(diff, prec)