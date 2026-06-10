# Word Guessing Game in Python
## By Bushra Rahman
This repository is for a word guessing game.

## Highlights (NEEDS EDITING)
NLP overview:
1. keyword extraction
2. topic modeling
3. corpus analysis

Text processing:
1. tokenization
2. normalization/filtration
3. POS tagging
4. removing undesired POS
5. lemmatizing using POS
6. frequency counting
7. frequency filtration

Game systems:
1. word selection
2. user input validation
3. scoring system
4. display updating


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

### Download NLTK Data
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
3. This output should simultaneously open a new window for the `NLTK Downloader`. Here, you can select which data to download. If disk space is not a concern, you can download all of the data. However, this project only requires the data in `book` ("Everything used in the `NLTK Book`"). You can re-open the `NLTK Downloader` at any time by repeating the steps in this section.

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
| Tag | Meaning | Example | Allowed in Game? | Corresponding WordNet Tag |
| :-------: | :------: | :-------: | :-------: | :-------: |
| CC | coordinating conjunction | but | &#9744; |
| CD | cardinal number | two | &#9744; |
| DT | determiner | the | &#9744; |
| EX | existential | there | &#9744; |
| FW | foreign word | ciao | &#9744; |
| IN | preposition | on | &#9744; |
| JJ | adjective | big | &#9745; | wordnet.ADJ |
| JJR | comparative adjective | bigger | &#9745; | wordnet.ADJ |
| JJS | superlative adjective | biggest | &#9745; | wordnet.ADJ |
| LS | list marker | A. | &#9744; |
| MD | modal | may | &#9744; |
| NN | noun | car | &#9745; | wordnet.NOUN |
| NNS | plural noun | cars | &#9745; | wordnet.NOUN |
| NNP | proper noun | Mary | &#9744; |
| NNPS | plural proper noun | Marys | &#9744; |
| PDT | predeterminer | _both_ Marys | &#9744; |
| POS | possessive | Mary’s | &#9744; |
| PRP | personal pronoun | she | &#9744; |
| PRP$ | possessive pronoun | hers | &#9744; |
| RB | adverb | badly | &#9744; |
| RBR | comparative adverb | worse | &#9745; | wordnet.ADV |
| RBS | superlative adverb | worst | &#9745; | wordnet.ADV |
| RP | particle | give _up_ | &#9744; |
| SYM | symbol | $ | &#9744; |
| TO | infinitive to | _to_ be | &#9744; |
| UH | interjection | ugh | &#9744; |
| VB | lexical verb | run | &#9745; | wordnet.VERB |
| VBD | past tense verb | ran | &#9745; | wordnet.VERB |
| VBG | gerund or present participle | running | &#9745; | wordnet.VERB |
| VBN | past particple | ran | &#9745; | wordnet.VERB |
| VBP | singular present, not 3rd person | run | &#9745; | wordnet.VERB |
| VBZ | singular present, 3rd person | runs | &#9745; | wordnet.VERB |
| WDT | wh-determiner | which | &#9744; |
| WP | wh-pronoun | who | &#9744; |
| WP$ | possessive wh-pronoun | whose | &#9744; |
| WRB | wh-adverb | when | &#9744; |

## Run Word Guessing Game (NEEDS EDITING)
Open terminal in `word-guessing-game` and run:
<!-- CODE START -->
```
cd src
python main.py
```
<!-- CODE END -->

## TODO FEATURES
* Web crawler?
* (DONE) Multiple different rulesets for game?
* Test cases?
* GUI? / option to quit at any time?
- implement hints in the game? <- 1, 2, or 3 hints depending on word length (must be calculated somehow: 1 or 2 for short words, 3 for all words past a certain length)

## TODO STYLE CHANGES
- (DONE) move all globals to a config.py? (https://docs.python.org/3/faq/programming.html#how-do-i-share-global-variables-across-modules)
- change function documentation to docstrings?
- replace all print stmts' f-strings with C-style strings, or vice-versa?
- include instruction on how to add new game modes to rulesets.py if desired?: "To add a new game mode, create a new subclass of RuleSet and implement the required methods. Define for yourself: (1) how points are gained and lost, and (2) the win and loss conditions."
  1. Add new rulset subclass to rulesets.py
  2. Add it to the RULESETS dict at the bottom of rulesets.py
- include instructions on adding globals:
  1. Add it to config.py <- a global belongs in config.py if it is a developer-adjustable setting, especially if used across multiple source files. Do not create any circular dependencies (eg. The RULESETS dict should not be in config.py because it would require config.py to import classes from rulsets.py, and rulesets.py already has to import config.py).
  2. Import config.py to target source file (do NOT do "from config import global", bc we want global usage to be explicit in the code).
  3. When using a global, write config.global (this is more explicit).

- RIGHT NOW
  1) inspect if/else logic and return logic (i'd prefer explicit if/else blocks instead of if... then unindented return instead of else) (i'd also prefer explicit variables being returned instead of return[long list of items])
  2) edit the instructions being printed for each ruleset; this is a stylistic tweak -- make sure the rules are explicit and make grammatical sense.
  3) then, get to work on converting all printed stmts to f-string, and work on function documentation/commenting.