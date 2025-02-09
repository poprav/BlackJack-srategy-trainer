# BlackJack Basic Strategy Trainer

# Test your knowlige of Perfect BlackJack strategy

# Written by OzzieOnBass, with help of ChatGPT. (Heresy i know) 
# Last edited 02/09/2025

'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import thumby
import random
import time

thumby.display.setFPS(60)

def generate_card():
    """Generate a card with a rank (1-13) and suit (1-4)"""
    card_num = random.randint(1, 52)
    rank = (card_num - 1) % 13 + 1  # Convert 1-52 to 1-13
    suit = (card_num - 1) // 13 + 1  # Convert 1-52 to 1-4
    return (rank, suit)

def generate_hand():
    """Generate a player hand and a dealer upcard"""
    return [generate_card(), generate_card()], generate_card()

def get_hand_total(hand):
    """Calculate the total of a hand, treating Aces (1) properly"""
    total = sum(min(card[0], 10) for card in hand)
    if any(card[0] == 1 for card in hand) and total + 10 <= 21:
        total += 10  # Count Ace as 11 if it doesn't bust
        return 'S' + str(total)
    return 'H' + str(total)

def calculate_outcome(player_hand, dealer_card):
    Hard = [
        # A ,  2 ,  3 ,  4 ,  5 ,  6 ,  7 ,  8 ,  9 ,  10
        ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  #8
        ['H', 'H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H'],  #9
        ['H', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H'],  #10
        ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D'],  #11
        ['H', 'H', 'H', 'S', 'S', 'S', 'H', 'H', 'H', 'H'],  #12
        ['H', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H'],  #13
        ['H', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H'],  #14
        ['H', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H'],  #15
        ['H', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H'],  #16
        ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],  #17
    ]
    Soft = [
        # A ,  2 ,  3 ,  4 ,  5 ,  6 ,  7 ,  8 ,  9 ,  10
        ['H', 'H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H'],  #A,2 13
        ['H', 'H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H'],  #A,3 14
        ['H', 'H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H'],  #A,4 15
        ['H', 'H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H'],  #A,5 16
        ['H', 'H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H'],  #A,6 17
        ['H', 'D', 'D', 'D', 'D', 'D', 'S', 'S', 'H', 'H'],  #A,7 18
        ['S', 'S', 'S', 'S', 'S', 'D', 'S', 'S', 'S', 'S'],  #A,8 19
        ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],  #A,9 20
    ]
    Split = [
        # A ,  2 ,  3 ,  4 ,  5 ,  6 ,  7 ,  8 ,  9 ,  10
        ['Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y'],  #1
        ['N', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'N', 'N', 'N'],  #2
        ['N', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'N', 'N', 'N'],  #3
        ['N', 'N', 'N', 'N', 'Y', 'Y', 'N', 'N', 'N', 'N'],  #4
        ['N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N'],  #5
        ['N', 'Y', 'Y', 'Y', 'Y', 'Y', 'N', 'N', 'N', 'N'],  #6
        ['N', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'N', 'N', 'N'],  #7
        ['Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y'],  #8
        ['N', 'Y', 'Y', 'Y', 'Y', 'Y', 'N', 'Y', 'Y', 'N'],  #9
        ['N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N'],  #10
    ]
    
    if min(player_hand[0][0], 10) == min(player_hand[1][0], 10):
        split_possible = 1
    else: split_possible = 0
    
    if dealer_card[0] > 10:
        dealer_int = 10
    else:
        dealer_int = int(dealer_card[0])
    
    player_eval = get_hand_total(player_hand)
    player_int = int(player_eval[1:]) 
    
    print("Eval:", player_eval ,"into", dealer_int)
    if split_possible == 1:
        print("Split?")
    
    if (split_possible == 1) & (Split[min(player_hand[0][0], 10)-1][dealer_int - 1] == 'Y'):
        print("Expected :", Split[min(player_hand[0][0], 10)-1][dealer_int - 1])
        return Split[min(player_hand[0][0], 10)-1][dealer_int - 1]
    elif split_possible == 1:
        print("Split: No")
    
    if player_eval[0] == 'H':
        if player_int > 17:
            player_int = 17
        elif player_int < 8:
            player_int = 8
        print("Expected :", Hard[player_int - 8][dealer_int - 1])
        return Hard[player_int - 8][dealer_int - 1]
    
    if player_eval[0] == 'S':
        if player_int > 20:
            player_int = 20
        elif player_int < 13:
            player_int = 13
        print("Expected :", Soft[player_int - 13][dealer_int - 1])
        return Soft[player_int - 13][dealer_int - 1]
    
    return 'E'

def draw_screen(player_hand, dealer_card):
    """Draw the game screen"""
    thumby.display.fill(0)  # Clear screen
    thumby.display.drawText(f"{convert_card(player_hand[0])}", 5, 15, 1)
    thumby.display.drawText(f"{convert_card(player_hand[1])}", 25, 15, 1)
    thumby.display.drawText(f"{convert_card(dealer_card)}", 5, 5, 1)
    thumby.display.drawText(f"<H >S ^D vS", 5, 25, 1)
    thumby.display.update()

def convert_card(card):
    """Convert card into readable format"""
    if card[0] == 1:
        rank = 'A'
    elif card[0] == 11:
        rank = 'J'
    elif card[0] == 12:
        rank = 'Q'
    elif card[0] == 13:
        rank = 'K'
    else:
        rank = str(card[0])
    
    if card[1] == 1:
        return rank + 'H'
    elif card[1] == 2:
        return rank + 'C'
    elif card[1] == 3:
        return rank + 'D'
    elif card[1] == 4:
        return rank + 'S'
    else:
        return rank + 'ERR'
        

def main():
    #Debug option. Comment generate_hand() calls and inject any case.
    #player_hand = [(4, 2), (1, 3)]
    #dealer_card = (9, 3)
    
    player_hand, dealer_card = generate_hand()
    print("Pulled:" + str(player_hand) + str(dealer_card))
    
    waiting_for_input = True
    
    while True:
        draw_screen(player_hand, dealer_card)
        
        if waiting_for_input:
            if thumby.buttonL.justPressed():
                action = "H" #Hit
                waiting_for_input = False
            elif thumby.buttonR.justPressed():
                action = "S" #Stand
                waiting_for_input = False
            elif thumby.buttonU.justPressed():
                action = "D" #Double
                waiting_for_input = False
            elif thumby.buttonD.justPressed():
                action = "Y" #Split
                waiting_for_input = False
        else:
            outcome = (action == calculate_outcome(player_hand, dealer_card))
            print("Player chose:", action, "and it is", outcome)
            thumby.display.drawText(f"{outcome}", 30, 5, 1)
            thumby.display.update()
            time.sleep(1)  # Show result for a moment
            player_hand, dealer_card = generate_hand()
            print("Pulled:" + str(player_hand) + str(dealer_card))
            waiting_for_input = True

main()
