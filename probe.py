text = "суп-1-45\nкаша-2-35\nморковь-5-5"
parts = text.split('\n')
dictionaries = []
for part in parts:
    dictionaries.append(part.split('-'))
print(dictionaries)




