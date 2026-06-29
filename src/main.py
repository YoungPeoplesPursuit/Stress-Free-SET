# Install Pygame
import pygame
import random

pygame.display.init()
pygame.font.init()

#################Setup Graphics and Cards###################

# set up screen
screen = pygame.display.set_mode((1200,800),pygame.RESIZABLE) #screen dimensions and it is resizable
pygame.display.set_caption("SET")


#game running loop stuff
running = True

# make 3x4 interface grid

def drawGrid():
    for i in range(3):
        for j in range(4):
            pygame.draw.rect(screen, 'white', pygame.Rect(290*j + 40, 250*i + 50, 250, 200)) #draw 12 rectangles

# rectangle parameters: upper left coordinates, width, height

# Cards class:
class Card:
    # 4 properties to draw: number, color, shading, and shape
    def __init__(self, number, color, shading, shape):
        self.number = number
        self.color = color
        self.shading = shading
        self.shape = shape
        self.onGrid = False #is card displayed on gird right now
        self.clicked = False #is card clicked

    def toList(self): #convert card to a list for easier manipulation
        list = []
        list.append(self.number)
        list.append(self.color)
        list.append(self.shading)
        list.append(self.shape)
        return list

    # function for drawing the corresponding card on a card in the interface with coordinates of top left card corner
    def draw(self, x, y):
        for i in range(self.number+1):
            if self.shading == 0: #light shading config
                width = 5 #draw a line border
                if self.color == 0: #red
                    shade = 'crimson'
                elif self.color == 1: #green
                    shade = 'green'
                else:
                    shade = 'darkslateblue' #purple
            else:
                width = 0
                if self.shading == 1: #light color fill for mid shading
                    if self.color == 0: #red
                        shade = 'lightcoral'
                    elif self.color == 1: #green
                        shade = 'lightgreen'
                    else:
                        shade = 'lightslateblue' #purple
                else: #dark colors for dark filling
                    if self.color == 0: #red
                        shade = 'crimson'
                    elif self.color == 1: #green
                        shade = 'green'
                    else:
                        shade = 'darkslateblue' #purple
            if self.shape == 1: #oval
                pygame.draw.ellipse(screen, shade, (x+25+70*i, y+50, 60, 100), width)
            elif self.shape == 0: #diamond
                pygame.draw.polygon(screen, shade, [[x+55+70*i, y+50], [x+85+70*i, y+100],[x+55+70*i, y+150], [x+25+70*i, y+100]], width)
            else: #squiggle
                pygame.draw.polygon(screen,shade,[[x+25+70*i,y+50],[x+85+70*i,y+50],[x+55+70*i,y+80],[x+85+70*i,y+100],[x+85+70*i,y+150],[x+25+70*i,y+150],[x+55+70*i,y+120],[x+25+70*i,y+100]],width)



##################Card Deck and Logic##############################


#Deck of total cards
deck = []
#attributes represented as numbers corresponding to indices of these lists for mod 3 SET validation
attributes = ["numbers", "colors", "shadings", "shapes"]
numbers = [1,2,3]
colors = ["red", "green", "purple"]
shadings = ["light", "mid", "dark"]
shapes = ["diamond", "oval", "squiggle"]
attributeLists = [numbers, colors, shadings, shapes]

#generate 81 unique cards for the deck.
for i in range(3):
    for color in range(3):
        for shading in range(3):
            for shape in range(3):
                deck.append(Card(i,color,shading,shape))

random.shuffle(deck) #shuffle the deck
cards_on_grid_location = [] # cards and rectangles stored where are the rectangles of these cards
cards_clicked = [] #check for SETs and know which cards are clicked
#dealDeck function
def dealDeck(deck,cards_on_grid_location):
    # passing in the cards on grid list
   # Clear any existing cards from the grid list
    cards_on_grid_location.clear()
    # Ensure we have enough cards to deal
    if len(deck) < 12: #edge case when it runs out of cards in deck
        print('Not enough cards in the deck to deal 12.')
        return

    else:
        for count in range(12):
            # Take the top card from the shuffled deck
            selected_card = deck.pop(0)  # get and remove the first card

            j = count % 4  # find the remainder (column)
            i = count // 4  # find the quotient (row)

            # Don't draw here, draw in the main loop
            selected_card.onGrid = True
            card_rect = pygame.Rect(290*j + 40, 250*i + 50, 250, 200)
            cards_on_grid_location.append((selected_card, card_rect)) #add rectangle location of card to grid


