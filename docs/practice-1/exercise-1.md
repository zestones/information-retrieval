# EXERCISE 1: Inverted Index

```xml
<!-- Documents collection -->
<doc><docno>D0</docno>Citizen Kane</doc>
<doc><docno>D1</docno>Casablanca</doc>
<doc><docno>D2</docno>The Godfather The Godfather</doc>
<doc><docno>D3</docno>Gone with the Wind</doc>
<doc><docno>D4</docno>Lawrence of Arabia</doc>
<doc><docno>D5</docno>The Wizard of Oz The Wizard of Oz</doc>
<doc><docno>D6</docno>The Graduate</doc>
<doc><docno>D7</docno>On the Waterfront</doc>
<doc><docno>D8</docno>Schindler’s List</doc>
<doc><docno>D9</docno>Singin’ in the Rain</doc>
```

**Q1.** Build (manually, in text or spreadsheet files) its inverted index usable for a boolean search. Give a
represention of this index both with postings lists and with an incidence matrix.

> **1.** First step is to apply tokenization, normalization, stemming and stop words removal to the documents. The result is the following:

```
Citizen Kane -> [citizen, kane]
Casablanca -> [casablanca]
The Godfather The Godfather -> [godfather, godfather]
Gone with the Wind -> [gone, wind]
Lawrence of Arabia -> [lawrence, arabia]
The Wizard of Oz The Wizard of Oz -> [wizard, oz, wizard, oz]
The Graduate -> [graduate]
On the Waterfront -> [waterfront]
Schindler’s List -> [schindler, list]
Singin’ in the Rain -> [singing, rain]
```

> **2.** Postings lists representation:

```
citizen -> [D0]
kane -> [D0]
casablanca -> [D1]
godfather -> [D2]
gone -> [D3]
wind -> [D3]
lawrence -> [D4]
arabia -> [D4]
wizard -> [D5]
oz -> [D5, D5]
graduate -> [D6]
waterfront -> [D7]
schindler -> [D8]
list -> [D8]
singing -> [D9]
rain -> [D9]
```

> **3.** Incidence matrix representation:

| Term       | D0  | D1  | D2  | D3  | D4  | D5  | D6  | D7  | D8  | D9  |
| ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| citizen    | 1   | 0   | 0   | 0   | 0   | 0   | 0   | 0   | 0   | 0   |
| kane       | 1   | 0   | 0   | 0   | 0   | 0   | 0   | 0   | 0   | 0   |
| casablanca | 0   | 1   | 0   | 0   | 0   | 0   | 0   | 0   | 0   | 0   |
| godfather  | 0   | 0   | 1   | 0   | 0   | 0   | 0   | 0   | 0   | 0   |
| gone       | 0   | 0   | 0   | 1   | 0   | 0   | 0   | 0   | 0   | 0   |
| wind       | 0   | 0   | 0   | 1   | 0   | 0   | 0   | 0   | 0   | 0   |
| lawrence   | 0   | 0   | 0   | 0   | 1   | 0   | 0   | 0   | 0   | 0   |
| arabia     | 0   | 0   | 0   | 0   | 1   | 0   | 0   | 0   | 0   | 0   |
| wizard     | 0   | 0   | 0   | 0   | 0   | 1   | 0   | 0   | 0   | 0   |
| oz         | 0   | 0   | 0   | 0   | 0   | 1   | 0   | 0   | 0   | 0   |
| graduate   | 0   | 0   | 0   | 0   | 0   | 0   | 1   | 0   | 0   | 0   |
| waterfront | 0   | 0   | 0   | 0   | 0   | 0   | 0   | 1   | 0   | 0   |
| schindler  | 0   | 0   | 0   | 0   | 0   | 0   | 0   | 0   | 1   | 0   |
| list       | 0   | 0   | 0   | 0   | 0   | 0   | 0   | 0   | 1   | 0   |
| singing    | 0   | 0   | 0   | 0   | 0   | 0   | 0   | 0   | 0   | 1   |
| rain       | 0   | 0   | 0   | 0   | 0   | 0   | 0   | 0   | 0   | 1   |
