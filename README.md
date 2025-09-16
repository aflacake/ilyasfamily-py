# IlyasFamily Python Implementation
**IlyasFamily** adalah format pertukaran dan penyimpanan data alternatif, seperti JSON tetapi lebih kaya tipe data.

Ekstensi resmi: `.ifamily`.

Repositori ini berisi **implementasi Python** dari spesifikasi [IlyasFamily](https://github.com/aflacake/ilyasfamily-spec).

## Instalasi
```bash
pip install ilyasfamily-py
```

## Contoh Pemakaiaan
```python
from ilyasfamily import Node, dump_file, load_file

person = Node("Person", {"Name": "Budi", "Age": 21})
dump_file(person, "person.ifamily")
loaded = load_file("person_family")

print(loaded)
```

## Lisensi
[Apache-2.0](https://github.com/aflacake/ilyasfamily-py/?tab=Apache-2.0-1-ov-file)
