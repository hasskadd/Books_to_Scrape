Pour installer cette application dans le répertoire 

## Installation
```bash
git clone git@github.com:hasskadd/Books_to_Scrape.git
```


```bash
cd Books_to_Scrape
```

## Créer un environement Virtuel

```python
python -m venv <nom_env>
```

## Activer l'environement Virtuel

Window
```python
<nom_env>/Scripts/Activate.ps1
```
Mac
```bash
source <nom_env>/bin/activate
```

## Installer les dépendances 

```python
pip freeze > requirements.txt
```

## Lancer l'application 
```bash
python scrap.py
```