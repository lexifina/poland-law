# Ustawy obowiązujące: tekst aktualny / Acts in force: current text

Oprócz Konstytucji, ustawy o obywatelstwie polskim i kodeksów (z pełną historią zmian) repozytorium zawiera każdą
obowiązującą ustawę z Dziennika Ustaw, którą API Sejmu (ELI) wymienia jako obowiązującą, w jej obecnym brzmieniu:

- ustawa z tekstem jednolitym: tekst według najnowszego tekstu jednolitego; commit ma datę wejścia w życie ostatniej
  zmiany ujętej w tym tekście i jest podpisany przez Marszałka Sejmu (obwieszczenie); zmiany, które weszły w życie
  później, są wymienione w trailerze `Not-included`;
- ustawa nigdy niezmieniana: tekst ogłoszony, z datą wejścia w życie.

Historia wcześniejszych zmian tych ustaw nie jest jeszcze w repozytorium; zostanie dodana później jako korekty.
Pominięto ustawy zmieniające (o zmianie ...), ustawy zmienione bez tekstu jednolitego, teksty dostępne tylko jako PDF
oraz teksty z tabelami, wzorami lub załącznikami, których parser jeszcze nie czyta. Lista ustaw: `data/ustawy.csv`.

Besides the Constitution, the citizenship act and the codes (with their full history), the repository holds every
act (ustawa) of the Journal of Laws that the Sejm's ELI API lists as in force, in its current wording: an act with
unified texts as the newest one gives it, dated the day the newest amendment in that text took effect and authored
by the Marshal of the Sejm (amendments in force later are listed in a `Not-included` trailer); an act never amended
as published, on the day it took effect. Their earlier history is not here yet; it will be added later as
corrections. Amending acts, acts amended but never consolidated, texts the API has only as PDF, and texts with
tables, formulas or annexes the parser does not read yet were left out. The list: `data/ustawy.csv`.
