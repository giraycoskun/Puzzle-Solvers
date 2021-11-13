# My Search Algorithms

giraycoskun

giraycoksun@sabanciuniv.edu

It is a repo for various puzzle solvers. It requires mySearchAlgorithms python package

**Documentation:** https://giraycoskun.github.io/myPuzzleSolvers/

---

## Contents

- Ballsort Puzzle

## Contents Planned

- Sudoku

- Hashi (Bridges) Puzzle


## Notes

Python Version: 3.9.6

Pip Version: 21.3.1

### Python Development Notes

```
source venv/bin/activate
python -m pip install --upgrade pip
pip freeze > requirements.txt
```

### Usage Notes
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e git+https://github.com/giraycoskun/mySearchAlgorithms.git#egg=mySearchAlgorithms
```

### Documentation Notes

Spinx READTHEDOCS theme

```
sphinx-quickstart
sphinx-apidoc -o ./docs/source/modules/ ./mySearchAlgorithms
python3 -m http.server
```

## References