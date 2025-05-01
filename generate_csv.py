import csv

# Numele fișierului pe care îl generăm
filename = "test_data.csv"

# Date de test - o listă de itemi
data = [
    ["id", "name", "price"],
    [1, "apple", 0.5],
    [2, "banana", 0.3],
    [3, "cherry", 0.2],
    [4, "date", 0.7],
    [5, "elderberry", 1.5]
]

# Scriem fișierul CSV
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print(f"{filename} generated successfully!")