import csv

# Numele fișierului pe care îl generăm
for i in range(1, 11):
    filename = f"file_{i}.csv"
    data = [
        ["id", "name", "price"],
        [i, f"item_{i}", round(0.1 * i, 2)]
    ]
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    print(f"{filename} generated successfully!")