import random

pp = 0  
bp = 0 

print("Welcome to Rock, Paper, Scissors! Enter 'r' for Rock, 'p' for Paper, 's' for Scissors.")

ch = ["r", "p", "s"]

while pp < 5 and bp < 5:
    uc = input("Your choice (r/p/s): ").lower() 
    if uc not in ch:
        print("Invalid choice! Try again.")
        continue

    bc = random.choice(ch) 
    print(f"Bot chose: {bc}")

    if uc == bc:
        print("It's a draw!")
    elif (uc == "r" and bc == "s") or (uc == "p" and bc == "r") or (uc == "s" and bc == "p"):
        print("You won this round!")
        pp += 1
    else:
        print("Bot won this round!")
        bp += 1

    print(f"Your points: {pp}, Bot's points: {bp}")

if pp == 5:
    print("Congratulations! You reached 5 points and won the game!")
elif bp == 5:
    print("Game over! The bot reached 5 points. You lost.")
