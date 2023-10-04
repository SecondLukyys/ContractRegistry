# Skaičių seka
A = [1, 4, 5, 6, 7, 8, 10]
B = [2, 6, 7, 9, 11, 14, 0, 16, 17]

# Sąrašas skirtas išsaugoti
results = []

# Dalybos veiksmas ir rezultatų išsaugojimas
for num_a in A:
    for num_b in B:
        if num_b != 0:  # Siekiama vengti dalybos iš nulio
            result = num_a / num_b
            results.append(result)

# Rezultatų atspauzdinimas
print("Skaičių A iš skaičių B dalybos rezultatai:")
for result in results:
    print(result)

