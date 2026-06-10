import re
import random
import config



class WordGuessingGame:
    def __init__(self, word_list, ruleset):
        self.word_list = word_list
        self.ruleset = ruleset

        self.word = None
        self.display = None
        self.value = None
        self.guesses = []
        self.hints_remaining = None



    def choose_word(self):
        if len(self.word_list) == 0:
            raise ValueError("Congratulations! You have played every word available in the word list.")

        index = random.randint(0, len(self.word_list) - 1)
        self.word = self.word_list.pop(index)

        self.display = [
            '_'
            for _
            in self.word]

        self.value = (self.ruleset.initial_value())
        self.guesses = []



    def display_game_state(self):
        print()
        print(' '.join(self.display))
        print(f"Letters: {len(self.word)}")
        print(f"{self.ruleset.display_label()}: {self.value}")
        print(f"Hints: {self.hints_remaining}")
        print("Guesses:", ' '.join(self.guesses))



    def get_valid_guess(self):
        while True:
            guess = input("Guess a letter: ").lower()

            if guess == config.QUIT_CHAR or guess == config.HINT_CHAR:
                return guess

            if not re.fullmatch(r"[a-z]", guess):
                print("Please enter one letter (a-z).")
                continue

            if guess in self.guesses:
                print("Please enter a letter you haven't already guessed or revealed through hints.")
                continue

            return guess



    def apply_guess(self, guess):
        occurrences = 0

        for i in range(len(self.word)):
            if self.word[i] == guess:
                self.display[i] = guess
                occurrences += 1

        return occurrences



    def print_guess_result(self, correct_guess, occurrences):
        if correct_guess:
            plural = ""
            if occurrences > 1:
                plural = "s"
            # THIS PRINT STMT NEEDS EDITING
            print(f"Right! You found {occurrences} occurrence{plural} of the letter {correct_guess}.")
        else:
            print("Incorrect guess.")

        print(f"{self.ruleset.display_label()}: {self.value}")



    def calculate_hints(self):
        word_length = len(self.word)

        # 1 hint as default, specifically if word caps at the the minimum token length
        num_hints = 1
        # 2 hints if word is at most 2 letters greater than the minimum token length
        if word_length > config.MIN_TOK_LEN and word_length <= (config.MIN_TOK_LEN + 2):
            num_hints = 2
        # 3 hints for words any longer than that
        if word_length > (config.MIN_TOK_LEN + 2):
            num_hints = 3
        
        return num_hints



    def use_hint(self):
        if self.hints_remaining <= 0:
            print("ERROR: No hints remaining.")
            return

        # Find unrevealed unique letters and choose one
        hint_letter = self.get_hint_letter()
        # 
        self.apply_guess(hint_letter)
        # 
        self.guesses.append(hint_letter)
        # 
        self.hints_remaining -= 1

        print(f"Hint used! The letter {hint_letter} was revealed.")
        if self.hints_remaining == 1:
            print(f'You now have {self.hints_remaining} hint remaining.')
        else:
            print(f'You now have {self.hints_remaining} hints remaining.')



    def get_hint_letter(self):
        # Make a set to remove multiple occurrences from the list of available letters, so that all have a 1/len(word) chance to be returned
        available = {
            self.word[i]
            for i in range(len(self.word))
            if self.display[i] == '_'}

        return random.choice(list(available))



    '''def completion_percent_all(self):
        """
        Percentage of ALL letters discovered.
        """
        revealed_letters = sum(
            1
            for char
            in self.display
            if char != '_')

        return (revealed_letters / len(self.word)) * 100'''



    def completion_percent_unique(self):
        """
        Percentage of unique letters discovered.
        """
        unique_letters_in_word = len(set(self.word))
        discovered_letters = len(set(self.display) - {'_'})
        return (discovered_letters / unique_letters_in_word) * 100



    def get_result(self):
        if '_' not in self.display:
            return "WIN"
        if self.ruleset.has_lost(self.value):
            return "LOSS"
        return None



    def play(self):
        self.choose_word()
        self.hints_remaining = self.calculate_hints()
        self.ruleset.print_rules()
        result = None

        while True:
            self.display_game_state()
            guess = self.get_valid_guess()

            if guess == config.QUIT_CHAR:
                print(f'The word was "{self.word}".')
                result = "QUIT"
                break

            if guess == config.HINT_CHAR:
                self.use_hint()
                continue

            self.guesses.append(guess)

            occurrences = (self.apply_guess(guess))

            correct_guess = (occurrences > 0)

            self.value = (self.ruleset.update(self.value, correct_guess, occurrences))

            self.print_guess_result(correct_guess, occurrences)

            result = self.get_result()

            if result == "WIN":
                # Display final solved word for player
                self.display_game_state()
                print(f"\nCongratulations! You solved \"{self.word}\"!")
                break

            if result == "LOSS":
                print(f"\nYou lost. The word was \"{self.word}\".")
                break

        # Dict to be returned for statistics
        return {
            "mode": self.ruleset.display_label(),
            "result": result,
            "score": self.value,
            "guesses": len(self.guesses),
            "completion": self.completion_percent_unique()}