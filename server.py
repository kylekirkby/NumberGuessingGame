""" This is the NumberGuessingGame class for running a multi-threaded server allowing multiple players to connect and
guess a random Number between 1 and 30 on port 4000. An admin can connect to the server and view the current players
connected by issuing the Who command on port 4001. """

# Import the required modules for the server.
from socket import *
import select
from threading import Thread
import random


class NumberGuessingGame:

    """ The NumberGuessingGame class which creates the server for the random number guessing game."""

    def __init__(self):

        # Required attributes of the server
        self.host = "127.0.0.1"
        self.clientPort = 4000
        self.adminPort = 4001

        # Packet size of transmissions (bytes)
        self.pack_size = 1024
        # Store the current client connections in a list as an attribute of the server class.
        self.server_connections = []

        # Create a tuple of the host and client port for both player and admin sockets.
        self.address = (self.host, self.clientPort)
        self.admin_address = (self.host, self.adminPort)

        # Create the player server socket.
        self.server_sock = socket(AF_INET, SOCK_STREAM)

        # Create the admin server socket.
        self.admin_sock = socket(AF_INET, SOCK_STREAM)

        # Bind the address tuples to the newly created sockets.
        self.server_sock.bind(self.address)
        self.admin_sock.bind(self.admin_address)

        # Start listening on both sockets.
        self.server_sock.listen()
        self.admin_sock.listen()

        # Set the inputs list of the sockets to monitor using the select module.
        inputs = [self.server_sock, self.admin_sock]

        # Create the running variable for the while loop and set it to True.
        running = True

        # Start a while loop which will loop as long as the server is running.
        while running:

            # Parse the inputs to the select.select() function and get the sockets that are ready for input.
            input_ready, output_ready, except_ready = select.select(inputs, [], [])

            # Start a for loop which looks through the sockets in the input_ready list.
            for s in input_ready:

                # Check if the element is a player socket.
                if s == self.server_sock:

                    # Receive a player connection using .accept() on the player socket.
                    (client_sock, (ip, port)) = self.server_sock.accept()

                    # Add the data to the current connections list.
                    self.server_connections.append([client_sock, [ip, port]])

                    # Create a new Instance of the ConnectionThread class for the player connected.
                    # Parse the thread the client_sock.
                    new_thread = ConnectionThread(self, client_sock)

                    # Start the new thread.
                    new_thread.start()

                # Check if the element is a admin socket.
                elif s == self.admin_sock:

                    # Receive an admin connection using .accept() on the admin socket.
                    (admin_sock, (ip, port)) = self.admin_sock.accept()

                    # Create a new AdminThread Instance and parse the admin_sock.
                    new_thread = AdminThread(self, admin_sock)

                    # Start the new thread.
                    new_thread.start()

    def __del__(self):
        # Close the socket connections upon exit.
        self.server_sock.close()
        self.admin_sock.close()


class AdminThread(Thread):

    """ The AdminThread class inherits the Thread class from the threading module and overrides the run method.
    to support the servers interaction with the admin client. """

    def __init__(self, server, admin_sock):

        # Run the super-constructor of the parent class.
        Thread.__init__(self)

        # Set the admin sock and server as class attributes.
        self.admin_sock = admin_sock
        self.server = server

        # Assign the hello_response attribute.
        self.hello_response = "Admin-Greetings\r\n"

    # Define the run method for this thread.
    def run(self):

        # Using the protocol defined in specification receive the Hello\r\n message from the admin client.
        admin_client_hello_msg = self.admin_sock.recv(self.server.pack_size).decode()

        # If the admin_client_hello_msg is correct then continue.
        if admin_client_hello_msg == "Hello\r\n":

            # Send the admin the hello_response after encoding.
            self.admin_sock.send(self.hello_response.encode())

            # Receive the Who\r\n message as defined in protocol by using the admin socket.
            admin_client_who_msg = self.admin_sock.recv(self.server.pack_size).decode()

            # Check the who message is correct and continue.
            if admin_client_who_msg == "Who\r\n":

                # Iterate through the server_connections list accessed through the server instance.
                for client in self.server.server_connections:

                    # Format the data to send to the admin of the ip and port.
                    client_line = str(client[1][0]) + " " + str(client[1][1]) + "\r\n"

                    # Send the formatted line to the admin client after encoding it.
                    self.admin_sock.send(client_line.encode())

        # After all is done cleanup and close the connection to the admin client.
        self.admin_sock.close()


class ConnectionThread(Thread):

    """ The ConnectionThread class inherits the Thread class from the threading module and overrides the run method.
    to support the servers interaction with the player clients. """

    def __init__(self, server, client_sock):

        # Run the super-constructor of the parent class.
        Thread.__init__(self)

        # Set the client sock and server as class attributes.
        self.client_sock = client_sock
        self.server = server

        # Connection thread textual responses.
        self.greetings_response = "Greetings\r\n"
        self.ready_response = "Ready\r\n"
        self.close_response = "Close\r\n"
        self.far_response = "Far\r\n"
        self.correct_response = "Correct\r\n"

        # For each instance of the Connection thread a new unique random number between 1 and 30 is stored.
        self.random_number = random.randint(1, 30)

    # Define the run method for this thread.
    def run(self):

        # Store the players hello message.
        client_hello_msg = self.client_sock.recv(self.server.pack_size).decode()

        # Check the hello message is correct.
        if client_hello_msg == "Hello\r\n":

            # If correct then send the player the greetings response.
            self.client_sock.send(self.greetings_response.encode())

            # Store the players game message.
            client_game_msg = self.client_sock.recv(self.server.pack_size).decode()

            # Check the game message is correct.
            if client_game_msg == "Game\r\n":

                # Send the player the ready response.
                self.client_sock.send(self.ready_response.encode())

                # Create the guessing boolean.
                guessing = True

                # Start a while loop for the length of time the player is guessing (while guessing boolean is True).
                while guessing:

                    # Receive the players guess.
                    client_guess = self.client_sock.recv(self.server.pack_size).decode()

                    # Split the player guess at ": " using the format of "My Guess is: 3" as defined in protocol.
                    guess_list = client_guess.split(": ")

                    # Convert the number string to an integer and store as guess_int.
                    guess_int = int(guess_list[1])

                    # Subtract the guess_int from the random_number generated and check if the absolute value is < 5.
                    # Also check that the guess_int is not the random number.
                    if abs(self.random_number - guess_int) < 5 and guess_int != self.random_number:
                        self.client_sock.send(self.close_response.encode())

                    # If the guess int is exactly equal to the random number then continue.
                    elif guess_int == self.random_number:

                        # Send the correct response to the client.
                        self.client_sock.send(self.correct_response.encode())

                        # Set the guessing boolean to False so the while loop can stop and the game can finish.
                        guessing = False

                    # If the guess int is neither within 5 or correct send the far response.
                    else:
                        self.client_sock.send(self.far_response.encode())

            # Once the game is finished loop through the server connections and remove the player from the list.
            for each in self.server.server_connections:
                if each[0] == self.client_sock:
                    self.server.server_connections.remove(each)

        # Close the player connection to the server.
        self.client_sock.close()

if __name__ == "__main__":
    game = NumberGuessingGame()
