"""

Synopsis: class definitions for simple ASCII-based Solitaire game

Author: Tim Baldwin

Created: 4/4/2014

Modified: 27/4/2016

"""



from random import shuffle  # used to shuffle the pack
from itertools import zip_longest  # used to display cards





class Card():
    """Definition of a single card, with a value and suit attribute"""

    # constants associated with Card:
    VALUES = ['A'] + [str(i) for i in range(2,11)] + ['J','Q','K']   # values of card (all strings -- 'A' = ace, '1' = 1, etc.)
    SUITS = ['S','H','D','C']  # card suits
    COLOUR = {'S': 'Black', 'H': "Red" ,'D': "Red", 'C': "Black"}  # mapping from suits to colours
    __CARD_SEPARATOR = "  "  # blank separators used when printing out the cards
    __VISIBLE_CARD_EDGE = "|"
    __INVISIBLE_CARD_EDGE = ":"

    def __init__(self):
        """Initialise each card with a 'value' and 'suit', each set to the list of all possible values"""
        self.value = Card.VALUES
        self.suit = Card.SUITS

    def createCard(self, value, suit):
        """Create a single Card object, based on the supplied 'value' and 'suit'"""
        card = Card()
        card.value = value
        card.suit = suit
        return card

    def getSuit(self):
        """Return the suit of a card"""
        return self.suit

    def getSuitColour(self):
        """Return the colour of a card"""
        return Card.COLOUR[self.suit]

    def getValue(self):
        """Return the value of a card"""
        return self.value

    def isAce(self):
        """Is the card an Ace?"""
        return self.value == 'A'

    def isKing(self):
        """Is the card a King?"""
        return self.value == 'K'

    def nextValue(self):
        """Return the next value up from the value of the card"""
        return Card.VALUES[Card.VALUES.index(self.getValue())+1]

    def prevValue(self):
        """Return the previous value down from the value of the card"""
        return Card.VALUES[Card.VALUES.index(self.getValue())-1]

    def __toString(self):
        """Return the card value and suit as a string (e.g. "AH")"""
        return self.value + self.suit

    def display(self,stack_no="",extras="",sep=__CARD_SEPARATOR,visible=True):
        """Display the card in ASCII glory, with the stack no. (0-7) and the number of "extra cards" in that stack"""
        if visible:
            card_edge = self.__VISIBLE_CARD_EDGE
        else:
            card_edge = self.__INVISIBLE_CARD_EDGE
        return(["  {}  ".format(stack_no) + sep, "+---+"+sep, "{0}   {0}".format(card_edge) + sep,
                "{0}{1:>3s}{0}".format(card_edge, self.__toString()) + sep,"{0}   {0}".format(card_edge) + sep,
                "+---+"+sep,"{:^5s}".format(extras)+sep])

    def displayEmptyCard(self,stack_no='',sep=__CARD_SEPARATOR):
        """Display an empty card in ASCII glory!"""
        return(["  {}  ".format(stack_no)+sep,"+---+"+sep,
                "{0}   {0}".format(self.__INVISIBLE_CARD_EDGE)+sep,
                "{0}   {0}".format(self.__INVISIBLE_CARD_EDGE)+sep,
                "{0}   {0}".format(self.__INVISIBLE_CARD_EDGE)+sep,
                "+---+"+sep,"     "+sep])





