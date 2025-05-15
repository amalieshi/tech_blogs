# 🔍 Using Regular Expressions to Parse PDF Test Data into JSON (with Data Validation)

Working with test reports stored in PDF files can be frustrating — especially when you need to extract structured data for automated processing. In this guide, we'll walk through how to use **Python's regular expressions (`re` module)** to:

* Parse test results from PDF files using **PyPDF2**
* Extract patterns using readable and maintainable **named capture groups**
* Validate structured output using **`jsonschema`**
* Understand common **regex syntax**, flags, and best practices

---

## 🧾 The Challenge: Test Reports in PDF Format

Imagine you're given a batch of PDFs containing test results in this format:

```
Test1234    2025-05-10    PASS
Test1235    2025-05-11    FAIL
```

The goal is to extract these results into structured JSON. Regular expressions let us define patterns to find these entries reliably.

---

## 🛠️ Step 1: Extracting Text with PyPDF2

Use `PyPDF2` to read PDF text:

```python
import PyPDF2

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        return "\n".join([page.extract_text() for page in reader.pages])
```

---

## 🧠 Step 2: Using Regex with Named Groups for Readability

Use **named capture groups** (`(?P<name>...)`) to improve readability:

```python
import re

pattern = re.compile(
    r'(?P<test_id>Test\d+)\s+(?P<date>\d{4}-\d{2}-\d{2})\s+(?P<result>PASS|FAIL)',
    re.MULTILINE | re.IGNORECASE
)

matches = pattern.finditer(text)
results = [match.groupdict() for match in matches]
```

---

## 🔏 Step 3: Validate Extracted Data with `jsonschema`

```python
from jsonschema import validate

schema = {
    "type": "object",
    "properties": {
        "test_id": {"type": "string"},
        "date": {"type": "string", "format": "date"},
        "result": {"type": "string", "enum": ["PASS", "FAIL"]}
    },
    "required": ["test_id", "date", "result"]
}

for result in results:
    validate(instance=result, schema=schema)
```

---

## 🔤 Regex Syntax Reference

### 🔠 Basic Elements

| Pattern | Description                      | Example Match                  |
| ------- | -------------------------------- | ------------------------------ |
| `.`     | Any character except newline     | `a.c` → `abc`, `a-c`           |
| `\d`    | Digit (0–9)                      | `\d+` → `123`                  |
| `\D`    | Non-digit                        | `\D+` → `abc`                  |
| `\w`    | Word character (a-zA-Z0-9\_)     | `\w+` → `hello123`             |
| `\W`    | Non-word character               | `\W` → `#`, `.`                |
| `\s`    | Whitespace (space, tab, newline) | `\s` → `' '`, `\n`             |
| `\S`    | Non-whitespace                   | `\S` → `a`, `1`, `_`           |
| `[]`    | Character set                    | `[aeiou]` → `a`, `e`           |
| `[^]`   | Negated set                      | `[^0-9]` → `a`, `B`            |
| `^`     | Start of line or string          | `^Hello` matches `Hello`       |
| `$`     | End of line or string            | `world$` matches `world`       |
| `\b`    | Word boundary                    | `\bword\b` matches `word` only |

---

### 🔁 Quantifiers

| Pattern | Description                 | Example Match                 |
| ------- | --------------------------- | ----------------------------- |
| `*`     | 0 or more repetitions       | `lo*l` → `ll`, `lool`         |
| `+`     | 1 or more repetitions       | `lo+l` → `lol`, `lool`        |
| `?`     | 0 or 1 repetition           | `colou?r` → `color`, `colour` |
| `{m}`   | Exactly m repetitions       | `a{3}` → `aaa`                |
| `{m,n}` | Between m and n repetitions | `a{2,4}` → `aa`, `aaa`        |

---

### 🧩 Grouping and Capturing

| Pattern         | Description                  | Example                   |
| --------------- | ---------------------------- | ------------------------- |
| `(...)`         | Capture group                | `(abc)+` → captures `abc` |
| `(?:...)`       | Non-capturing group          | `(?:abc)+`                |
| `(?P<name>...)` | Named capturing group        | `(?P<year>\d{4})`         |
| `(?P=name)`     | Backreference to named group |                           |

---

### ⚙️ Common Regex Functions in Python

| Function       | Purpose                           |
| -------------- | --------------------------------- |
| `re.findall()` | Return all matches                |
| `re.search()`  | Return first match                |
| `re.match()`   | Match from beginning of string    |
| `re.sub()`     | Substitute matched string         |
| `re.split()`   | Split string on pattern           |
| `re.compile()` | Compile regex with optional flags |
| `re.escape()`  | Escape regex special characters   |

---

### 🚩 Regex Flags

| Flag            | Description                               |
| --------------- | ----------------------------------------- |
| `re.IGNORECASE` | Case-insensitive matching                 |
| `re.MULTILINE`  | `^` and `$` match line boundaries         |
| `re.DOTALL`     | `.` matches newline too                   |
| `re.VERBOSE`    | Allows whitespace and comments in pattern |

---

## 💡 Tips for Readable Regex

* **Use `re.compile()`** for clarity and reuse.
* **Label parts** of your regex with `(?P<name>...)` to make results self-descriptive.
* Use **`re.escape()`** when searching for literal strings that may include regex characters:

```python
term = "Test(123)"
escaped = re.escape(term)
pattern = re.compile(escaped)
```

---

## ✅ Conclusion

By combining PDF parsing, regex with named groups, and JSON Schema validation, you can automate test data extraction and verification cleanly and reliably.

Regex can be intimidating at first, but with practice and smart organization — especially using named groups and clear structure — it becomes a powerful ally in any data extraction task.

