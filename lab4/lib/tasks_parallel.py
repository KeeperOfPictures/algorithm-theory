import math
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from random import choice
import random
from string import ascii_lowercase, ascii_uppercase

def area_func(radius: int) -> float:
    return math.pi * radius ** 2

def parallel_circle_areas():
    radii = range(10, 101)
    start = time.perf_counter()
    with ProcessPoolExecutor() as ex:
        results = list(ex.map(area_func, radii))
    exec_time = time.perf_counter() - start
    return exec_time

to_emails = ascii_lowercase + ascii_uppercase + "0123456789_"

def make_email(_):
    return ''.join(choice(to_emails) for _ in range(8)) + "@mail.ru"

def parallel_email_generator(n=100000):
    start = time.perf_counter()
    with ThreadPoolExecutor() as ex:
        emails = list(ex.map(make_email, range(n)))
    exec_time = time.perf_counter() - start
    return exec_time

def check_number(n: int) -> bool:
    return 10 <= abs(n) <= 99

def parallel_filter_string(numbers_str):
    nums = list(map(int, numbers_str.split()))
    start = time.perf_counter()
    with ProcessPoolExecutor() as ex:
        mask = list(ex.map(check_number, nums))
    filtered = [n for n, ok in zip(nums, mask) if ok]
    exec_time = time.perf_counter() - start
    return exec_time