# randomly generate 12 cards from deck to put on the interface
#user can click shuffle for an entirely new board

#replaceCard function
'''
old replace card function that didn't work because that list was getting mutated
def replaceCard(cardlist):
    global deck, cards_on_grid_location
    # Find the positions (Rects) of the cards to be removed
    # and replace them with new cards from the deck
    for card in cardlist:
        index = cards_on_grid_location.index(card)
        card.onGrid = False
        card.used = True
        if len(deck) > 0:  # Ensure there are cards left in the deck
            newcard = deck.pop(0)
            newcard.onGrid = True
            rect = (cards_on_grid_location[index])[1] #get 2nd entry of tuples in cards on grid location
            cards_on_grid_location.pop(index)
            cards_on_grid_location.insert(index, (newcard, rect))
        else:
            print('No cards in the deck')

'''


def replaceCard(cards_clicked, deck, cards_on_grid_location):

    # Create a list of the indexes to update
    indices_to_replace = []

    # the indexes of all cards in the cards clicked list within cards_on_grid_location
    for card_in_SET in cards_clicked:  # Iterate through the 3 cards that formed the SET
        for i, (card_on_grid, rect) in enumerate(cards_on_grid_location):
            if card_on_grid is card_in_SET:
                indices_to_replace.append(i)
                break  # Break inner loop once this specific card is found

    # loop through indexes to replace
    for index in indices_to_replace:
        old_card_at_index = cards_on_grid_location[index][0]
        old_card_at_index.onGrid = False  # Mark the old card off the grid

        if len(deck) > 0:  # check deck length
            newcard = deck.pop(0)
            newcard.onGrid = True
            newcard.clicked = False  # set new card to not clicked to be safe

            # Find rectangle for this position
            rect = cards_on_grid_location[index][1]

            # Replace the old (Card, Rect) tuple with the new (Card, Rect) tuple at this index
            cards_on_grid_location[index] = (newcard, rect)
        else:
            print('No cards in the deck, replacing with empty slot.')
            # If deck is empty, replace the slot with None
            cards_on_grid_location[index] = (None, cards_on_grid_location[index][1])


#isSET function
def isSET(cardlist): #checks if its a SET and explains why
    card1 = cardlist[0]
    card2 = cardlist[1]
    card3 = cardlist[2]

    list1 = card1.toList()
    list2 = card2.toList()
    list3 = card3.toList()
    # the 3 cards picked are a SET if for each of their properties, the variants are either all the same or all different
    # number, color, shading, shape order
    allTrue = True
    for i in range(4):
        if (list1[i]+list2[i]+list3[i]) % 3 != 0: #if the attributes don't sum to 0 mod 3 its not a SET
            allTrue = False

    return allTrue

#write the message for explaining if things are a SET or not. Very similar to the isSET function, but decided to make them different because different outputs
def explainSET(cardlist):
    card1 = cardlist[0]
    card2 = cardlist[1]
    card3 = cardlist[2]

    list1 = card1.toList()
    list2 = card2.toList()
    list3 = card3.toList()

    msg = "" #final, full message

    for i in range(4):
        if (list1[i]+list2[i]+list3[i]) % 3 != 0: #is the attributes don't match a SET
            msg = msg + "\nThe "+attributes[i]+" don't satisfy the conditions for a SET."
        else:
            if list1[i]==list2[i]:
                msg = msg + "\nThe " + attributes[i] + " are all " + str((attributeLists[i])[list1[i]]) +"."
            else:
                msg = msg + "\nThe " + attributes[i] + " are all different."

    return msg

#################Gameplay and Loop###########################

#initialize score to 0
score = 0
current_game_message = ''

# Game loop
game_started = False
# set background color to our window
screen.fill('black')
# Create font
font = pygame.font.Font('freesansbold.ttf', 32)

#popup variables
show_popup = False
popup_message = ""

