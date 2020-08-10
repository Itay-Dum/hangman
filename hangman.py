def is_valid_input(letter_guessed, old_letters_guessed):
    """checks if the the user input is valid"""
    return letter_guessed.isalpha() and len(letter_guessed) == 1 and letter_guessed not in old_letters_guessed


def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """trys to append the letter guessed by the user to the old letter guessed list"""
    if is_valid_input(letter_guessed, old_letters_guessed) and letter_guessed not in old_letters_guessed:
        old_letters_guessed.append(letter_guessed)
        return True
    else:
        return False


def show_hidden_word(secret_word, old_letters_guessed, letter_guessed):
    """updates the amount of underlines(_) printed to the user acording to what he guessed """
    length_of_secret_word = len(secret_word)
    underlines = length_of_secret_word * '_ '
    underlines_list = []
    secret_word_list = []
    for k in underlines:
        if k == "_":
            underlines_list.append(k)
    secret_word_list = list(secret_word)
    for letter in old_letters_guessed:
        if letter in secret_word:
            indexes_in_secret_word = [i for i, x in enumerate(secret_word_list) if x == letter]
            for index in indexes_in_secret_word:
                underlines_list[index] = letter
                underlines = "".join(underlines_list)
    print("")
    for k in underlines:
        print(k, "", end="", flush=True)
    if underlines.count("_") == 1 and letter_guessed in secret_word and letter_guessed not in old_letters_guessed \
            and letter_guessed != "":
        b = True
    else:
        b = False
    underlines_count = underlines.count("_")
    return b, underlines_count


def print_hangman(num_of_tries):
    """keeps a dictionary of all the hangman positions and prints them as num of tries grows"""
    HANGMAN_PHOTOS = {
        "1": '''x-------x''',
        "2": '''
    x-------x
    |
    |
    |
    |
    |''',
        "3": '''
    x-------x
    |       |
    |       0
    |
    |
    |''',
        "4": '''
    x-------x
    |       |
    |       0
    |       |
    |
    |''',
        "5": r'''
    x-------x
    |       |
    |       0
    |      /|\
    |
    |''',
        "6": r'''
    x-------x
    |       |
    |       0
    |      /|\
    |      /
    |''',
        "7": r'''
    x-------x
    |       |
    |       0
    |      /|\
    |      / \
    |'''

    }

    print(HANGMAN_PHOTOS[str(num_of_tries)])


def choose_word(file_path, index):
    """returns the the word in the place of index within the file path the user entered"""
    counter_of_different_words = 0
    counter_of_all_words = 0
    with open(file_path, "r") as input_file:
        input_file_data = input_file.read()
        input_file_data_list = input_file_data.split(" ")
        for k in input_file_data_list:
            counter_of_all_words += 1
        dictionary_count_of_each_word = {i: input_file_data_list.count(i) for i in input_file_data_list}
        for values_of_dictionary in dictionary_count_of_each_word.values():
            if values_of_dictionary == 1:
                counter_of_different_words += 1
        if index > counter_of_all_words:
            temp = index // counter_of_all_words
            index = index - temp * counter_of_all_words
        returned_tuple = (counter_of_different_words, input_file_data_list[index - 1])
        return returned_tuple


def check_win(secret_word, old_letters_guessed, letter_guessed):
    import sys, os

    def blockPrint():
        sys.stdout = open(os.devnull, 'w')

    def enablePrint():
        sys.stdout = sys.__stdout__

    blockPrint()
    j = show_hidden_word(secret_word, old_letters_guessed, letter_guessed)[1]
    enablePrint()
    return j


def welcome():
    """prints the hangman welcome screen"""
    print('''  _    _                                         
 | |  | |                                        
 | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
 |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
 | |  | | (_| | | | | (_| | | | | | | (_| | | | |
 |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                      __/ |                      
                    |___/''')


def main():
    """The main function combines all of the other functions int he program to create the actual game"""
    import sys, os
    welcome()
    input_file = input("Enter file path:\n")
    index = int(input("Enter index:\n"))
    print("\nLet's start")
    num_of_tries = 1
    old_letters_guessed = []
    secret_word = choose_word(input_file, index)[1]
    letter_guessed = '0'
    player_won = False
    print_hangman(1)
    show_hidden_word(secret_word, old_letters_guessed, letter_guessed)
    while not player_won and num_of_tries < 7:
        letter_guessed = input("\nGuess a letter:\n").lower()
        if is_valid_input(letter_guessed, old_letters_guessed):
            if letter_guessed in secret_word:
                try_update_letter_guessed(letter_guessed, old_letters_guessed)
                show_hidden_word(secret_word, old_letters_guessed, letter_guessed)
                if check_win(secret_word, old_letters_guessed, letter_guessed) == 0:
                    player_won = True
                    break
            else:
                num_of_tries += 1
                try_update_letter_guessed(letter_guessed, old_letters_guessed)
                print_hangman(num_of_tries)
                show_hidden_word(secret_word, old_letters_guessed, letter_guessed)
        else:
            print("\nX\n")
            print(" -> ".join(map(str, old_letters_guessed)))

    if num_of_tries >= 6:
        print("\nLOSE")
    else:
        print("\nWIN")


main()
