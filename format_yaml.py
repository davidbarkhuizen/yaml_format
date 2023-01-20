import argparse

class Line:

    def __init__(self, raw_line: str):
        self.raw  = raw_line
        
        self.level = len(raw_line) - len(raw_line.lstrip(' ')) 

        rstripped = raw_line.rstrip(' ').rstrip('#').rstrip(' ') 
        stripped = rstripped.lstrip(' ')

        self.line = stripped

    @classmethod
    def normalize_levels(cls, lines: list):
        
        lcd = min([l.level for l in lines if l.level != 0])
        
        for l in lines:
            l.level = l.level // lcd

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

parser = argparse.ArgumentParser(
    prog = 'format_yaml',
    description = 'format yaml')

parser.add_argument('file', default='orb.yml') 
args = parser.parse_args()

source_file_path = args.file

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

lines = None

with open(source_file_path, 'tr') as source_file:
    lines = [Line(l) for l in 
        source_file.read().replace('\r', '').split('\n')]

Line.normalize_levels(lines)

def transform(line: Line, pre_indent: int = 2, level_limit: int = 2, line_length = 80) -> str:
    padded = f'{" " * pre_indent * line.level}{line.line}'
    if line.level < level_limit and line.line.endswith(':'):
        padded = (padded + ' ').ljust(line_length, '#')
    return padded

final = [transform(line) for line in lines]

with open(source_file_path, 'w') as f:
    f.write('\n'.join(final))