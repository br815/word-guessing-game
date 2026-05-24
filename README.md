# Word Guessing Game in Python
## By Bushra Rahman
This repository is for a word guessing game.

## Highlights (NEEDS EDITING)
* keyword extraction
* topic modeling
* corpus analysis
Order:
1. tokenize
2. normalize/filter
3. POS tag
4. remove undesired POS
5. lemmatize using POS
6. frequency count
7. frequency filter

## Install Python (and Pip)
Python is necessary to run this project.

To install the latest version of Python (Python 3) on Windows 11 or less, follow these instructions:
1. Download the latest version of Python from [the official Python website](https://www.python.org/downloads/).
2. Run the installer.
3. Add Python to the `Path` Environment Variable. [This YouTube video](https://www.youtube.com/watch?v=uadGsNA6h5Q) has the steps to follow:
    * Open `Control Panel >> System and Security >> System >> Advanced System Settings`.\
    (Alternatively, open `Settings >> System >> About >> Advanced System Settings`.)\
    This opens a window for `System Properties`.
    * In `System Properties`, go to `Environment Variables`.\
    In `Environment Variables`, look down at `System variables` and scroll until you reach `Path`.\
    Select `Path` and hit `Edit`.
    * Once you’ve opened `Edit environment variable`, find the file path for Python’s `/bin` folder in your File Explorer and copy it.\
    It should look similar to:
    <!-- CODE START -->
    ```
    C:\Users\Owner\AppData\Local\Python\bin
    ```
    <!-- CODE END -->
    * Go back to `Edit environment variable`, hit `New`, and paste the file path for `/bin`.
    * Then hit `OK` in `Edit environment variable`, hit `OK` in `Environment Variables`, and hit `OK` in `System Properties`.
    * Python should now be properly installed and locatable within `Path`. To test in the terminal, run:
    <!-- CODE START -->
    ```
    python --version                  # could alternatively type python3 or py
    ```
    <!-- CODE END -->
    You should see output similar to:
    <!-- CODE START -->
    ```
    Python 3.14.4
    ```
    <!-- CODE END -->
    Additionally, make sure `pip` is properly installed. Since Python was installed from [the official Python website](https://www.python.org/downloads/), `pip` should have come with the installation. To test in the terminal, run:
    <!-- CODE START -->
    ```
    pip --version
    ```
    <!-- CODE END -->
    You should see output similar to:
    <!-- CODE START -->
    ```
    pip 26.0.1 from C:\Users\Owner\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\pip (python 3.14)
    ```
    <!-- CODE END -->
4. After installing Python and adding it to `Path`, make sure to restart your IDE to avoid compilation errors.

## Install NLTK
The Python library `NLTK` is necessary to run the NLP portion of this project.

To install `NLTK`, open the terminal and run:

<!-- CODE START -->
```
pip install nltk
```
<!-- CODE END -->

<details><summary>You should see output similar to:</summary>

<!-- DROPDOWN CODE START -->
```
Collecting nltk
  Downloading nltk-3.9.4-py3-none-any.whl.metadata (3.2 kB)
Collecting click (from nltk)
  Downloading click-8.3.3-py3-none-any.whl.metadata (2.6 kB)
Collecting joblib (from nltk)
  Downloading joblib-1.5.3-py3-none-any.whl.metadata (5.5 kB)
Collecting regex>=2021.8.3 (from nltk)
  Downloading regex-2026.4.4-cp314-cp314-win_amd64.whl.metadata (41 kB)
Collecting tqdm (from nltk)
  Downloading tqdm-4.67.3-py3-none-any.whl.metadata (57 kB)
Collecting colorama (from click->nltk)
  Downloading colorama-0.4.6-py2.py3-none-any.whl.metadata (17 kB)
Downloading nltk-3.9.4-py3-none-any.whl (1.6 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.6/1.6 MB 2.2 MB/s  0:00:00
Downloading regex-2026.4.4-cp314-cp314-win_amd64.whl (280 kB)
Downloading click-8.3.3-py3-none-any.whl (110 kB)
Downloading colorama-0.4.6-py2.py3-none-any.whl (25 kB)
Downloading joblib-1.5.3-py3-none-any.whl (309 kB)
Downloading tqdm-4.67.3-py3-none-any.whl (78 kB)
Installing collected packages: regex, joblib, colorama, tqdm, click, nltk
   ━━━━━━━━━━━━━━━━━━━━╺━━━━━━━━━━━━━━━━━━━ 3/6 [tqdm]  WARNING: The script tqdm.exe is installed in 'C:\Users\Owner\AppData\Local\Python\pythoncore-3.14-64\Scripts' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╺━━━━━━ 5/6 [nltk]  WARNING: The script nltk.exe is installed in 'C:\Users\Owner\AppData\Local\Python\pythoncore-3.14-64\Scripts' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
Successfully installed click-8.3.3 colorama-0.4.6 joblib-1.5.3 nltk-3.9.4 regex-2026.4.4 tqdm-4.67.3

[notice] A new release of pip is available: 26.0.1 -> 26.1
[notice] To update, run: C:\Users\Owner\AppData\Local\Python\pythoncore-3.14-64\python.exe -m pip install --upgrade pip
```
<!-- DROPDOWN CODE END -->
</details>

## Download NLTK Data
After installing `NLTK`, you will need to download some or all of its data.

To download `NLTK` data, follow these instructions:
1. Open the terminal and type `python` (or `python3`) to open the Python interactive shell.
  <!-- CODE START -->
  ```
  python
  ```
  <!-- CODE END -->
  You should see output similar to:
  <!-- CODE START -->
  ```
  Python 3.14.4 (tags/v3.14.4:23116f9, Apr  7 2026, 14:10:54) [MSC v.1944 64 bit (AMD64)] on win32
  Type "help", "copyright", "credits" or "license" for more information.
  ```
  <!-- CODE END -->
2. In the Python shell, run:
  <!-- CODE START -->
  ```
  >>> import nltk
  >>> nltk.download()
  ```
  <!-- CODE END -->
  You should see output similar to:
  <!-- CODE START -->
  ```
  showing info https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/index.xml
  ```
  <!-- CODE END -->
3. This output should simultaneously opens a new window for the `NLTK Downloader`. Here, you can select which data to download. If disk space is not a concern, you can download all of the data. However, this project only requires the data in `book` ("Everything used in the `NLTK Book`"). (You can re-open the `NLTK Downloader` at any time by repeating the steps in this section.)

To view your downloaded `NLTK` data in File Explorer, note the Download directory specified in the `NLTK Downloader`. It should look similar to:
  <!-- CODE START -->
  ```
  C:\Users\Owner\AppData\Roaming\nltk_data
  ```
  <!-- CODE END -->
4. Finally, close the the `NLTK Downloader` and end the Python shell:
  <!-- CODE START -->
  ```
  >>> quit()
  ```
  <!-- CODE END -->

## Install Requests & Beautiful Soup
The Python libraries `Requests` and `Beautiful Soup` are necessary to run the web crawler portion of this project.

To install `Requests`, open the terminal and run:
<!-- CODE START -->
```
pip install requests
```
<!-- CODE END -->
To install `Beautiful Soup`, open the terminal and run:
<!-- CODE START -->
```
pip install bs4
```
<!-- CODE END -->

<details><summary>You should see output similar to:</summary>

<!-- DROPDOWN CODE START -->
```
Collecting requests
  Downloading requests-2.33.1-py3-none-any.whl.metadata (4.8 kB)
Collecting charset_normalizer<4,>=2 (from requests)
  Downloading charset_normalizer-3.4.7-cp314-cp314-win_amd64.whl.metadata (41 kB)
Collecting idna<4,>=2.5 (from requests)
  Downloading idna-3.13-py3-none-any.whl.metadata (8.0 kB)
Collecting urllib3<3,>=1.26 (from requests)
  Downloading urllib3-2.7.0-py3-none-any.whl.metadata (6.9 kB)
Collecting certifi>=2023.5.7 (from requests)
  Downloading certifi-2026.4.22-py3-none-any.whl.metadata (2.5 kB)
Downloading requests-2.33.1-py3-none-any.whl (64 kB)
Downloading charset_normalizer-3.4.7-cp314-cp314-win_amd64.whl (159 kB)
Downloading idna-3.13-py3-none-any.whl (68 kB)
Downloading urllib3-2.7.0-py3-none-any.whl (131 kB)
Downloading certifi-2026.4.22-py3-none-any.whl (135 kB)
Installing collected packages: urllib3, idna, charset_normalizer, certifi, requests
   ━━━━━━━━━━━━━━━━╺━━━━━━━━━━━━━━━━━━━━━━━ 2/5 [charset_normalizer]  WARNING: The script normalizer.exe is installed in 'C:\Users\Owner\AppData\Local\Python\pythoncore-3.14-64\Scripts' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
Successfully installed certifi-2026.4.22 charset_normalizer-3.4.7 idna-3.13 requests-2.33.1 urllib3-2.7.0

[notice] A new release of pip is available: 26.0.1 -> 26.1
[notice] To update, run: C:\Users\Owner\AppData\Local\Python\pythoncore-3.14-64\python.exe -m pip install --upgrade pip
```
<!-- CODE END -->
And:
<!-- CODE START -->
```
Collecting bs4
  Downloading bs4-0.0.2-py2.py3-none-any.whl.metadata (411 bytes)
Collecting beautifulsoup4 (from bs4)
  Downloading beautifulsoup4-4.14.3-py3-none-any.whl.metadata (3.8 kB)
Collecting soupsieve>=1.6.1 (from beautifulsoup4->bs4)
  Downloading soupsieve-2.8.3-py3-none-any.whl.metadata (4.6 kB)
Collecting typing-extensions>=4.0.0 (from beautifulsoup4->bs4)
  Downloading typing_extensions-4.15.0-py3-none-any.whl.metadata (3.3 kB)
Downloading bs4-0.0.2-py2.py3-none-any.whl (1.2 kB)
Downloading beautifulsoup4-4.14.3-py3-none-any.whl (107 kB)
Downloading soupsieve-2.8.3-py3-none-any.whl (37 kB)
Downloading typing_extensions-4.15.0-py3-none-any.whl (44 kB)
Installing collected packages: typing-extensions, soupsieve, beautifulsoup4, bs4
Successfully installed beautifulsoup4-4.14.3 bs4-0.0.2 soupsieve-2.8.3 typing-extensions-4.15.0

[notice] A new release of pip is available: 26.0.1 -> 26.1
[notice] To update, run: C:\Users\Owner\AppData\Local\Python\pythoncore-3.14-64\python.exe -m pip install --upgrade pip
```
<!-- DROPDOWN CODE END -->
</details>

## POS Tags
| Tag | Meaning | Example | Allowed Here? | Corresponding WordNet Tag |
| :-------: | :------: | :-------: | :-------: | :-------: |
| CC | coordinating conjunction | but | ❌ |
| CD | cardinal number | two | ❌ |
| DT | determiner | the | ❌ |
| EX | existential | there | ❌ |
| FW | foreign word | ciao | ❌ |
| IN | preposition | on | ❌ |
| JJ | adjective | big | ✅ | wordnet.ADJ |
| JJR | comparative adjective | bigger | ✅ | wordnet.ADJ |
| JJS | superlative adjective | biggest | ✅ | wordnet.ADJ |
| LS | list marker | A. | ❌ |
| MD | modal | may | ❌ |
| NN | noun | car | ✅ | wordnet.NOUN |
| NNS | plural noun | cars | ✅ | wordnet.NOUN |
| NNP | proper noun | Mary | ❌ |
| NNPS | plural proper noun | Marys | ❌ |
| PDT | predeterminer | _both_ Marys | ❌ |
| POS | possessive | Mary’s | ❌ |
| PRP | personal pronoun | she | ❌ |
| PRP$ | possessive pronoun | hers | ❌ |
| RB | adverb | badly | ❌ |
| RBR | comparative adverb | worse | ✅ | wordnet.ADV |
| RBS | superlative adverb | worst | ✅ | wordnet.ADV |
| RP | particle | give _up_ | ❌ |
| SYM | symbol | $ | ❌ |
| TO | infinitive to | _to_ be | ❌ |
| UH | interjection | ugh | ❌ |
| VB | lexical verb | run | ✅ | wordnet.VERB |
| VBD | past tense verb | ran | ✅ | wordnet.VERB |
| VBG | gerund or present participle | running | ✅ | wordnet.VERB |
| VBN | past particple | ran | ✅ | wordnet.VERB |
| VBP | singular present, not 3rd person | run | ✅ | wordnet.VERB |
| VBZ | singular present, 3rd person | runs | ✅ | wordnet.VERB |
| WDT | wh-determiner | which | ❌ |
| WP | wh-pronoun | who | ❌ |
| WP$ | possessive wh-pronoun | whose | ❌ |
| WRB | wh-adverb | when | ❌ |

## Run Word Guessing Game (NEEDS EDITING)
Open terminal in `Word_Guessing_Game` and run:
<!-- CODE START -->
```
cd src
python main.py
```
<!-- CODE END -->

## TODO
* Web crawler?
* Multiple different rulesets for game?
* Test cases?
* GUI? / option to quit at any time?