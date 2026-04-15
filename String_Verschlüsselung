"""
Module: String Reordering
Description: This tool reorders the user input through string manipulation.
Function: 
    1. Asks user for a string to reorder.
    2. Splits the string in three parts (start, last, mid) and extracts the total length of the input.
    3. All three strings are added together in a reverse order with the length as a integer at the end.

Args:
    None: Source string is provided by user via standard input
Returns:
    None: Tool outputs the reordered string via standard output
"""

word = input("Zu verschlüsselndes Wort:") 

start = word[0]     
last = word[-1]     
mid = word[1:-1]    
length = len(word) 

# --- Output ---
new_word = last + mid + start + str(length)

print(f"{new_word}")