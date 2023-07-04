from data_collection import output_text
from pathlib import Path

z = Path('datasets/')

texts, targets = output_text(z)
print(texts)
print(targets)


