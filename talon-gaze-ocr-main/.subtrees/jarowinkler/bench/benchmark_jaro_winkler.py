# todo combine benchmarks of scorers into common code base
import timeit
import pandas
import numpy as np

def benchmark(name, func, setup, lengths, count):
    print(f"starting {name}")
    start = timeit.default_timer()
    results = []
    for length in lengths:
        test = timeit.Timer(func, setup=setup.format(length, count))
        results.append(min(test.timeit(number=1) for _ in range(7)) / count)
    stop = timeit.default_timer()
    print(f"finished {name}, Runtime: ", stop - start)
    return results

setup ="""
from jarowinkler import JaroWinkler
import jellyfish
import Levenshtein
import string
import random
random.seed(18)
characters = string.ascii_letters + string.digits + string.whitespace + string.punctuation
a      = ''.join(random.choice(characters) for _ in range({0}))
b_list = [''.join(random.choice(characters) for _ in range({0})) for _ in range({1})]
"""

lengths = list(range(1,512,4))
count = 4000

time_jarowinkler = benchmark("jarowinkler",
        '[JaroWinkler.similarity(a, b) for b in b_list]',
        setup, lengths, count)

# this gets very slow, so only benchmark it for smaller values
time_jellyfish = benchmark("jellyfish",
        '[jellyfish.jaro_winkler(a, b) for b in b_list]',
        setup, list(range(1,128,4)), count) + [np.NaN] * 96

time_python_levenshtein = benchmark("python-Levenshtein",
        '[Levenshtein.jaro_winkler(a, b) for b in b_list]',
        setup, list(range(1,256,4)), count) + [np.NaN] * 64

df = pandas.DataFrame(data={
    "length": lengths,
    "jarowinkler": time_jarowinkler,
    "jellyfish": time_jellyfish,
    "python-Levenshtein": time_python_levenshtein
})

df.to_csv("results/jaro_winkler.csv", sep=',',index=False)
