# This project is for a word guessing game.

import sys
import pathlib
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import re
from random import randint



# This function takes a list of raw text as input
# and outputs the tokens and nouns.
def process_text(raw_text):
    # PART A:
    # List comprehension used to tokenize raw text
    # and reduce tokens to only those that meet the desired requirements:
    # tokens that are alpha (i.e. are words), not stopwords, and are more than 5 letters long.
    desired_tokens = [tok.lower() for tok in word_tokenize(raw_text)
                       if tok.isalpha() and tok not in stopwords.words('english') and len(tok) > 5]
    # print("\nList of desired tokens:", desired_tokens)

    # PART B:
    # List comprehension used to lemmatize processed tokens
    # and reduce to a set of unique lemmas.
    wnl = WordNetLemmatizer()
    all_lemmas = [wnl.lemmatize(tok) for tok in desired_tokens]
    unique_lemmas = list(set(all_lemmas))
    # print('\nSet of unique lemmas:', unique_lemmas)

    # PART C:
    # Do POS tagging on the unique lemmas and print the first 20 tagged
    tags = pos_tag(unique_lemmas)
    # print('\nThe POS tags are:',tags)
    # print("\nThe first 20 POS tags for unique lemmas are:", tags[0:20])
    print("\nThe first 20 POS tags for unique lemmas are:")
    for i in range(20):
        print(str(i+1) + ". " + str(tags[i]))

    # PART D:
    # List comprehension used to get the unique lemmas that are nouns (NN):
    # All pos labels in a pos_tag tuple that start with 'N' are nouns: NN, NNS, NNP, NNPS.
    noun_lemmas = [tag for tag, POS in tags if POS[0] == 'N']
    # print("\nAll lemmas that are NOUNS:", noun_lemmas)

    # PART E:
    # Print the number of tokens from PART A and the number of nouns from PART D.
    print("\nThe number of tokens from part (a) is " + str(len(desired_tokens)) + ".")
    print("The number of nouns from part (d) is " + str(len(noun_lemmas)) + ".")

    # PART F:
    # Return tokens (not unique tokens) from PART A and nouns from PART D.
    # Two values are returned as a tuple.
    return desired_tokens, noun_lemmas

# End of process_text()


# This function takes a list of strings as input.
def guessing_game(wordlist):
    # The word is randomly chosen from the list
    index = randint(0, len(wordlist)-1)
    word = wordlist[index]
    # word = "placeholder"

    print("\nLet's play a word guessing game! Here are the rules:")
    print("1. You start with 5 points.")
    print("2. When you guess a letter correctly, you gain as many points as that letter occurs in the word.")
    print("3. When you guess a letter incorrectly, you lose 1 point.")
    print("4. You win if you correctly guess all the letters. You lose if your score goes below 0.")
    print("5. Enter ! at anytime to quit.")

    # Output to console an "underscore space" for each letter in the word
    str_guess = re.sub('[a-z]', '_ ', word)
    print(str_guess)
    points = 5      # Int for player score
    guess = ''      # Char for player guess
    guesses = ""    # String to store player guesses
    while points > -1 and guess != '!':
        # Validate input to ensure that it is 1 alpha char that hasn't already been guessed
        guess = input("Guess a letter: ").lower()
        while not re.fullmatch('[A-Za-z]', guess) and guess != '!' or guess in guesses:
            if not re.fullmatch('[A-Za-z]', guess):
                guess = input("Please enter one letter (a-z): ").lower()
            elif guess in guesses:
                guess = input("Please enter a letter you haven't already guessed: ").lower()
        guesses += guess  # Put the guess in the string of already-guessed letters.

        # Process input: it is either quit, correct, or incorrect
        if guess == '!':
            print("The word was \"" + word + "\". Your final score is " + str(points))
            quit()  # or return
        elif guess in word:
            # Strings are immutable, so to update the displayed guess string, it first needs to be converted to a list.
            list_guess = list(str_guess)
            occurrences = 0  # Number of times letter occurs in word, used to award points
            for i in range(len(word)):
                if word[i] == guess:
                    occurrences += 1
                    # Target index is i*2 bc str_guess has 2 chars ("_ ") for each char in word.
                    list_guess[i*2] = guess
            str_guess = ''.join(list_guess)  # Convert list back to string using join() on empty string ''
            points += occurrences
            plural = ''
            if occurrences > 1:
                plural = 's'
            print("Right! You earned " + str(occurrences) + " point" + plural + ". Your score is " + str(points) + ".")
        else:
            points -= 1
            # Lose condition: if score goes below 0.
            if points < 0:
                print("Sorry, your score is " + str(points) + ". The word was \"" + word + "\". You lose.")
                restart = input("\nEnter ! to quit. Enter any other character(s) to restart the game. ")
                if restart == '!':
                    print("Goodbye.")
                    quit()
                else:
                    guessing_game(wordlist)
            else:
                print("Sorry, you lost 1 point. Your score is " + str(points) + ".")
        print(str_guess)    # Print updated guess string

        # Win condition: if str_guess without the spaces is the same as the word.
        if str_guess.replace(' ', '') == word:
            print("Congratulations, you solved it! Your final score is " + str(points) + ".")
            restart = input("\nEnter ! to quit. Enter any other character(s) to restart the game. ")
            if restart == '!':
                print("Goodbye.")
                quit()
            else:
                guessing_game(wordlist)
    # End of while loop
