# NDDNUG AI

This repository contains a number of sample projects used in the RAG AI workshop run by the North Dallas Developers users group.

## Setup virtualenv

We recommend running these in a python virtualenv (or something like it). See https://docs.python.org/3/library/venv.html. If you have it installed, download this source code and create a virtual env for yourself.

macOS\Linxu
```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements-mac.txt 
```

Windows
```bash
python -m venv env
./env/Scripts/Activate.ps1 or ./env/Scripts/activate.bat
pip install -r requirements_win.txt 
```
## Samples

### simple-llama-index

```bash
cd simple-llama-index
python run.py
```

### full-rag-groq

This will require running `chromadb` (installed in the requirements file) locally. Open another tab in your terminal, activate the virtual environment, and fire up `chromadb`.

```bash
chroma run
```

Add some pdfs to the `documents` folder. Then run the file to load chroma db.

```bash
python load_chroma_db.py
```

At this point chromadb is running and has data. Now fire up the website.

```bash
flask --app run_ai_server.py run
```

Then go to `http://localhost:5000` and enter a query.

## ChromaDB Admin

Download it: https://github.com/flanker/chromadb-admin

```bash
npm install
# nvm use v20.15.0
npm dev
```


## Sequence

Basic open ai call
Slideshow
simple-llama-index
nddnug-meetings
nddnug-meetings-function
full-rag-groq



