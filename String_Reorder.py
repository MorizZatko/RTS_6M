"""String Reordering.

This tool reorders a user string input through string manipulation,
by swapping first and last element and adding the total length to the end.
Input and output via standard terminal
"""
# User input
word = input("Zu verschlüsselndes Wort:") 

# LOGIC BLOCK
start = word[0]     
last = word[-1]     
mid = word[1:-1]    
length = len(word) 

# Generates new reordered string
new_word = last + mid + start + str(length)

# Output new string
print(f"{new_word}")