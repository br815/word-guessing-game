# This version of the game is just an extracted copy of the original word_guessing_game() function in v0_nlp.

import re
from random import randint


# This function takes a list of strings as input.
def word_guessing_game(wordlist):
    # The word is randomly chosen from the list
    index = randint(0, len(wordlist)-1)
    print("length of list is %i" %len(wordlist))
    print("index is %i" %index)
    word = wordlist[index]
    # Hard-coded variable for debugging
    # word = "placeholder"

    print("\nLet's play a word guessing game! Here are the rules:")
    print("1. You start with 5 points.")
    print("2. When you guess a letter correctly, you gain as many points as that letter occurs in the word.")
    print("3. When you guess a letter incorrectly, you lose 1 point.")
    print("4. You win if you correctly guess all the letters. You lose if your score goes below 0.")
    print("5. Enter ! at anytime to quit.")

    # Output an "underscore space" for each letter in the word
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
                    word_guessing_game(wordlist)
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
                word_guessing_game(wordlist)
    # End of while loop
# End of word_guessing_game()
