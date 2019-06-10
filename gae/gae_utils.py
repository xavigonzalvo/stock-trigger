"""Set of utils for AppEngine."""

import json


def SafeReadLines(filename):
  """Reads all lines from a file making.

  It makes sure there are no spaces at the beginning and end.
  """
  lines = []
  with open(filename) as f:
    for line in f.readlines():
      lines.append(line.strip())
  return lines


def read_json(filename):
  """Reads a json in text mode."""
  with open(filename, 'r') as f:
    return json.loads(f.read())
