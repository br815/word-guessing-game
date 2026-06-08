from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from unicodedata import normalize, combining
from nltk import pos_tag
from collections import Counter
import config

# GLOBALS:
# Global stopwords set so that it doesn't have to be reloaded repeatedly for each token to be checked against.
# Instead of leaving stopwords as list with O(n) linear lookup, set() is used for O(1) hash lookup.
STOPWORDS_SET = set(stopwords.words("english"))
# Global tokenizer. Checks for sequences of uppercase letters or lowercase letters or apostrophes.
TOKENIZER = RegexpTokenizer(r"[A-Za-z'’]+")
# Global lemmatizer.
LEMMATIZER = WordNetLemmatizer()



''' Helper Function 1:		remove_accents()
	Descr:			        This function replaces any accented characters in a text with unaccented characters.
                            It is called by process_text().
	Param:			        input_str
                            String for a text that may contain accented characters.
	Return:			        unaccented_str
					        String for the text with all accented characters replaced. '''
def remove_accents(input_str):
    # Convert to NFKD: decompose characters into base chars + combining (diacritic) chars.
    nfkd_form = normalize('NFKD', input_str)

    # Generator expression used to rejoin base chars into a string.
    unaccented_str = ''.join(
        char 
        for char 
        in nfkd_form 
        if not combining(char)) # if not a combining (diacritic) char.

    return unaccented_str
# End of remove_accents()



''' Helper Function 2:		is_valid_token()
	Descr:			        This function checks if a token passes a series of conditions.
                            It is called by process_text().
	Param:			        tok
                            String for a token.
	Return:			        True OR False
					        Boolean indicating whether the token passes the given conditions. '''
def is_valid_token(tok):
    # Token must not be a contraction (ie. should not contain ' or ’).
    if "'" in tok or "’" in tok:
        if config.PROJECT_DEBUGGER or config.PT_DEBUGGER:
            print("***Token \"%s\" failed filtration check due to: IS CONTRACTION***" %tok)
        return False
    # Token must not be a stopword.
    if tok in STOPWORDS_SET:
        if config.PROJECT_DEBUGGER or config.PT_DEBUGGER:
            print("***Token \"%s\" failed filtration check due to: IS STOPWORD***" %tok)
        return False
    # Token length must be at least (ie. >=) the minimum length.
    if len(tok) < config.MIN_TOK_LEN:
        if config.PROJECT_DEBUGGER or config.PT_DEBUGGER:
            print("***Token \"%s\" failed filtration check due to: LENGTH < %i***" %(tok, config.MIN_TOK_LEN))
        return False

    # Return True if token passes all the previous checks.
    return True
# End of is_valid_token()



''' Function 3:		        process_text()
	Descr:			        This function tokenizes, lemmatizes, and counts lemma frequencies of a given text.
                            It then returns a word list of frequent lemmas in the text.
                            The fundamental processing happening in this function is:
                            [unaccented token 
                            for token 
                            in tokenized(raw_text) 
                            if token != stopword AND token != contraction 
                            AND POS(token) in POS_DICT 
                            AND len(lemmatized(token)) > MIN_TOK_LEN].
                            Because accurate lemmatization requires POS tagging, and POS tagging is expensive on an entire text, 
                            token filtration using is_valid_token() is done first.
                            Token length > MIN_TOK_LEN is checked twice. 
                            First, during token filtration, it helps to reduce the size/cost of POS tagging & lemmatization later.
                            Then, after lemmatization, it is necessary to validate that the shortened words themselves are at least the min length.
	Param:			        raw_text
                            A string of unprocessed text.
	Return:			        frequent_lemmas
					        A list of the lemmas that occur frequently and meet all desired conditions. '''
def process_text(raw_text):
    # 1st: Clean raw text to convert accented words into unaccented words.
    unaccented_text = remove_accents(raw_text)

    # 2nd: Tokenize using RegEx to extract sequences consisting ONLY of letters (A-Z, a-z) or apostrophes (', ’).
    # Contractions are preserved in the tokenization so they can later be cleanly rejected by is_valid_token().
    tokens = TOKENIZER.tokenize(unaccented_text)

    # 3rd: List comprehension used to filter tokens to only those that pass the checks in is_valid_token().
    filtered_tokens = [
        tok                             # Do not lowercase tokens until POS filtration, so that proper nouns remain as is.
        for tok 
        in tokens 
        if is_valid_token(tok.lower())] # Check lowercase tokens because stopwords list is in lowercase.

    # Edge case: if no tokens pass the checks, display error message.
    if len(filtered_tokens) == 0:
        print("ERROR: No valid tokens found in the selected input file.")
        return None

    if config.PROJECT_DEBUGGER or config.PT_DEBUGGER:
        print("***FILTERED TOKENS FROM PROCESS_TEXT():***\n\"%s\"" %filtered_tokens)

    # 4th: POS Tagging.
    # List comprehension used to filter tokens to only those that match the desired POS.
    # The (word, POS) tuple is preserved so that a word's POS can be used later for lemmatization.
    tags = pos_tag(filtered_tokens)
    filtered_pos = [
        (word.lower(), pos)     # Tokens are normalized to lowercase here, once POS filtration is done on each token.
        for word, pos 
        in tags 
        if pos in config.POS_DICT]

    # Edge case: if no tokens pass the checks, display error message.
    if len(filtered_pos) == 0:
        print("ERROR: No valid parts of speech were found in the selected input file.")
        return None
    
    if config.PROJECT_DEBUGGER or config.PT_DEBUGGER:
        print("***FILTERED POS FROM PROCESS_TEXT():***\n\"%s\"" %filtered_pos)

    # 5th: List comprehension used to lemmatize the filtered tokens, using POS information to get more accurate lemmatization.
    all_lemmas = [
        LEMMATIZER.lemmatize(word, config.POS_DICT[pos])   # Use dict mapping to convert pos_tag to WordNet tag.
        for word, pos 
        in filtered_pos]

    # 6th: List comprehension used to validate that the final lemmatized words are at least the min length.
    filtered_lemmas = [
        lemma 
        for lemma 
        in all_lemmas 
        if len(lemma) >= config.MIN_TOK_LEN]

    if config.PROJECT_DEBUGGER or config.PT_DEBUGGER:
        print("***FILTERED LEMMAS FROM PROCESS_TEXT():***\n\"%s\"" %filtered_lemmas)

    # 7th: Count frequencies of each lemma.
    # List comprehension used to further filter lemmas only by those appearing "frequently".
    lemma_counts = Counter(filtered_lemmas)
    frequent_lemmas = [
        lemma 
        for lemma, count 
        in lemma_counts.most_common()   # most_common() returns items sorted by descending frequency.
        if count >= config.MIN_FREQ_VAL]

    # Edge case: if no lemma meets the min freq requirement, just allow words that occur at least once.
    if len(frequent_lemmas) == 0:
        frequent_lemmas = [
            lemma 
            for lemma, count 
            in lemma_counts.most_common() 
            if count >= 1]

    if config.PROJECT_DEBUGGER or config.PT_DEBUGGER:
        print("***FREQUENT LEMMAS FROM PROCESS_TEXT():***\n\"%s\"" %frequent_lemmas)

    return frequent_lemmas
# End of process_text()