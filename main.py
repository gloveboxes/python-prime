'''calculates prime numbers using multiprocessing '''

import time
import math
from multiprocessing import Process, Manager


def is_prime(n):
    '''checks if a number is prime'''
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n))+1, 2):
        if n % i == 0:
            return False
    return True


def calc_primes(proc_num, return_dict, start, end):
    '''calculates prime numbers from start to end'''
    primes = []
    for i in range(start, end):
        if is_prime(i):
            primes.append(i)

    return_dict[proc_num] = primes


def main():
    '''main function'''
    max_num = 1000000
    num_of_processes = 8
    batch_size = max_num // num_of_processes
    start = time.time()

    manager = Manager()
    return_dict = manager.dict()

    processes = []

    for i in range(num_of_processes):
        proc = Process(target=calc_primes, args=(
            i, return_dict, i*batch_size, (i+1)*batch_size))
        proc.start()
        processes.append(proc)

    for proc in processes:
        proc.join()

    primes = []
    list_of_primes = sorted(return_dict.items())
    for i in list_of_primes:
        primes.extend(i[1])

    end = time.time()

    print(primes)
    print("Time taken = {0:.5f}".format(end - start))


if __name__ == '__main__':
    main()
