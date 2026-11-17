# Logdelta

Logdelta is a Python CLI tool for analyzing application logs.

It uses [Drain3](https://github.com/logpai/Drain3) to identify recurring log
patterns and provides two commands:

- `summary`: Extract log templates and count their occurrences.
- `compare`: Compare log templates between two log files and identify changes.

## Features

- Automatic log template extraction using Drain3(for now, more algorithms to come)
- Support for analyzing multiple log files together.
- Comparison of log template frequencies.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/Gleventis/logdelta.git
cd logdelta
uv sync
```

Verify the installation:

```bash
uv run logdelta --help
```

## Usage

### Summary

The `summary` command extracts recurring log templates and counts their
occurrences.

```bash
uv run logdelta summary examples/before.log
```

You can also analyze multiple files together:

```bash
uv run logdelta summary examples/before.log examples/after.log
```

All supplied files are processed together to produce a single summary.

Example output:

| Template                   | Count |
|----------------------------|------:|
| Application started        |     5 |
| Database connection failed |     2 |
| Request timeout exceeded   |     2 |

### Compare

The `compare` command identifies differences in log template frequencies
between two files.

```bash
uv run logdelta compare examples/before.log examples/after.log
```

Example output:

| Template                   | Before | After | Delta |
|----------------------------|-------:|------:|------:|
| Application started        |      2 |     3 |    +1 |
| Database connection failed |      2 |     0 |    -2 |
| Request timeout exceeded   |      0 |     2 |    +2 |

The delta is calculated as:

`delta = after_count - before_count`

- Positive delta: The template occurs more frequently in the second file.
- Negative delta: The template occurs less frequently in the second file.
- Zero delta: The occurrence count is unchanged.

Templates that exist in only one file are also included in the comparison.

**Note:** Each file is mined independently. Templates are matched using their
extracted template strings rather than their internal cluster IDs.

## How It Works

Logdelta processes logs through the following stages:

1. **Reading:** Read log entries from the supplied files.
2. **Parsing:** Convert log entries into structured Log objects.
3. **Mining:** Use Drain3 to discover recurring log templates.
4. **Analysis:** Summarize template frequencies or compare two sets of templates.
5. **Formatting:** Display the results using Rich tables.

## Development

Install the project with its development dependencies:

```bash
uv sync
```

Run the test suite:

```bash
uv run pytest
```

Build the package:

```bash
uv build
```

This produces a Python wheel and source distribution inside `dist/`.

## Disclaimer

Logdelta is currently under development.
