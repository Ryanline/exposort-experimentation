# ExpoSort Experimentation

This repository contains a small Python benchmark suite for studying ExpoSort and related deliberately inefficient sorting algorithms. The project accompanies the included paper, [A Survey and Experimental Evaluation of ExpoSort](A%20Survey%20and%20Experimental%20Evaluation%20of%20ExpoSort.pdf), and provides the code and output data used for the experiment.

ExpoSort is a reluctant sorting algorithm introduced by Mikkel Abrahamsen in 2024. It sorts correctly, but does so by repeatedly re-sorting prefixes of the array, producing exponential running time.

## Background

ExpoSort recursively sorts the first `n - 1` elements of an array, compares and possibly swaps the final two elements, and then recursively sorts the first `n - 1` elements again. Its running time satisfies:

```text
T(n) = 2T(n - 1) + theta(1)
```

which gives exponential growth, `theta(2^n)`.

This repository benchmarks ExpoSort against several related algorithms to show how its theoretical behavior appears in practice.

## Algorithms Included

| Algorithm | Description |
| --- | --- |
| ExpoSort | Main algorithm under study; performs two recursive calls on `n - 1` for each non-base case. |
| CubeSort | A close variant of ExpoSort where the second recursive call only happens after a swap. |
| InsertionSort | Practical baseline; included because ExpoSort and CubeSort share its swap sequence. |
| StoogeSort | Classic deliberately inefficient recursive sorting algorithm. |
| SlowSort | Reluctant sorting algorithm based on the multiply-and-surrender paradigm. |

## Repository Structure

```text
.
|-- .gitignore
|-- A Survey and Experimental Evaluation of ExpoSort.pdf
|-- LICENSE
|-- README.md
|-- main.py
`-- results.csv
```

`main.py` contains the benchmark implementation. `results.csv` contains the current benchmark output. The PDF contains the accompanying paper/report.

## Requirements

The benchmark uses only the Python standard library:

- `csv`
- `dataclasses`
- `random`
- `statistics`
- `time`

No third-party Python packages are required to run `main.py`.

## Quick Start

Clone the repository and enter the project directory:

```bash
git clone https://github.com/Ryanline/exposort-experimentation.git
cd exposort-experimentation
```

Run the benchmark:

```bash
python main.py
```

Depending on your local Python setup, you may need to use `python3` or a full Python executable path instead.

## Running the Benchmark

The benchmark is configured near the top of `main.py`:

```python
RANDOM_SEED = 20260616
TRIALS = 101
SIZES = [4, 8, 12, 16, 20, 22, 24]
MODES = ("random", "sorted", "reverse")
```

For each trial and input size, the code generates one random base array. From that same base array it derives three test cases:

- random
- sorted
- reverse-sorted

Every algorithm is run on the same generated test cases. This keeps comparisons between algorithms consistent.

Warning: ExpoSort is intentionally exponential. Increasing the input sizes can make the benchmark impractical very quickly.

## Output Data

Running the benchmark writes `results.csv`.

| Column | Meaning |
| --- | --- |
| `trial_id` | Trial number for the generated input case. |
| `algorithm` | Algorithm name. |
| `n` | Input array length. |
| `mode` | Input category: `random`, `sorted`, or `reverse`. |
| `time_ms` | Runtime for one trial in milliseconds. |
| `calls` | Function or recursive calls counted during the trial. |
| `comparisons` | Element comparisons counted during the trial. |
| `swaps` | Element swaps counted during the trial. |
| `mean_time_ms` | Mean runtime for that algorithm, size, and mode group. |
| `median_time_ms` | Median runtime for that algorithm, size, and mode group. |

## Reproducing the Paper Results

The included results were generated with:

- Python 3.14.3
- Random seed `20260616`
- 101 trials per algorithm/input-size/input-category combination
- Input sizes `4, 8, 12, 16, 20, 22, 24`
- Input modes `random`, `sorted`, and `reverse`

Exact runtimes depend on hardware, operating system behavior, Python version, and interpreter overhead. Operation counts such as calls, comparisons, and swaps are more stable than wall-clock timing.

## Key Results

The benchmark supports the expected theoretical behavior:

- ExpoSort grows exponentially.
- At `n = 24`, ExpoSort reaches `16,777,215` calls.
- ExpoSort's call and comparison counts are effectively independent of input order.
- ExpoSort and InsertionSort have matching swap counts on the tested inputs.
- CubeSort is dramatically faster because its second recursive call is conditional.

## Limitations

This is a Python-level benchmark, so runtime includes interpreter overhead and function-call overhead. The project is intended for empirical and educational analysis, not practical sorting performance. ExpoSort becomes impractical on larger inputs.

## References

- M. Abrahamsen, "ExpoSort: Breaking the quasi-polynomial-time barrier for reluctant sorting," arXiv:2409.00794, Sep. 2024.
- A. Z. Broder and J. Stolfi, "Pessimal algorithms and simplexity analysis," SIGACT News, vol. 16, no. 3, pp. 49-53, 1984.

## License

See [LICENSE](LICENSE). Use of this code or the accompanying results should reference Ryan Brooks and the included paper/report.
