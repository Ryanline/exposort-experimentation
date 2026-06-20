from dataclasses import dataclass
from statistics import mean, median
from time import perf_counter_ns
import random
import csv


# Configuration
RANDOM_SEED = 20260616
TRIALS = 101
SIZES = [4, 8, 12, 16, 20, 22, 24]
MODES = ("random", "sorted", "reverse")


# Metrics
@dataclass
class Stats:
    calls: int = 0
    comparisons: int = 0
    swaps: int = 0


# Sorting algorithms
def expo_sort(a, n=None, stats=None):
    if stats is None:
        stats = Stats()
    if n is None:
        n = len(a)
    stats.calls += 1
    if n > 1:
        expo_sort(a, n - 1, stats)
        stats.comparisons += 1
        if a[n - 2] > a[n - 1]:
            a[n - 2], a[n - 1] = a[n - 1], a[n - 2]
            stats.swaps += 1
        expo_sort(a, n - 1, stats)
    return stats


def cube_sort(a, n=None, stats=None):
    if stats is None:
        stats = Stats()
    if n is None:
        n = len(a)
    stats.calls += 1
    if n > 1:
        cube_sort(a, n - 1, stats)
        stats.comparisons += 1
        if a[n - 2] > a[n - 1]:
            a[n - 2], a[n - 1] = a[n - 1], a[n - 2]
            stats.swaps += 1
            cube_sort(a, n - 1, stats)
    return stats


def insertion_sort(a):
    stats = Stats(calls=1)
    for j in range(1, len(a)):
        i = j
        while i > 0:
            stats.comparisons += 1
            if a[i - 1] > a[i]:
                a[i - 1], a[i] = a[i], a[i - 1]
                stats.swaps += 1
                i -= 1
            else:
                break
    return stats


def stooge_sort(a, i=0, j=None, stats=None):
    if stats is None:
        stats = Stats()
    if j is None:
        j = len(a) - 1
    stats.calls += 1
    if i >= j:
        return stats
    stats.comparisons += 1
    if a[i] > a[j]:
        a[i], a[j] = a[j], a[i]
        stats.swaps += 1
    if j - i + 1 > 2:
        t = (j - i + 1) // 3
        stooge_sort(a, i, j - t, stats)
        stooge_sort(a, i + t, j, stats)
        stooge_sort(a, i, j - t, stats)
    return stats


def slowsort(a, i=0, j=None, stats=None):
    if stats is None:
        stats = Stats()
    if j is None:
        j = len(a) - 1
    stats.calls += 1
    if i >= j:
        return stats
    m = (i + j) // 2
    slowsort(a, i, m, stats)
    slowsort(a, m + 1, j, stats)
    stats.comparisons += 1
    if a[m] > a[j]:
        a[m], a[j] = a[j], a[m]
        stats.swaps += 1
    slowsort(a, i, j - 1, stats)
    return stats


# Algorithm registry
ALGORITHMS = {
    "ExpoSort": expo_sort,
    "CubeSort": cube_sort,
    "InsertionSort": insertion_sort,
    "StoogeSort": stooge_sort,
    "SlowSort": slowsort,
}


# Test set generation
def add_test_case(test_cases, trial_id, n, mode, arr, expected):
    test_cases.setdefault((mode, n), []).append({
        "trial_id": trial_id,
        "n": n,
        "mode": mode,
        "input": arr,
        "expected": expected,
    })


def make_random_array(n, rng):
    if n < 3:
        raise ValueError("random test arrays require n >= 3")

    arr = list(range(n))
    rng.shuffle(arr)
    sorted_arr = list(range(n))
    reverse_arr = list(reversed(sorted_arr))

    while arr == sorted_arr or arr == reverse_arr:
        rng.shuffle(arr)

    return arr


def make_test_cases(trials, sizes, rng):
    test_cases = {}

    for trial_id in range(1, trials + 1):
        for n in sizes:
            random_arr = make_random_array(n, rng)
            sorted_arr = sorted(random_arr)
            reverse_arr = list(reversed(sorted_arr))

            for mode, arr in (
                ("random", random_arr),
                ("sorted", sorted_arr),
                ("reverse", reverse_arr),
            ):
                add_test_case(test_cases, trial_id, n, mode, arr, sorted_arr)

    return test_cases


def run_trial(name, test_case):
    arr = test_case["input"]
    expected = test_case["expected"]
    data = arr.copy()

    t0 = perf_counter_ns()
    stats = ALGORITHMS[name](data)
    t1 = perf_counter_ns()

    if data != expected:
        trial_id = test_case["trial_id"]
        n = test_case["n"]
        mode = test_case["mode"]
        raise RuntimeError(
            f"{name} failed on trial={trial_id}, n={n}, mode={mode}"
        )

    return {
        "trial_id": test_case["trial_id"],
        "algorithm": name,
        "n": test_case["n"],
        "mode": test_case["mode"],
        "time_ms": (t1 - t0) / 1_000_000,
        "calls": stats.calls,
        "comparisons": stats.comparisons,
        "swaps": stats.swaps,
    }


def benchmark(output_csv="results.csv", trials=TRIALS):
    rows = []
    rng = random.Random(RANDOM_SEED)
    test_cases = make_test_cases(trials, SIZES, rng)

    for name in ALGORITHMS:
        for mode in MODES:
            for n in SIZES:
                trial_rows = [
                    run_trial(name, test_case)
                    for test_case in test_cases[(mode, n)]
                ]

                median_time = median(r["time_ms"] for r in trial_rows)
                mean_time = mean(r["time_ms"] for r in trial_rows)
                for row in trial_rows:
                    row["mean_time_ms"] = mean_time
                    row["median_time_ms"] = median_time
                rows.extend(trial_rows)

    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


# Script entry point
if __name__ == "__main__":
    benchmark()
