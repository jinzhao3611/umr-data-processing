# List of names
names = [
    "Julia Bonn",
    "Andrew Cowell",
    "Ching-wen Chen",
    "Haibo Sun",
    "Nianwen Xue",
    "Jin Zhao",
    "Kenneth Lai",
    "James Pustejovsky",
    "Jens E. VanGysel",
    "Meagan Vigus",
    "Rosa Vallejos",
    "Lukas Denk",
    "William Croft",
    "Martha Palmer",
    "Alexis Palmer",
    "Jan Hajič"
]


# Sort and print names
sorted_names = sorted(names, key=lambda name: name.split()[-1])
for name in sorted_names:
    print(name)