class Stack():
    """Definition of a "stack", as an abstract super-class of Tableau, Foundation and Deck"""

    # constants associated with Stack:
    __CARD_FOOTER = -3 # amount of card to remove when printing with a card stacked on top of it
    __CARD_HEADER = 1 # size of the header, to separate stacks in the basic display

    def __init__(self):
        """Initialise the stack to an empty list of cards"""
        self.cards = []

    def addCard(self,card):
        """Add 'card' to the stack"""
        self.cards.append(card)

    def addCards(self,cards):
        """Add the list 'cards' to the stack"""
        self.cards += cards

    def removeCard(self):
        """Remove the (top) card from the stack"""
        return self.cards.pop()

    def removeCards(self,n):
        """Remove 'n' cards from the top of the stack"""
        ret_cards = []
        for i in range(n):
            ret_cards.append(self.removeCard())
        return ret_cards

    def showTopCard(self):
        """Return the "top" card from the stack, or the empty string if the stack is empty"""
        if self.cards:
            return(self.cards[-1])
        return("")
    
    def showTopCards(self):
        """Return the "top" card from the stack, and an empty list of "stacked" cards"""
        if self.cards:
            return(self.cards[-1],[])
        return("",[])

    def showBottomCard(self):
        """Show the "bottom" card (= same as the "top" card for the general stack)"""
        return self.showTopCard()

    def display(self,stack_no='',show_all=False,show_from=None):
        """Generate a string rendering of the stack, optionally numbering it
        as 'stack_no', optionally showing all cards on the stack ('show_all'),
        and optionally showing all cards from 'show_from' on"""
        c = Card() # used to display an empty stack
        card_count = len(self.cards)  # "depth" of the stack

        # No cards in stack
        if not card_count:
            return(c.displayEmptyCard(stack_no))

        # One card in stack
        elif card_count == 1:
            return(self.showTopCard().display(stack_no))

        # Multiple cars in stack
        else:

            # Show all of the cards in the stack
            if show_all:
                out = self.cards[0].display(stack_no)
                for card in self.cards[1:]:
                    out = out[:Stack.__CARD_FOOTER]  # delete the last three rows of the card (the bottom half) to stack cards up
                    out += card.display()[Stack.__CARD_HEADER:]  # delete the first row of the card (the blank header)
                return(out)

            # Show all cards from 'show_from' on
            elif type(show_from) is int:

                # Multiple cards to display
                if show_from < len(self.cards) - 1:
                    out = self.cards[show_from].display(stack_no)
                    for card in self.cards[show_from+1:-1]:
                        out = out[:Stack.__CARD_FOOTER] # delete the last three rows of the card (the bottom half) to stack cards up
                        out += card.display()[Stack.__CARD_HEADER:] # delete the first row of the card (the blank header)
                    out = out[:Stack.__CARD_FOOTER] # delete the last three rows of the card (the bottom half) to stack cards up
                    out += self.cards[-1].display(extras="+"+str(show_from))[Stack.__CARD_HEADER:] # delete the first row of the card (the blank header)

                # Single card to display
                else:
                    out = self.cards[-1].display(stack_no,extras="+"+str(show_from))

                return(out)
            
            # Standard display
            else:
                return(self.showTopCard().display(stack_no,"+"+str(card_count-1)))





class TableauStack(Stack):
    """Definition of Tableau, as a sub-type of Stack"""

    def __init__(self):
        """Tableau made up of cards and a "top" card"""
        self.cards = []
        self.base = 0

    def addCards(self,cards,initialise=False):
        """Add 'cards' to tableau, optionally in initialisation phase"""
        self.cards += cards

        # Initialise, setting the final card to be the top
        if initialise:
            self.base = len(self.cards)-1

        # Not initialising, but stacking cards on an empty tableau
        elif len(self.cards) == len(cards):
            self.base = 0


    def removeCard(self):
        """Remove a single card from the tableau"""
        
        # Update the 'top' if the card to be removed is the top (i.e. not a stacked card)
        if self.base == len(self.cards)-1:
            self.base -= 1

        # Remove the card
        return self.cards.pop()

    def removeCards(self,n):
        """Remove 'n' cards from the tableau"""
        ret_cards = [self.removeCard()]  # cards which are removed
        
        # Remove cards one at a time
        for i in range(n-1):
            ret_cards.append(self.removeCard())

        return ret_cards

    def showTopCard(self):
        """Show the "top" card, or the empty string if there is no top card (empty tableau)"""
        if self.cards:
            return(self.cards[self.base])
        return("")

    def showBottomCard(self):
        """Show the "bottom" card, or the empty string if there is no bottom card (empty tableau)"""
        if self.cards:
            return(self.cards[-1])
        return("")

    def showTopCards(self):
        """Show the top card and the list of all cards stacked on it; 
        empty string and empty list if empty tableau"""
        if self.cards:
            return(self.cards[self.base],self.cards[self.base+1:])
        return("",[])

    def isValidAdd(self, card):
        """Can 'card' be added to the current tableau (right colour and value)?"""
        if not self.showBottomCard():
            return card.isKing()
        return card.getSuitColour() != self.showBottomCard().getSuitColour() and card.nextValue() == self.showBottomCard().getValue()