# End of guessing_game()


# main()
if __name__ == "__main__":
    # User must specify filename as sysarg[1], otherwise quit
    if len(sys.argv) < 2:
        # The filename "anat19.txt" is specified under Parameters in "Edit Configurations"
        print("ERROR: Please enter a filename as a system arg")
        quit()

    filename = sys.argv[1]  # Save the user-inputted filename

    # Pathlib joins filename to current working directory for cross-platform file opening
    with open(pathlib.Path.cwd().joinpath(filename), "r", encoding="utf-8") as f:
        # File text is read in as raw text
        text_in = f.read()

    # Calculate lexical diversity:
    # List comprehension used to get all words in text (i.e. no punctuation or numbers).
    all_words = [tok.lower() for tok in word_tokenize(text_in) if tok.isalpha()]
    # Then use set() on all_words to create a set only of the unique words in text.
    # lower() was used so that 2 same words won't be considered different in the set just bc one is uppercase.
    unique_words = list(set(all_words))
    # Last, calculate the number of unique tokens divided by the total number of tokens.
    lex_div = len(unique_words)/len(all_words)
    print("The lexical diversity of the text is:", round(lex_div, 2))

    # Preprocess the raw text
    tokens, nouns = process_text(text_in)

    # Make a dictionary of {noun:count of noun in tokens} items from the nouns and tokens lists
    dict_nouns = {}
    for i in range(len(nouns)):
        # Add noun count to dictionary
        dict_nouns[nouns[i]] = tokens.count(nouns[i])
    # print(dict_nouns)

    # Lambda expression used to sort dict_nouns by count of nouns (i.e. by value, not key).
    # Return type is not a dict but a list due to sorted(). Each list element is a {key:value} tuple.
    sorted_noun_counts = sorted(dict_nouns.items(), key=lambda x: x[1], reverse=True)
    print(sorted_noun_counts)

    # Print the 50 most common nouns and their counts
    amount = 50
    print("\nThe top " + str(amount) + " most common nouns and their counts are:")
    for i in range(amount):
        print(str(i+1) + ". " + str(sorted_noun_counts[i]))

    # List comprehension with slicing used to extract nouns from the list of tuples
    common_nouns = [noun for noun, count in sorted_noun_counts][0:amount]
    # print(common_nouns)

    # Guessing game on the list of most common nouns
    guessing_game(common_nouns)

# End of main()
