#!/usr/bin/env python3
import sys
import argparse
from typing import Iterator, TextIO, Optional
import json
from collections import Counter
import csv
import re

class TextTool:
    """Base class for text processing tools that follow Unix philosophy"""
    def __init__(self, input_stream: TextIO = sys.stdin, output_stream: TextIO = sys.stdout):
        self.input = input_stream
        self.output = output_stream

    def process_line(self, line: str) -> Optional[str]:
        """Process a single line of text. Return None to skip the line."""
        raise NotImplementedException()

    def process_stream(self) -> None:
        """Process the entire input stream, writing to output stream"""
        for line in self.input:
            result = self.process_line(line.rstrip('\n'))
            if result is not None:
                self.output.write(result + '\n')

class Grep(TextTool):
    """Search for lines matching a pattern"""
    def __init__(self, pattern: str, ignore_case: bool = False, invert: bool = False, **kwargs):
        super().__init__(**kwargs)
        flags = re.IGNORECASE if ignore_case else 0
        self.pattern = re.compile(pattern, flags)
        self.invert = invert

    def process_line(self, line: str) -> Optional[str]:
        matches = bool(self.pattern.search(line))
        if matches ^ self.invert:
            return line
        return None

class Cut(TextTool):
    """Extract specific fields from each line"""
    def __init__(self, fields: list[int], delimiter: str = '\t', **kwargs):
        super().__init__(**kwargs)
        self.fields = fields
        self.delimiter = delimiter

    def process_line(self, line: str) -> Optional[str]:
        parts = line.split(self.delimiter)
        try:
            selected = [parts[i] for i in self.fields]
            return self.delimiter.join(selected)
        except IndexError:
            return line  # Return original line if field selection fails

class Sort(TextTool):
    """Sort lines of text"""
    def __init__(self, reverse: bool = False, numeric: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.reverse = reverse
        self.numeric = numeric
        self.lines = []

    def process_line(self, line: str) -> Optional[str]:
        self.lines.append(line)
        return None

    def process_stream(self) -> None:
        """Override to implement sorting"""
        if self.numeric:
            self.lines.sort(key=lambda x: float(x), reverse=self.reverse)
        else:
            self.lines.sort(reverse=self.reverse)
        
        for line in self.lines:
            self.output.write(line + '\n')

class Uniq(TextTool):
    """Remove or count repeated lines"""
    def __init__(self, count: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.count = count
        self.counter = Counter()
        self.last_line = None

    def process_stream(self) -> None:
        for line in self.input:
            line = line.rstrip('\n')
            self.counter[line] += 1

        for line, count in self.counter.most_common():
            if self.count:
                self.output.write(f"{count} {line}\n")
            else:
                self.output.write(f"{line}\n")

def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(description='Unix-style text processing tools')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Grep parser
    grep_parser = subparsers.add_parser('grep', help='Search for patterns')
    grep_parser.add_argument('pattern', help='Pattern to search for')
    grep_parser.add_argument('-i', '--ignore-case', action='store_true', help='Ignore case')
    grep_parser.add_argument('-v', '--invert', action='store_true', help='Invert match')

    # Cut parser
    cut_parser = subparsers.add_parser('cut', help='Extract fields')
    cut_parser.add_argument('-f', '--fields', type=lambda x: [int(i) for i in x.split(',')],
                           help='Fields to extract (comma-separated)')
    cut_parser.add_argument('-d', '--delimiter', default='\t', help='Field delimiter')

    # Sort parser
    sort_parser = subparsers.add_parser('sort', help='Sort lines')
    sort_parser.add_argument('-r', '--reverse', action='store_true', help='Sort in reverse')
    sort_parser.add_argument('-n', '--numeric', action='store_true', help='Sort numerically')

    # Uniq parser
    uniq_parser = subparsers.add_parser('uniq', help='Remove or count repeated lines')
    uniq_parser.add_argument('-c', '--count', action='store_true', help='Print counts')

    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.command == 'grep':
        tool = Grep(args.pattern, args.ignore_case, args.invert)
    elif args.command == 'cut':
        tool = Cut(args.fields, args.delimiter)
    elif args.command == 'sort':
        tool = Sort(args.reverse, args.numeric)
    elif args.command == 'uniq':
        tool = Uniq(args.count)
    else:
        parser.print_help()
        sys.exit(1)

    tool.process_stream()

if __name__ == '__main__':
    main()