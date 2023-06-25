from pathlib import Path

hi = Path("app/documents/hi.txt")

with open(hi, 'r') as f:
    print(f.read())