# keep game running till the player closes
while running:

    # Check for event if user has pushed any event in queue
    for event in pygame.event.get():

        # if event is of type quit then set running bool to false
        if event.type == pygame.QUIT:
            running = False
            # popup appearance logic
        if show_popup:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # left click gets rid of popup
                show_popup = False
        else: #continue normal gameplay if no popups
            if event.type == pygame.MOUSEBUTTONDOWN:  # else if the user clicks something
                #get the x and y of the mouse
                click_pos = event.pos
                for card, rect in cards_on_grid_location:
                    #if it clicks a card
                    if rect.collidepoint(click_pos):
                        if len(cards_clicked) == 3 and not isSET(cards_clicked): #conditional to clear cards that aren't in a SET
                            for c in cards_clicked:
                                if c: c.clicked = False
                            cards_clicked.clear()
                        if card.clicked == True:
                    # if card clicked before:
                            card.clicked = False
                            cards_clicked.remove(card)
                        # card clicked = false
                        # remove card from cards_clicked
                        else:
                            if len(cards_clicked) < 3: #don't check for SET
                                card.clicked = True
                                cards_clicked.append(card)
                                #add card to cards.clicked and mark clicked as true
                        if len(cards_clicked) == 3:
                            current_game_message = ""
                            message_display_end_time = 0
                            if isSET(cards_clicked):
                                #if len(deck) > 0:
                                replaceCard(cards_clicked, deck, cards_on_grid_location)


                                score += 3
                                print(score)
                                print(len(deck), 'cards remaining')
                                popup_message = "It's a SET!\n" + explainSET(cards_clicked)
                                for card in cards_clicked:
                                    card.clicked = False
                                cards_clicked = []

                            else:
                                current_game_message = ""
                                smallfont = pygame.font.Font('freesansbold.ttf', 24)
                                current_message_font = smallfont
                                current_message_rect_center = (700, 25)
                                popup_message = "It's not a SET!"+ explainSET(cards_clicked)+"\nPress the space bar for new cards. Press backspace to try again."
                            show_popup = True


            elif event.type == pygame.KEYDOWN:
                current_game_message = ''
                message_display_end_time = 0 #reset message timer
                if len(cards_clicked) == 3 and not isSET(cards_clicked):
                    if event.key == pygame.K_SPACE:
                        if len(deck) > 0:
                            replaceCard(cards_clicked, deck, cards_on_grid_location)

                for card in cards_clicked:
                    card.clicked = False
                cards_clicked.clear() # Clear the list after action



########################Game Displays###############################
    screen.fill((0, 0, 0))
    drawGrid()

    # Score text to be displayed
    scorestring = 'Score: ' + str(score) + ". You have " + str(12+len(deck)) + ' cards remaining.'
    score_text = font.render(scorestring, True, 'white', 'black')
    # rectangle around text
    textRect = score_text.get_rect()
    # set the center of the rectangular object.
    textRect.center = (350, 25)
    screen.blit(score_text, textRect)  # draw text for score

    #display messages
    if current_game_message:
        message_surface = current_message_font.render(current_game_message, True, 'white', 'black')
        message_rect = message_surface.get_rect(center=current_message_rect_center)
        screen.blit(message_surface, message_rect)

    #deal the deck once game starts
    if not game_started:
        dealDeck(deck, cards_on_grid_location)
        game_started = True
    # Draw the cards that are currently on the grid
    if len(cards_on_grid_location) > 0:
        for count, cardrect in enumerate(cards_on_grid_location):
            j = count % 4
            i = count // 4
            card = cardrect[0]
            if card is not None:
                card.draw(290*j + 40, 250*i + 50)  # draw the card on the correct rectangle
                if card.clicked:
                    # cards turn gold when user clicks. User can click again to undo
                    pygame.draw.rect(screen, 'gold', pygame.Rect(290*j + 40, 250*i + 50, 250, 200),5)


    #Popups drawing
    if show_popup:

        #dims the background with a transparent black wash
        overlay = pygame.Surface((1200, 800), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        #draw the pop-up box
        popup_rect = pygame.Rect(300, 200, 600, 400)
        pygame.draw.rect(screen, (250, 250, 250), popup_rect)  # Light gray box
        pygame.draw.rect(screen, (0, 0, 0), popup_rect, 2)  # Black border

        #I need to figure out how to wrap the text because it gets long in the pop-up
        font = pygame.font.Font(None, 32)
        wrap_width_pixels = 500  # Width in pixels to wrap text

        #the wraplength automatically wraps
        text_surface = font.render(popup_message, True, (0, 0, 0), wraplength=wrap_width_pixels)
        text_rect = text_surface.get_rect(center=popup_rect.center)
        screen.blit(text_surface, text_rect)

        #permanent click to dismiss instructions
        dismiss_font = pygame.font.Font(None, 24)
        dismiss_text = dismiss_font.render("Click anywhere to dismiss", True, (50, 50, 50))
        dismiss_rect = dismiss_text.get_rect(center=(popup_rect.centerx, popup_rect.bottom - 20))
        screen.blit(dismiss_text, dismiss_rect)


    #update everything in main loop per run
    pygame.display.flip()


pygame.quit()
print(score)

