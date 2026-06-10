# For POS_DICT.
from nltk.corpus import wordnet



# GAME CHAR SETTINGS
QUIT_CHAR = '!'
HINT_CHAR = '?'



# CODE DEBUGGERS
# Project-wide debugger to print all debug statements.
PROJECT_DEBUGGER = False
# Boolean specifically for main.py (MAIN) to print its debug statements if desired.
MAIN_DEBUGGER = False
# Boolean specifically for process_file.py (PF) to print its debug statements if desired.
PF_DEBUGGER = False
# Boolean specifically for process_text.py (PT) to print its debug statements if desired.
PT_DEBUGGER = False
# GAME_DEBUGGER? Doesn't exist yet...



# TEXT PROCESSING SETTINGS
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