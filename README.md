# python_usage_example
Example of how python is used by S&amp;A

I det følgende antages, at man har åbnet en bash terminal i roden af rpojektet.
Hvis man hellere vil bruge en powershell eller en kommandoterminal, skal man nok lave nogle ændringer til fremgangsmåden beskrevet her.

1.  kør scriptet mk_env.sh, der danner ens virtuelle miljø, og placerer det i src/.venv. Scriptet tager et argument og det er det python exe fil, der danner udgangspunkt i en virtuelle miljø.
2. Kopier .vscode_example til .vscode med kommandoen:
cp -rf .vscode_example .vscode
3. Start vscode med kommandoen:
code .
4. I code tryk "ctrl+shift+p" og søg efter ens python fil i det virtuelle miljø, der lige er dannet i src/.venv
5. Man skal nu have fat i en api nøgle fra DMI, der kan bruges på deres observationsdata (der henvises til https://opendatadocs.dmi.govcloud.dk/DMIOpenData).
6. Denne nøgle kopieres ind i ens launch ud for "DMI_API_KEY"

Man kan nu gå i gang med at debugge programmerne test/test_data.py og main programmet src/wind_prod.

Hvis man vil køre wind_prod programmet fra en bash terminal (windows), så skal man følgende fra en bash terminal i projekt rod:
```
source src/.venv/script/activate
export PYTHONPATH=src
export DMI_API_KEY=xxx (erstat xxx med ens Dmi api key)
python src/wind_prod -f 2024-07-01 -t today-5
```
Output ligger i test folderen og indeholder regneark med korrelationer mellem DMI målestationer observation for vindhastighed og DK2 vindproduktion for vindmøller med en kapacitet på over 50 KW.
Der ligger også to scatterplot. Det ene viser den målestation, der korreler dårligst med DK2 produktionen, mens det andet med den målestation, der har den bedste korrelation.






