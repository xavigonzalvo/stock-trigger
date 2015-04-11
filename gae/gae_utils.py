from google.protobuf import text_format

def ReadTextProto(filename, proto):
    """Reads a protobuf in text mode."""
    with open(filename, 'r') as f:
        text_format.Merge(f.read(), proto)


def SafeReadLines(filename):
    """Reads all lines from a file making.

    It makes sure there are no spaces at the beginning and end.
    """
    lines = []
    with open(filename) as f:
        for line in f.readlines():
            lines.append(line.strip())
    return lines
