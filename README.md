# Shadowlogger

Simple wrapper for built-in logger module which formats logs and
adds a passthrough function which can be overridden to add 
additional log handling.

---

![img.png](img.png)

---

## Installation

```bash
pip install shadowlogger
```

---

## Usage

```python
import shadowlogger.logger
```

or 

```python
from shadowlogger.shadowlogger import ShadowLogger


class MyCustomLogger(ShadowLogger):
    # override these to customize the logger
    prefix: str
    name: str
    message_format: str
    log_level: int
    
    # override this to handle the formatted message
    def handle_message(self, formatted_message: str, level_name: str):
        pass
```

---

## Testing

```bash
python -m unittest discover -s tests
```
