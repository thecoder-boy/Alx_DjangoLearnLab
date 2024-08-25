# Update book

```python
from bookshelf.models import Book

# Update the title of “1984” to “Nineteen Eighty-Four” and save the changes.
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
```
