@echo off
rem Point d'entree de l'outil de scraping. Usage : scraper.bat <adresse> [--format markdown|json|texte] [--sortie fichier]
"%~dp0.venv\Scripts\python.exe" "%~dp0src\scraper.py" %*
