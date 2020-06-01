# Spanish Conjugation Question Generator
#### Easily Generate Useful Spanish Conjugation Practice Questions

Using Linguasorb's [Top 100 Spanish Verbs](https://www.linguasorb.com/spanish/verbs/most-common-verbs/1) and @ghidinelli's [Spanish Conjugation database](https://github.com/ghidinelli/fred-jehle-spanish-verbs), this program generates a CSV containing one conjugation question and one solution per line.

## To Use
1. Clone repository and install dependancies in `pipfile`
2. Call `generate.py` with the following optional arguments:
```
-n <int> / --num=<int> : Specify number of generate questions. Maximum is about 1650
-t <int> / --top=<int> : Specify top N number of Spanish verbs. Maximum is 100.
-v : Boolean flag representing the inclusion of the Vostoros object in questions. 
     Vostros is not used in Latin American Spanish, but is common in Spain Spanish
```
