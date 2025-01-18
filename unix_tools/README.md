# Write Your Own wc Tool Challenge

This is my implementation of the ["Write Your Own wc Tool"](https://codingchallenges.fyi/challenges/challenge-wc) challenge from [John Crickett's Coding Challenges](https://codingchallenges.fyi/).

## Overview

This project implements Unix-style command-line text processing tools including functions similar to `grep`, `sort`, `uniq`, and `cut`. It's built following Unix philosophy principles of creating simple, modular tools that can be combined to perform complex tasks.

## Features

- **grep**: Search for pattern matches in text
- **sort**: Sort lines of text (supports numeric sorting)
- **uniq**: Remove duplicate lines or count occurrences
- **cut**: Extract specific fields from each line of text

## Requirements

- Python 3.x

## Installation

1. Clone this repository:
```bash
git clone [your-repository-url]
cd unix_tools
```

2. No additional Python packages are required as this project uses only standard library modules.

## Usage

### Basic Commands

```bash
# Search for pattern
python text_tools.py grep "pattern" < input.txt

# Sort lines
python text_tools.py sort < input.txt

# Count unique occurrences
python text_tools.py uniq -c < input.txt

# Extract fields
python text_tools.py cut -f 0,2 -d ',' < data.csv
```

### Command Options

#### grep
- `-i, --ignore-case`: Case insensitive search
- `-v, --invert`: Invert the match

#### sort
- `-r, --reverse`: Sort in reverse order
- `-n, --numeric`: Sort numerically

#### uniq
- `-c, --count`: Print number of occurrences

#### cut
- `-f, --fields`: Specify fields to extract (comma-separated)
- `-d, --delimiter`: Specify field delimiter (default: tab)

## Testing

Create a sample file and try various commands:

```bash
# Create test file
echo "apple" > sample.txt
echo "banana" >> sample.txt
echo "apple" >> sample.txt
echo "cherry" >> sample.txt

# Test commands
python text_tools.py grep "apple" < sample.txt
python text_tools.py sort < sample.txt
python text_tools.py uniq -c < sample.txt
```

## Project Structure

```
unix_tools/
├── text_tools.py    # Main implementation
└── sample.txt       # Sample test file
```

## Learning Outcomes

Through this project, I learned about:
- Command-line interface design
- Text stream processing in Python
- File I/O handling
- Modular program design
- Unix philosophy principles

## Acknowledgments

This project is part of the Coding Challenges series by [John Crickett](https://codingchallenges.fyi/). 

## Next Steps

Planned improvements:
- Add more Unix text processing tools
- Implement comprehensive test suite
- Add support for regular expressions
- Improve error handling

