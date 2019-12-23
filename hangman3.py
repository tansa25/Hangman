# Problem Set 2, hangman.py
# Name: Tanya Korniyenko
# Collaborators: Eduard Tsakhlo
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"

    is_guessed = True

    for letter in secret_word:
        if letter not in letters_guessed:
            is_guessed = False
    
    return is_guessed


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"

    word = ''

    for letter in secret_word:
        if letter in letters_guessed:
            word += letter
        else:
            word += '_'

    return word


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"

    ascii_low = string.ascii_lowercase

    letters = set( ascii_low ) - set( letters_guessed )
    letters = list( letters )
    letters.sort()
    letters = ''.join( letters )

    return letters
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    
    length = len(secret_word)
    warnings = 3
    guesses_remaining = 6
    letters_guessed = []
    is_run_out_of_guesses = False
    vowels = 'aeiou'
    is_with_hints = False

    print("""Welcome to the game Hangman!
You are allowed to write only one alphabetical symbol in any case.
I am thinking of a word that is {} letters long.
You have {} warnings left.
{}""".format(length, warnings, '-' * 10))

    while not( is_word_guessed( secret_word, letters_guessed ) or guesses_remaining <= 0 ):
        print('You have {} guesses left. Available letters: {}'.format(guesses_remaining, get_available_letters(letters_guessed)))
        letter = input('Please guess a letter: ').lower()

        while len(letter) != 1 or not letter.isalpha() or letter in letters_guessed:
            guessed_word = get_guessed_word(secret_word, letters_guessed)

            if(letter == "*" and is_with_hints):
                show_possible_matches(guessed_word)
                letter = input('Please guess a letter: ').lower()
                continue
            warnings -= 1

            if warnings != 0:
                if letter in letters_guessed:
                    print(f'Oops! You\'ve already guessed that letter. You have {warnings} warnings left: {guessed_word}')
                else:
                    print(f'Oops! That is not a valid letter. You have {warnings} warnings left: {guessed_word}')
            else:
                guesses_remaining -= 1
                print(f'You have no warnings left so you lose one guess. {guesses_remaining} guesses left: {guessed_word}')

                if guesses_remaining <= 0:
                    print('-' * 10)
                    break

            letter = input('Please guess a letter: ').lower()

        letters_guessed.append(letter)

        if letter in secret_word:
            print('Good guess: {}'.format(get_guessed_word(secret_word, letters_guessed)))
        else:
            guesses_remaining -= 2 if letter in vowels else 1
            print('Oops! That letter is not in my word: {}'.format(get_guessed_word(secret_word, letters_guessed)))
        print('-' * 10)

    if guesses_remaining > 0:
        score = guesses_remaining * len(set(secret_word))
        print('Congratulations, you won!\nYour total score for this game is: {}'.format(score))
    else:
        print('Sorry, you ran out of guesses. The word was {}'.format(secret_word))



# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    my_word = my_word.replace(' ', '')
    conditions = []

    if len( my_word ) == len( other_word ):
        for index, letter in enumerate( my_word ):
            conditions.append( letter == other_word[index] or (letter == '_' and my_word.count(other_word[index]) == 0))
    
        return all( conditions )
    return False

def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    matches = []

    for other_word in wordlist:
        if match_with_gaps( my_word, other_word ):
            matches.append( other_word )

    if matches:
        print( *matches )
    else:
        print( 'No matches found' )


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    length = len(secret_word)
    warnings = 3
    guesses_remaining = 6
    letters_guessed = []
    is_run_out_of_guesses = False
    vowels = 'aeiou'
    is_with_hints = True

    print("""Welcome to the game Hangman!
You are allowed to write only one alphabetical symbol in any case.
I am thinking of a word that is {} letters long.
You have {} warnings left.
{}""".format(length, warnings, '-' * 10))

    while not( is_word_guessed( secret_word, letters_guessed ) or guesses_remaining <= 0 ):
        print('You have {} guesses left. Available letters: {}'.format(guesses_remaining, get_available_letters(letters_guessed)))
        letter = input('Please guess a letter: ').lower()

        while len(letter) != 1 or not letter.isalpha() or letter in letters_guessed:
            guessed_word = get_guessed_word(secret_word, letters_guessed)

            if(letter == "*" and is_with_hints):
                show_possible_matches(guessed_word)
                letter = input('Please guess a letter: ').lower()
                continue
            warnings -= 1

            if warnings != 0:
                if letter in letters_guessed:
                    print(f'Oops! You\'ve already guessed that letter. You have {warnings} warnings left: {guessed_word}')
                else:
                    print(f'Oops! That is not a valid letter. You have {warnings} warnings left: {guessed_word}')
            else:
                guesses_remaining -= 1
                print(f'You have no warnings left so you lose one guess. {guesses_remaining} guesses left: {guessed_word}')

                if guesses_remaining <= 0:
                    print('-' * 10)
                    break

            letter = input('Please guess a letter: ').lower()

        letters_guessed.append(letter)

        if letter in secret_word:
            print('Good guess: {}'.format(get_guessed_word(secret_word, letters_guessed)))
        else:
            guesses_remaining -= 2 if letter in vowels else 1
            print('Oops! That letter is not in my word: {}'.format(get_guessed_word(secret_word, letters_guessed)))
        print('-' * 10)

    if guesses_remaining > 0:
        score = guesses_remaining * len(set(secret_word))
        print('Congratulations, you won!\nYour total score for this game is: {}'.format(score))
    else:
        print('Sorry, you ran out of guesses. The word was {}'.format(secret_word))



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    secret_word = choose_word(wordlist)
    hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    #secret_word = choose_word(wordlist)
    #hangman_with_hints(secret_word)
