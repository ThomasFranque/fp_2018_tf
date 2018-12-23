import sys
import time

print("\n\nWell look who is back...")
time.sleep(1)
print('After you fell on the pit you passed out. Yet, you are still falling.')
time.sleep(2)
print('Thought you were dead actually.')
time.sleep(2)
difficulty = str(input('So, how are you feeling?\n>[bad (Easy)] [well (Normal)] [good (Hard)]\n'))

while True:
    if difficulty == 'good': #Easy
        print('Oh, then you must be ready for a challange!\n')
        break
    elif difficulty == 'bad': #Hard
        print('Oh, poor you... Maybe the gods will smile upon you.\n')
        break
    elif difficulty == 'well': #Normal
        print('Oh, nice!\n')
        break
    
    dificulty = str(input('\nSorry did not understand...\nSo, how are you feeling?\n>[good] [bad] [well]\n'))

print('Hm... Intresting, I have somet-- WHAT?!')
time.sleep(1)
print('YOUR EYES, YOU CAN SEE AGAIN! Too bad you are doomed...')
time.sleep(3)
