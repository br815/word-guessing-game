# For TEXTS.
import pathlib
# For POS_DICT.
from nltk.corpus import wordnet

### PATH TO REPO'S SUB-DIRECTORY CONTAINING TXT INPUT FILES
TEXTS = pathlib.Path(__file__).resolve().parent.parent / "texts"



### TEST LIST TO TEST WORD GUESSING GAME ON
TEST_LIST = ["pain", "piano", "stuffy", "germane", "asteroid", "inflorescence"]



### SPECIAL CHARS FOR GAME SETTINGS
QUIT_CHAR = '!'
HINT_CHAR = '?'



### CODE DEBUGGERS
# Project-wide debugger to trigger all debug statements.
DEBUG_ALL = False
# Boolean specifically for web_scraper.py to print its debug statements if desired.
WEB_SCRAPER_DEBUGGER = True
# Boolean specifically for web_crawler.py to print its debug statements if desired.
WEB_CRAWLER_DEBUGGER = True
# Boolean specifically for generate_texts.py to print its debug statements if desired.
GENERATE_TEXTS_DEBUGGER = True
# Boolean specifically for process_file.py to print its debug statements if desired.
PROCESS_FILE_DEBUGGER = False
# Boolean specifically for process_text.py to print its debug statements if desired.
PROCESS_TEXT_DEBUGGER = False
# Boolean specifically for word_guess_game.py to print its debug statements if desired.
GAME_DEBUGGER = False
# Two booleans specifically for main.py to print its debug statements if desired:
MAIN_DEBUGGER_TEST_LIST = True
# the one above for the hard-coded test list, and one below for the user-selected word list.
MAIN_DEBUGGER_WORD_LIST = False



### TEXT PROCESSING SETTINGS
# Const for minimum length of a word (eg. 5 letters), for filtration.
MIN_TOK_LEN = 5
# Const for minimum frequency of a word occurring (eg. twice), for filtration.
MIN_FREQ_VAL = 2
# Penn TreeBank POS tags returned by nltk.pos_tag() are NOT compatible with WordNetLemmatizer().
# This global dictionary maps the specified pos_tags to their equivalent WordNet tags.
# Add or remove pos_tags to this dict as desired (and update the POS table in README accordingly).
POS_DICT = {
    # Desired Penn TreeBank tags here are: certain nouns, all verbs, all adjectives, certain adverbs.

    # Nouns:
    "NN": wordnet.NOUN,
    "NNS": wordnet.NOUN,

    # Verbs:
    "VB": wordnet.VERB,
    "VBD": wordnet.VERB,
    "VBG": wordnet.VERB,
    "VBN": wordnet.VERB,
    "VBP": wordnet.VERB,
    "VBZ": wordnet.VERB,

    # Adjectives:
    "JJ": wordnet.ADJ,
    "JJR": wordnet.ADJ,
    "JJS": wordnet.ADJ,

    # Adverbs:
    "RBR": wordnet.ADV,
    "RBS": wordnet.ADV
}