class FoundationStack(Stack):
    """Definition of Foundation, as a sub-type of Stack"""

    # constants associated with FoundationStack:
    __ALL_CARDS = 13  # maximum number of cars on a Foundation stack

    def isValidAdd(self,card):
        """Can 'card' be added to the current foundation (right value and suit)?"""
        if not self.showTopCard():
            return card.isAce()
        return card.getSuit() == self.showTopCard().getSuit() and card.prevValue() == self.showTopCard().getValue()

    def complete(self):
        """Is the foundation "complete", i.e. contain all cards for the suit?"""
        return len(self.cards) == self.__ALL_CARDS





class Deck(Stack):
    """Definition of Deck (= Trash), as a sub-type of Stack"""

    # constants associated with Deck:
    __DECK_CARD_TURN_NUMBER = 3  # the number of cards from the deck to count off in one "draw"

    def __init__(self):
        """Initialise 'cards' to suffled list of all 52 card possibilities"""
        c = Card()
        self.cards = [c.createCard(value,suit) for value in c.getValue() for suit in c.getSuit()]
        self.__shuffle()

    def __shuffle(self):
        """Shuffle the deck (in-place)"""
        shuffle(self.cards)

    def shiftTopCard(self):
        """Count off a single card from the top of the deck"""
        if self.cards:
            top = self.cards.pop(0)
            self.cards = self.cards + [top]

    def nextCard(self):
        """Count off 'DECK_CARD_TURN_NUMBER' cards from the deck"""
        if self.cards:
            for i in range(Deck.__DECK_CARD_TURN_NUMBER):
                self.shiftTopCard()
                





class Game():
    """Definition of Game, made up of the tableaux, foundation stacks and deck"""

    # constants associated with Game:
    TABLEAUX = 7  # number of tableaux (of increasing size)

    def __init__(self):
        """A game is made up of 'TABLEAUX' tableaux, one foundation stack per
        card suit, a shuffled deck of cards; deal out the cards across the tableaux"""

        # initialise the tableaux
        self.tableau = [TableauStack() for i in range(0,Game.TABLEAUX)]  

        # initialise the foundation stacks
        self.foundation = {}  

        # initialise and suffle the deck of cards
        self.deck = Deck()  

        # number of cards to add to the next tableau
        deck_size = 1  

        # Add 'deck_size' cards to each tableaux, incrementing 'deck_size'
        # per iteration
        for i in range(Game.TABLEAUX):
            self.tableau[i].addCards(self.deck.removeCards(deck_size),initialise=True)
            deck_size += 1

        # Initialise the foundations to empty Foundation stacks
        for suit in Card.SUITS:
            self.foundation[suit] = FoundationStack()

    def display(self,display_foundations=False,display_deck=True,show_all=False):
        """Display the various stacks in the current game, optionally displaying the
        foundation stacks ('display_foundations'), optionally displaying the deck 
        ('display_deck') and optionally disclosing the full content of each stack ('show_all')"""

        def zip_stacks(list1,list2):
            """Local function which 'zips' together the rendering of the two stacks (each
            in the form of a list of text) into a list of text globs"""
            if len(list1) < len(list2):
                out = [a+b for a,b in zip_longest(list1,list2,fillvalue=" "*len(list1[0]))]
            else:
                out = [a+b for a,b in zip_longest(list1,list2,fillvalue=" "*len(list2[0]))]
            return out

        # Display the foundation stacks first
        if display_foundations:
            out = ""

            # Render the foundation stacks as a single glob of text
            for suit in Card.SUITS:
                if out:
                    out = zip_stacks(out,self.foundation[suit].display())
                else:
                    out = self.foundation[suit].display()
            print("\n".join(out))
            print("\n")

        # Initialise the tableaux rendering based on the first tableau
        out = self.tableau[0].display('0',show_all=show_all,show_from=self.tableau[0].base)

        # Add each of the remaining tableaux the rendering
        for i in range(1,Game.TABLEAUX):
            out = zip_stacks(out,self.tableau[i].display(str(i),show_all=show_all,show_from=self.tableau[i].base))

        # Display the deck
        if display_deck:
            out = zip_stacks(out,self.deck.display(str(Game.TABLEAUX),show_all=show_all))

        print("\n".join(out))

    def solved(self):
        """Is the game solved (have all foundation stacks been completed)?"""
        for suit in Card.SUITS:
            if not self.foundation[suit].complete():
                return False
        return True
