# GetWiktLang

When this program (the file getwiktlang.py) is run in a Python shell, it will create a bar chart in TkInter of coverage of languages on the English Wiktionary. The black bars indicate the number of lemmas for that language, while the orange bars indicate the ideal number, i.e. how many lemmas there would be if the language had the same lemmas-to-native-speakers ratio as English. If two bars are connected with black filler, then they have the exact same number of lemmas. You can scroll up and down in the chart with the arrow keys; the chart will automatically re-size itself.

You can change the TkInter window size with size.csv.

Required dependencies:
- BeautifulSoup
- TkInter

The supplementary file nativespeakers.py generates nativespeakers.csv, the list of languages by number of speakers.

Additional functions:
- quickList(): Outputs a list of the languages listed in quicklist.txt by the difference between the actual and ideal number of lemmas. Positive values indicate over-representation, negative values indicate under-representation. Feel free to edit quicklist.txt to include your own languages; make sure to include a newline at the end of the list. If you are using IDLE, then you will need to use HTML code for non-ASCII characters.
- createList() outputs a list of all languages into the file all.txt, used by nativespeakers.py.
- createMap(): Coming in a future update.