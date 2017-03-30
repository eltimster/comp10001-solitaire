"""

Synopsis: simple ASCII-based Solitaire game

Author: Tim Baldwin

Created: 4/4/2014

Modified: 27/4/2016

- updated to Python3
"""


from classes import *

g = Game()  

# show Foundation stacks?
display_foundations = False  

# show Trash deck?
display_deck = False  

# show starting Tableaux
g.display(display_deck=display_deck)

# iterate over single turns until the game is solved
while not g.solved():

    # get user input
    turn = input("""\nRETURN = Draw from Trash, 'M' = move card from stack M to Foundation, 'MN' = move card from stack M to Tableau N, 's' = show all: """)

    # draw from Trash
    if turn == '':
        g.deck.nextCard()
        display_deck = True

    # show all cards
    elif turn == 's':
        print("Naughty, naughty!")
        g.display(display_foundations, display_deck, show_all=True)
        continue

    # move card from stack M to the appropriate Foundation stack
    elif len(turn) == 1 and '0' <= turn <= str(Game.TABLEAUX):

        # Stack number M
        stack_no = int(turn) 

        # M is Trash
        if stack_no == Game.TABLEAUX:
            deck = g.deck

        # M is a Tableau
        else:
            deck = g.tableau[stack_no]

        # Get "movable" card
        card = deck.showBottomCard()

        # Move card only if it is a valid move
        if card and g.foundation[card.getSuit()].isValidAdd(card):
            deck.removeCard()
            g.foundation[card.getSuit()].addCard(card)
            display_foundations = True

    # move card from stack M to Tableau N
    elif len(turn) == 2 and '0' <= turn[0] <= str(Game.TABLEAUX) and '0' <= turn[1] < str(Game.TABLEAUX):
        source = int(turn[0]) # (source) stack number M
        dest = int(turn[1]) # (destination) Tableau N
        
        # M is Trash
        if source == Game.TABLEAUX:
            source_deck = g.deck

        # M is a Tableau
        else:
            source_deck = g.tableau[source]

        source_card,stacked_cards = source_deck.showTopCards()

        # move card only if it is a valid move
        if source_card and g.tableau[dest].isValidAdd(source_card):
            source_deck.removeCards(len(stacked_cards) + 1)
            g.tableau[dest].addCards([source_card] + stacked_cards)
    
    # unrecognised input
    else:
        print("Invalid input; try again")

    # display game state
    g.display(display_foundations, display_deck)

print("Solved it ... go you!")
