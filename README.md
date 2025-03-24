### Inizializzazione

```bash
cd < percorso >
poetry new < nome_progetto >
```
### Impostare il parent Folding corretto
```vscode
<nome_progetto>/
├── tests/
│   └── __init__.py
├── venv/
│   ├── pycache.py
│   └── __init__.py
├── poetry.lock
├── pyproject.toml
└── README.md
```

### Installazione Dipendenze

```vscode
Entrare in pyproject.toml e cambiare la versione in "requires-python = "<4.0.0,>=3.10"
```

```bash
poetry add chainlit
poetry add < nome_dipendenza >
poetry install
```

### Avvio


Se esistente:
# lanciamo il venv
source /c/Users/<nome_utente>/AppData/Local/pypoetry/Cache/virtualenvs/<nome_progetto>-<hash>/Scripts/activate


# lanciamo l'assistente
cd <nome_progetto>

poetry install
eval $(poetry env activate)
 
chainlit run <nome_progetto>/__init__.py -w



```bash
chainlit run < nome_progetto >
```

### Configurazione

```vscode
creare un file "config.py" in < nome_progetto >/< nome_modello >
```

Dentro il file scriveremo:
```python
class Config:
    LLM_MODEL = "llama3.2"
    LLM_MODEL_LOW = "deepseek-r1:1.5b"
    AI_API_URL = "https://api.llama-api.com/"
    AI_API_KEY = "ea15cdbd-3610-4d97-a512-d42e4be9d598"
```