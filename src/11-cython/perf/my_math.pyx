from libc.math cimport sqrt
import cython

def do_math(start=0, num=10):
    pos = start
    k_sq = 1000 * 1000

    while pos < num:
        pos += 1
        sqrt((pos - k_sq) * (pos - k_sq))