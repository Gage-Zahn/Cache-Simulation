import csv
import math
import cache


def run_test(block_size, set_num, blocks_per_set, recent_use, tests):
    test_cache = cache.Cache(block_size, set_num, blocks_per_set, recent_use)
    hit = 0
    total = 0
    for t in tests:
        hit += test_cache.check(t)
        total += 1

    return float(hit/total)


def read_tests(name):
    tests = []
    with open(name, "r") as file:
        line = file.readline()
        while line.__len__() > 1:
            tests.append(line[4:12])
            line = file.readline()
    return tests


set_nums = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
blocks = [1, 2, 4, 8]
block_sizes = [32, 64, 128]
recent_uses = [1, 0]
size = 1024

results = []

t = read_tests("gcc.trace")

#while size <= 2**17:
for s in set_nums:
    print("Set:", s)
    for bs in block_sizes:
        for b in blocks:
            for r in recent_uses:
                results.append([bs, s, b, r, run_test(bs, s, b, r, t)])
    #size *= 2

with open("results.csv", "w+") as results_csv:
    csv_writer = csv.writer(results_csv, delimiter=',')
    csv_writer.writerows(results)