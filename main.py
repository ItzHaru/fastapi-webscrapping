import orjson
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# uložené data
class BookRecord(BaseModel):
    title: str
    year: int
    author: str

    @staticmethod
    def from_dict(data: dict):
        record = BookRecord(**data)
        return record


class Problem(BaseModel):
    detail: str


class Database:
    def __init__(self):
        self._data: list = []
    # načtení dat z json souboru
    def load_from_filename(self, filename: str):
        with open(filename, "rb") as f:
            data = orjson.loads(f.read())
            for record in data:
                obj = BookRecord.from_dict(record)
                self._data.append(obj)
    # mazání dat
    def delete(self, id_book: int):
        if 0 < id_book >= len(self._data):
            return
        self._data.pop(id_book)
    # přidání dat
    def add(self, book: BookRecord):
        self._data.append(book)
    # záskání dat
    def get(self, id_book: int):
        if 0 < id_book >= len(self._data):
            return
        return self._data[id_book]
    # získání všech dat
    def get_all(self) -> list[BookRecord]:
        return self._data
    # úprava dat
    def update(self, id_book: int, book: BookRecord):
        if 0 < id_book >= len(self._data):
            return
        self._data[id_book] = book
    # počítá délku dat
    def count(self) -> int:
        return len(self._data)

# načítání dat z books.json
db = Database()
db.load_from_filename('books.json')

app = FastAPI(title="Books API", version="0.1", docs_url="/docs")

app.is_shutdown = False

# vypíše všechna data
@app.get("/books", response_model=list[BookRecord], description="Vrátí seznam knih")
async def get_books():
    return db.get_all()

# vypíše určité data
@app.get("/books/{id_book}", response_model=BookRecord)
async def get_book(id_book: int):
    return db.get(id_book)

# přidání dat
@app.post("/books", response_model=BookRecord, description="Přidáme knihu do DB")
async def post_books(book: BookRecord):
    db.add(book)
    return book

# mazání dat
@app.delete("/books/{id_book}", description="Sprovodíme knihu ze světa", responses={
    404: {'model': Problem}
})
# vymazání dat
async def delete_book(id_book: int):
    book = db.get(id_book)
    if book is None:
        raise HTTPException(404, "Kniha neexistuje")
    db.delete(id_book)
    return {'status': 'smazano'}

# úprava dat
@app.patch("/books/{id_book}", description="Aktualizujeme knihu do DB", responses={
    404: {'model': Problem}
})
# úprava dat
async def update_book(id_book: int, updated_book: BookRecord):
    book = db.get(id_book)
    if book is None:
        raise HTTPException(404, "Kniha neexistuje")
    db.update(id_book, updated_book)
    return {'old': book, 'new': updated_book}