PI = 3.141592653

def dot(l1, l2):
    if len(l1) != len(l2):
        raise ValueError('List lengths do not match!')

    return sum([l1[a] * l2[a] for a in range(len(l1))])

def column(m, n):
    return [m[i][n] for i in range(len(m))]


def matmul(m1, m2):
    if len(m1[0]) != len(m2):
        raise ValueError('Invalid Matrix Demensions!')
    
    return [[dot(m1[j], column(m2, i)) for i in range(len(m2[j]))] for j in range(len(m1))]


def fct(n):
    if n == 0:
        return 1
    else:
        return n*fct(n-1)

def sin(x):
    a = (x-((x+PI)//(2*PI) * (2*PI)))
    s = 0
    for n in range(10):
        s+=(a**(2*n+1) / fct(2*n+1))*((-1)**n)
    return s

def cos(x):
    return sin(x+(PI/2))

def tan(x):
    return sin(x)/cos(x)

def sqrt(n):
    if n == 0: return 0
    a = n/2
    for i in range(20):
        a = 0.5*(n/a + a)
    return a
