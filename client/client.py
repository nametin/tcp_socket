import socket

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = "127.0.0.1"
    PORT = 12345
    s.connect((HOST, PORT))
    try:
        while True:
            server_message = s.recv(1024).decode()
            print(server_message)

            if (
                "Game over." in server_message
                or "Correct!" in server_message
            ):
                return
            guess = input("Your guess: ")
            
            if guess == "END":
                s.sendall(guess.encode())
                break
            s.sendall(guess.encode())
    finally:
        s.close()

if __name__ == "__main__":
    main()

