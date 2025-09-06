"""Working with a Virtual Library (90 min)
Build a tiny in-memory library manager.
FEATURES
- add_book(title, author, year)
- search(query) by title or author
- checkout(title) / return_book(title)
- list_by_year()
ACCEPTANCE
- All functions pure (no print), return values only
- Write at least 10 unit tests in _tests.py
"""

from typing import List, Dict

class Library:
    def __init__(self):
        self.books = []  # dicts: {title, author, year, checked_out: bool}

    def add_book(self, title: str, author: str, year: int) -> None:
        # TODO: implement
        self.books.append({"title": title, "author": author, "year": year, "checked_out": False})

    def search(self, query: str) -> List[Dict]:
        q = query.lower()
        return [b for b in self.books if q in b["title"].lower() or q in b["author"].lower()]

    def checkout(self, title: str) -> bool:
        for b in self.books:
            if b["title"].lower() == title.lower() and not b["checked_out"]:
                b["checked_out"] = True
                return True
        return False

    def return_book(self, title: str) -> bool:
        for b in self.books:
            if b["title"].lower() == title.lower() and b["checked_out"]:
                b["checked_out"] = False
                return True
        return False

    def list_by_year(self) -> List[Dict]:
        return sorted(self.books, key=lambda b: (b["year"], b["title"]))

def _demo():
    lib = Library()
    lib.add_book("Clean Code","Robert C. Martin",2008)
    lib.add_book("Automate the Boring Stuff","Al Sweigart",2015)
    print(lib.search("code"))

if __name__ == "__main__":
    _demo()
