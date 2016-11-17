""" This is the player class for the NumberGuessingGame server class."""

import socket


class Player:

    """ The Player Class takes the ip address of the NumberGuessingGame server and the port 4000. """

    def __init__(self, address, port):

        # Assign the address and port of the server to class attributes.
        self.server_address = address
        self.server_port = port

        # Create the tuple to be used in the socket.connect.
        self.address = (self.server_address, self.server_port)

        # Store the pack size to use when sending and receiving data.
        self.pack_size = 1024

        # Store the strings sent by the player client to the server.
        self.hello_message = "Hello\r\n"
        self.game_message = "Game\r\n"
        self.guess_string = "My Guess is: "

        # Create a socket instance.
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the address provided.
        self.sock.connect(self.address)

        # Send the Hello\r\n message to the server to initiate communication.
        self.sock.send(self.hello_message.encode())

        # Store the greetings response sent back by the server.
        self.greetings_response = self.sock.recv(self.pack_size).decode("UTF-8")

        # Check if the greetings response is correct.
        if self.greetings_response == "Greetings\r\n":

            # Send the server the game message encoded.
            self.sock.send(self.game_message.encode())

            # Store the ready response from the server.
            self.ready_response = self.sock.recv(self.pack_size).decode()

            # Check the ready response is correct.
            if self.ready_response == "Ready\r\n":

                # Start the game method.
                self.game()

    # Game method starts the number guessing game client side.
    def game(self):

        # Print the welcome message.
        print("Welcome to the guess the number game!")

        # Set end boolean for the game loop to False.
        end = False

        # Start the game loop.
        while end is False:

            # Using a try/except to catch any ValueErrors client side for the number input.
            try:

                # Store the user input as an integer. If a string is entered here a ValueError will raise.
                user_input = int(input('What is your guess? '))

                # Create the new guess string to be sent to the server after converting the int to str for sending.
                new_guess_string = self.guess_string + str(user_input) + "\r\n"

                # Send the new guess string after encoding.
                self.sock.send(new_guess_string.encode())

                # Store the guess response of the server.
                guess_response = self.sock.recv(self.pack_size).decode()

                # Check if the guess was correct.
                if guess_response == "Correct\r\n":

                        # Notify the player they guessed correctly.
                        print("You guessed Correctly!\r\n")

                        # End the game by assigning the end boolean to True.
                        end = True

                # Check if the guess was close.
                elif guess_response == "Close\r\n":

                        # Notify the player that they were close.
                        print("You are close!")

                # Check if the guess was far.
                elif guess_response == "Far\r\n":

                        # Notify the player that they were far.
                        print("You are way off.")

            # Catch the ValueErrors raised if the player enters a string instead of a number.
            except ValueError:

                # Tell the player a ValueError occurred.
                print("The number you entered was not valid. Please enter a positive integer between 1 and 30!")


if __name__ == "__main__":

    # Create new instance of the player client.
    player_client = Player("127.0.0.1", 4000)
