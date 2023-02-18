# Python Validator v1.0

Python Validator is a program that takes an image of a scanned passport and returns the passport holder's information and photo.


## Usage

```python
from passport_validators import analyzer
from passport_validators import face_detection

# returns the passport-holders data in a multi-line format
passport_analyzer = analyzer.PassportMachineReadableZoneAnalyzer(file)
passport_analyzer.parse()

# takes the passport holder's face photo and extracts it into a separate 'result.png' file
face_detection.recognize_passport_face(file)
```

## Libraries

- [PassportEye](https://passporteye.readthedocs.io/en/latest/) is used to extract MRZ out of a passport photo. This made my job easier for parsing the extracted data. I decided to create a way to parse data myself in the end, using the library only to get the raw MRZ string. 
- [Face-recongition](https://pypi.org/project/face-recognition/) to extract the person's face out of a passport photo. This was a better option than using other more complicated libraries.
- [pycountry](https://www.icao.int/publications/pages/publication.aspx?docnum=9303) to get a country out of its ISO 3166-1 alpha-3 code.

## Implementation standards

The program uses information from [ICAO 9303](https://www.icao.int/publications/pages/publication.aspx?docnum=9303) to verify passport MRZ data. Moreover, it implements the ICAO 9303 *digit check algorithm* to provide further validation for the data in terms of the passport holder's: passport number, birth date and passport expiration date (indicated by either **True** or **False**). 

The program also stores any *optional data* stored through the MRZ. This is used by individual countries and its meaning is specific to each country. The program does not further parse nor analyze this data.

The program currently only incorporates the following things out of ICAO 9303 standards:

- Location of the specific information in the MRZ lines
- Digit check algorithms in three cases
- Official country names with ISO 3166-1 alpha-3 codes



## Live examples


If provided with the following image of a [passport](https://i.imgur.com/QcHa9tW.jpeg) (which is fake) it will print the following result:
```
NAME: GHEZALI
SURNAME: MEHDI-MUHAMMED
DOCUMENT TYPE: Passport
NATIONALITY: Kingdom of Sweden
PASS NUMBER: 45492416< (True)
BIRTH DATE: 07/05/79 (True)
SEX: Male
EXP. DATE: 07/28/14 (True)
OPT. DATA: 19790705
```
Moreover, it will also extract the [passport holder's face](https://i.imgur.com/vioKnPW.png).

