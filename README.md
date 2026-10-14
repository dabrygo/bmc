# bmc
Aid to memorizing passages of text

## Develop

To setup virtual environment on Windows:

```
> python -m venv venv
> .\venv\Scripts\activate.bat
> pip install -r requirements.txt
```

## Test
To run test suite:

```
> python -m unittest discover -s "./tests" -p "test_*.py" 
```

To view test coverage:

```
> coverage run -m unittest discover -s "./tests" -p "test_*.py"
> coverage report # for text report OR
> coverage html # for html report
```

## Quickstart

Input files currently expected to be of the form:

```
WORD 1:1 Lorem ipsum ...
```

## Instructions

A typical game screen shows blanks for words to guess.
Use first letters of blanked words to reveal the word.
Use forward slash `/` to guess, or reveal parts of the word.
Correctly guess all blanked words to progress through the game.