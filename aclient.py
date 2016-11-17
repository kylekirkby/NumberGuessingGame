"""This is the Admin() client class for a simple number guessing game project"""
import socket


class Admin:

    """ This is the Admin class which takes the address(ip) and port(4001) of the NumberGuessingGame server
     and parameters."""

    def __init__(self, address, port):

        # Store the server address and port as class attributes.
        self.server_address = address
        self.server_port = port

        # Store the tuple of the server address to be used with the socket.
        self.address = (self.server_address, self.server_port)

        # Store the strings sent to the NumberGuessingGame.
        self.hello_message = "Hello\r\n"
        self.who_message = "Who\r\n"

        # Store the pack size used in transmission of data.
        self.pack_size = 1024

        # Create a new socket instance.
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Parse the server address to the socket and connect.
        self.sock.connect(self.address)

        # Send the Hello message to the server to initiate communication.
        self.sock.send(self.hello_message.encode())

        # Get the greetings response
        self.greetings_response = self.sock.recv(self.pack_size).decode("UTF-8")

        # Check if the greetings response is correct.
        if self.greetings_response == "Admin-Greetings\r\n":

            # Send the who message.
            self.sock.send(self.who_message.encode())

            print("The players currently playing are: ")

            # Set the boolean receiving to true.
            receiving = True

            # Start the while loop for receiving data.
            while receiving:

                # Receive line by line the clients connected to the server.
                data = self.sock.recv(self.pack_size)

                # If the len of the data is not 0 then print the data.
                if len(data) != 0:

                    print(data.decode())
                else:
                    # Exit from the loop by setting the receiving boolean to False.
                    receiving = False


if __name__ == "__main__":
    admin_client = Admin("127.0.0.1", 4001)
