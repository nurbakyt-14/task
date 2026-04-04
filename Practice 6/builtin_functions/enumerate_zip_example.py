names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]

for idx, name in enumerate(names, start=1):
    print(f"{idx}: {name}")

for name, age in zip(names, ages):
    print(f"{name} is {age} years old")