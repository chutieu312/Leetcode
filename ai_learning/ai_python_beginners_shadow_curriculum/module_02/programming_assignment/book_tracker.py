"""Book Tracker (120 min)
Persist tasks/books to CSV.
FEATURES
- add/list/find/remove
- mark read, rating 1–5, started/finished dates
- CLI menu loop; autosave to books.csv
ACCEPTANCE
- Covers happy path + 8+ edge cases
- No crashes on bad input; input sanitized
"""
import csv, sys
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class Book:
    title: str
    author: str
    read: bool = False
    rating: int | None = None

class BookDB:
    def __init__(self, path=Path("books.csv")):
        self.path = Path(path)
        self.rows: list[Book] = []

    def load(self):
        if self.path.exists():
            with self.path.open(newline='', encoding='utf-8') as f:
                for row in csv.DictReader(f):
                    self.rows.append(Book(row['title'], row['author'], row['read']=='True', int(row['rating']) if row['rating'] else None))

    def save(self):
        with self.path.open('w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=["title","author","read","rating"])
            w.writeheader()
            for b in self.rows:
                w.writerow(asdict(b))

    # TODO: add methods add/find/remove/mark_read

def main():
    db = BookDB(); db.load()
    print("Loaded", len(db.rows), "books")
    # TODO: CLI loop

if __name__ == "__main__":
    main()
