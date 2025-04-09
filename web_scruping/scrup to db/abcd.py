import random
from datetime import datetime, timedelta


def generate_measurement_time(start_time, i, delta_minutes=2):
    # Generuje czas pomiaru: start_time + i*delta_minutes
    return (start_time + timedelta(minutes=i * delta_minutes)).strftime("%H:%M")


def format_number(value, decimals=2):
    # Formatuje liczbę z określoną liczbą miejsc po przecinku,
    # zamieniając kropkę na przecinek
    return format(value, f".{decimals}f").replace('.', ',')


def main():
    # Lista ilości wierszy: najpierw 1000, 5000, 10000, a potem od 25000 do 750000 co 25000
    row_counts = [100, 500, 1000]
    start_time = datetime.strptime("10:00", "%H:%M")

    for num_rows in row_counts:
        filename = f"{num_rows}.csv"  # Nazwa pliku: np. "1000.csv", "5000.csv", etc.
        with open(filename, "w", encoding="utf-8") as f:
            # Zapisujemy nagłówek (kończący się średnikiem)
            f.write("# godzina pomiaru; ciśnienie [hPa];  temperatura [stopnie C]; wilgotność [%];\n")

            for i in range(num_rows):
                time_str = generate_measurement_time(start_time, i)
                # Losujemy wartości dla pomiarów
                pressure = random.uniform(900.0, 1100.0)
                temperature = random.uniform(-30.0, 50.0)
                humidity = random.uniform(10.0, 100.0)

                # Formatujemy wartości pomiarowe
                pressure_str = format_number(pressure, 2)
                temperature_str = format_number(temperature, 1)
                humidity_str = format_number(humidity, 0)

                # Łączymy dane w jeden wiersz oddzielony średnikami, zakończony średnikiem
                line = f"{time_str}; {pressure_str}; {temperature_str}; {humidity_str};\n"
                f.write(line)

        print(f"Plik {filename} został utworzony z {num_rows} wierszami.")


if __name__ == "__main__":
    main()
