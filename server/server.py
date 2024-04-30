import pandas as pd
import socket
import random

def load_plate_codes(file_path):
    df = pd.read_excel(file_path)
    plate_codes = dict(zip(df["CityName"], df["PlateNumber"].astype(str)))
    return plate_codes

def main():
    connection = 1
    plate_codes = load_plate_codes("plate_list.xlsx")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 12345))
        s.listen()
        print(f"Waiting for {connection}th client connection")
        print("Server waiting for connection...")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Client connected from: {addr}")
                connection+=1

                selected_city, selected_plate = random.choice(list(plate_codes.items()))
                conn.sendall(f"What is the plate code of {selected_city.strip()}".encode())
                new_con = True
                try:
                    while True:
                        guess = conn.recv(1024).decode()
                        if guess == "END":
                            new_con = False
                            return
                        try:
                            if not (1 <= int(guess) <= 81):
                                print(f"Received from client: {guess.strip()}")
                                conn.sendall(
                                    "Number exceeds the range. Game over.\n".encode()
                                )
                                break
                        except:
                            pass
                        
                        if not guess.isdigit():
                            print(f"Received from client: {guess.strip()}")
                            conn.sendall(
                                "You entered a non-numeric value. Game over.\n".encode()
                            )
                            break

                        elif guess == selected_plate:
                            print(f"Received from client: {guess.strip()}")
                            conn.sendall("Correct!\n".encode())
                            break
                        else:
                            print(f"Received from client: {guess.strip()}")
                            city_for_guess = next(
                                (
                                    city
                                    for city, plate in plate_codes.items()
                                    if plate == guess
                                ),
                                None,
                            )
                            if city_for_guess:
                                message = f"You have entered the plate code of {city_for_guess.strip()}"
                                conn.sendall(message.encode())

                finally:
                    conn.close()

                    if new_con :
                        print(f"Waiting for {connection}th client connection")
                        print("Server waiting for connection...")

if __name__ == "__main__":
    main()
