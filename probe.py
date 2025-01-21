# text = "суп-1-45\nкаша-2-35\nморковь-5-5"
# parts = text.split('\n')
# dictionaries = []
# for part in parts:
#     dictionaries.append(part.split('-'))
# print(dictionaries)


# price = 0
# original_list = ['суп', '1', '45\r']
# for i in original_list:
#     cleaned_list = original_list[i].replace('\r', '')
#     print(cleaned_list)
#     # price += int(cleaned_list)

#
# original_list = ['суп', '1', '45\r']
# cleaned_list = [item.encode().decode('utf-8').replace('\r', '') for item in original_list]
# print(cleaned_list)


original_list = ['суп', '1', '45\r']
cleaned_list = [item.replace('\r', '') for item in original_list]
print(cleaned_list)
