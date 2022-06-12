# Pias bysykkel-kart

Dette prosjektet består av et script `get_bysykkel_data.py`, skrevet i Python3, en `requirements.txt` og denne readme'en.
Scriptet skriver ut en liste over alle bysykkelstasjonene i Oslo, med tilgjengelige sykler, låser og adresse i både terminalvinduet og til filen `bysykkelstasjonsstatus.txt`.
Det genererer også et kart med markører for hver stasjon med en tooltip som viser stasjonsnavn og en popup som viser tilgjengelige sykler, låser og adressen.

Instruksjoner for å kjøre scriptet:
1. Naviger til prosjektmappen.
2. Innstaller avhengighetene  ved å kjøre `pip install -r requirements.txt` i terminalen
3. Kjør skriptet ved kommando `python3 get_bysykkel_data.py`. Stasjonsinformasonen- og statusen listes nå i terminalen og i `bysykkelstasjonsstatus.txt`. (NB: Listen er lang og det kan være nyttig å sette scrollback til unlimited for å se hele i terminalen).
4. Dersom man ønsker å se stasjonene med informasjon i kartet kan det startes en lokal server ved å kjøre `python3 -m http.server` i en annen fane i terminalen (fortsatt lokalisert i prosjektmappa).
5. Åpne deretter URLen for den lokale serveren og velg kart.html i directory-listen. Evt. kan den genererte html-filen åpnes i nettleser uten lokal server.
