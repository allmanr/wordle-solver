from pathlib import Path

WORD_LIST_PATH = Path("word_list.txt")


class WordleSolver:

    def __init__(self):
        # Master word list containing all five-letter words
        self.word_list = list()
        # List of possible remaining words
        self.my_words = list()

        # Dictionary with letters for keys and positions for values (idx 0-4)
        self.word_dict = dict()

        self.turn_number = 1

        # Load word list with default path
        self.load_word_list()
        self.my_words = self.word_list

    def load_word_list(self, list_path: Path = WORD_LIST_PATH):
        with open(list_path) as word_list:
            tmp_word_list = word_list.readlines()

        for word in tmp_word_list:
            self.word_list.append(word.strip())

    def gray_letters(self, str_gray_letters: str):
        """
        :param str_gray_letters: a string containing all letters shown as gray
        :return: sets self.my_words to a subset containing words that did not have the input letters
        """
        for letter in str_gray_letters:
            new_word_list = list()
            for word in self.my_words:
                if letter not in word:
                    new_word_list.append(word)
                # Be sure to also add words that have the gray letter in the already found
                # green position but nowhere else
                elif letter in self.word_dict and word.count(letter) == 1:
                    new_word_list.append(word)

            # Set self.my_word_list to the new subset and repeat if there are more gray letters
            self.my_words = new_word_list

    def yellow_letter(self, yellow_letter: str, pos: int):
        """
        :param yellow_letter: which letter showed up as yellow
        :param pos: which position this letter appeared as yellow (1-5)
        :return: new my_words with all remaining words that contain the letter outside the specified position
        """
        new_word_list = list()
        idx = pos - 1
        for word in self.my_words:
            if yellow_letter in word and word[idx] != yellow_letter:
                new_word_list.append(word)

        self.my_words = new_word_list

    def green_letter(self, green_letter: str, pos: int):
        """
        :param green_letter: which letter showed up as green
        :param pos: which position this letter appeared as green (1-5)
        :return: new my_words with all remaining words that contain the letter at the specified position
        """
        new_word_list = list()
        idx = pos - 1

        # Add this letter to our word_dict to keep track of what we've found
        self.word_dict[green_letter] = idx

        for word in self.my_words:
            if green_letter in word and word[idx] == green_letter:
                new_word_list.append(word)

        self.my_words = new_word_list

    def print_info(self, print_word_list=False):
        if print_word_list:
            print(self.my_words)
        print("Number of words remaining: ", len(self.my_words), "\n")

        return

    def handle_input(self):
        input_cmd = input("Enter color key, letter(s), and position: ")
        inputs = input_cmd.split(" ")
        input_color = inputs[0].upper()

        # Handle exit command
        if input_color == "EXIT":
            print("Thanks for playing / cheating\n")
            exit(0)

        # End of turn - print remaining word list and return
        if input_color == "ET" or input_color == "SHOW":
            print("\nWords remaining after turn #", self.turn_number, ":")
            self.turn_number += 1
            self.print_info(print_word_list=True)
            return

        # Get input letters
        try:
            input_letters = inputs[1]
        except IndexError:
            print("Invalid input format. Must input a letter")
            return

        # Handle gray letters
        if input_color == "X" or input_color == "B":
            self.gray_letters(input_letters)

        # For green and yellow letters, first get position and check for error cases
        else:
            try:
                position = int(inputs[2])
            except IndexError:
                print("Invalid input - must specify position")
                return
            except ValueError:
                print("Invalid input - position must be an integer")
                return

            if position < 1 or position > 5:
                print("Invalid position: must be between 1 and 5")
                return

            if len(input_letters) != 1:
                print("Error - green and yellow letters must be input one at a time")
                return

            # Handle green letter:
            if input_color == "G":
                self.green_letter(input_letters, position)

            # Handle yellow letter
            elif input_color == "Y":
                self.yellow_letter(input_letters, position)

            # Handle invalid color key
            else:
                print("Invalid color specified. Color key must be G, Y, or X")
                return

        # Print info on remaining words and return
        self.print_info()
        return


if __name__ == "__main__":
    my_ws = WordleSolver()
    while True:
        my_ws.handle_input()
