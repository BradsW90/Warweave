import pygame
from random import randint

pygame.init()
pygame.font.init()

#---------------Game State Variables and Setup-------------------
WIDTH = 1280
HEIGHT = 720
FPS = 60
game_state = "title"
running = True
selected = 0

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("War Weave")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 48)
statFont = pygame.font.Font(None, 18)
smallStatFont = pygame.font.Font(None, 12)

#---------------Title Menu Variables-----------------------------
title_options = ["Play", "Quit"]

#--------------------Card Class----------------------------------
class Card():
    def __init__(self, name, terrain, cost, atk, defe, effect, cardType, image):
        self.name = name
        self.terrain = terrain
        self.cost = cost
        self.atk = atk
        self.defe = defe
        self.effect = effect
        self.cardType = cardType
        self.image = image

    def asResource(self, hand, discard_pile):
        for i, j in enumerate(hand):
            if self == j:
                discard_pile.append(hand.pop(i))
        return self.cost // 2 if self.cost > 1 else 1
    
    def viewCard(self):
        print(self.name + " " + str(self.terrain) + " " + str(self.cost) + " " + str(self.atk) + " " + str(self.defe) + " " + str(self.effect) + " " + self.cardType)


#-------------------Asset Loading--------------------------------
def load_image(path, size=None):
    """Load an image once and optionally resize it."""
    image = pygame.image.load(path).convert_alpha()

    if size:
        image = pygame.transform.scale(image, size)

    return image

title_image = load_image("img/title.png", (WIDTH, HEIGHT))
titleBanner_image = load_image("img/titleBanner.png", (WIDTH // 2, HEIGHT // 2))
title_option_unselected = load_image("img/title_unselected.png", (WIDTH // 4, HEIGHT // 3))
title_option_selected = load_image("img/title_selected.png", (WIDTH // 4, HEIGHT // 3))
forest_image = load_image("img/forest.png", (125,175))
wild_dog_image = load_image("img/wild_dog.png", (125,175))
gregory_image = load_image("img/gregory.png", (125,175))
board = load_image("img/board.png")

#-----------------Game Variables---------------------------------
p1Deck = [
    {
        "name": "Forest",
        "terrain": "Forest",
        "cost": 1,
        "atk": 0,
        "defe": 0,
        "effect": None,
        "cardType": "resource",
        "image": forest_image
    },
    {
        "name": "Wild Dog",
        "terrain": "Forest",
        "cost": 3,
        "atk": 4,
        "defe": 2,
        "effect": None,
        "cardType": "creature",
        "image": wild_dog_image
    },
    {
        "name": "Grand Adventurer Gregory",
        "terrain": "Forest",
        "cost": 2,
        "atk": 2,
        "defe": 2,
        "effect": None,
        "cardType": "creature",
        "image": gregory_image
    },
    {
        "name": "Forest",
        "terrain": "Forest",
        "cost": 1,
        "atk": 0,
        "defe": 0,
        "effect": None,
        "cardType": "resource",
        "image": forest_image
    }
]

p2Deck = [
    {
        "name": "Forest",
        "terrain": "Forest",
        "cost": 1,
        "atk": 0,
        "defe": 0,
        "effect": None,
        "cardType": "resource",
        "image": forest_image
    },
    {
        "name": "Wild Dog",
        "terrain": "Forest",
        "cost": 3,
        "atk": 4,
        "defe": 2,
        "effect": None,
        "cardType": "creature",
        "image": wild_dog_image
    },
    {
        "name": "Grand Adventurer Gregory",
        "terrain": "Forest",
        "cost": 2,
        "atk": 2,
        "defe": 2,
        "effect": None,
        "cardType": "creature",
        "image": gregory_image
    },
    {
        "name": "Forest",
        "terrain": "Forest",
        "cost": 1,
        "atk": 0,
        "defe": 0,
        "effect": None,
        "cardType": "resource",
        "image": forest_image
    }
]

playerOne_fields = [
    [
        {
            "name": "field",
            "terrain": None,
            "occupied": None,
            "cards": []
        },
        {
            "name": "field",
            "terrain": None,
            "occupied": None,
            "cards": []
        },
        {
            "name": "field",
            "terrain": None,
            "occupied": None,
            "cards": []
        },
        {
            "name": "field",
            "terrain": None,
            "occupied": None,
            "cards": []
        },
        {
            "name": "field",
            "terrain": None,
            "occupied": None,
            "cards": []
        },
        {
            "name": "discard_pile",
            "count": 0,
            "cards": []
        }
    ],
    [
        {
            "name": "field",
            "terrain": None,
            "occupied": None,
            "cards": []
        },
        {
            "name": "field",
            "terrain": None,
            "occupied": None,
            "cards": []
        },
        {
            "name": "field",
            "terrain": None,
            "occupied": None,
            "cards": []
        },
        {
            "name": "field",
            "terrain": None,
            "occupied": None,
            "cards": []
        },
        {
            "name": "field",
            "terrain": None,
            "occupied": None,
            "cards": []
        },
        {
            "name": "deck",
            "count": 0,
            "cards": []
        }
    ]
]

playerTwo_fields = [
    [
        {
            "name": "field",
            "terrain": None,
            "occupied": None,
            "cards": []
        },
        {
            "name": "field",
            "terrain": None,
            "occupied": None,
            "cards": []
        },
        {
            "name": "field",
            "terrain": None,
            "occupied": None,
            "cards": []
        },
        {
            "name": "field",
            "terrain": None,
            "occupied": None,
            "cards": []
        },
        {
            "name": "field",
            "terrain": None,
            "occupied": None,
            "cards": []
        },
        {
            "name": "discard_pile",
            "count": 0,
            "cards": []
        }
    ],
    [
        {
            "name": "field",
            "terrain": None,
            "occupied": None,
            "cards": []
        },
        {
            "name": "field",
            "terrain": None,
            "occupied": None,
            "cards": []
        },
        {
            "name": "field",
            "terrain": None,
            "occupied": None,
            "cards": []
        },
        {
            "name": "field",
            "terrain": None,
            "occupied": None,
            "cards": []
        },
        {
            "name": "field",
            "terrain": None,
            "occupied": None,
            "cards": []
        },
        {
            "name": "deck",
            "count": 0,
            "cards": []
        }
    ]
]
playerOne_hand = []
playerTwo_hand = []
turn = 0
resources = 0
phase = "draw"
hide = False
playerTurn = 0
cardPos = [0,0]
selected_card_index = 0
card_menu_open = False
menu_option = 0
action_menu = ["Place", "Convert to Resource"]
placeing = False
converting = False
fieldX = 0
fieldY = 3
field_menu = False
field_menu_options = ["View Field", "End Turn", "Concede"]
field_selected = 0

#---------------Handle Input Events-----------------------
def event_handler():
    global running, selected, game_state, selected_card_index, card_menu_open, menu_option, placeing, converting, hide, fieldX, fieldY, oldFieldY, oldFieldX, field_menu
    global field_selected, phase, turn
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if game_state == "title":
                if event.key == pygame.K_s:
                    selected = (selected - 1) % len(title_options)
                if event.key == pygame.K_w:
                    selected = (selected + 1) % len(title_options)
                if event.key == pygame.K_RETURN:
                    if selected == 0:
                        game_state = "game"
                    elif selected == 1:
                        running = False
            elif game_state == "game":
                if event.key == pygame.K_a and not card_menu_open and not placeing and not field_menu:
                    if playerTurn == 0 and len(playerOne_hand) > 0:
                        selected_card_index = (selected_card_index -1) % len(playerOne_hand)
                    elif playerTurn == 1 and len(playerTwo_hand) > 0:
                        selected_card_index = (selected_card_index -1) % len(playerTwo_hand)
                if event.key == pygame.K_d and not card_menu_open and not placeing and not field_menu:
                    if playerTurn == 0 and len(playerOne_hand) > 0:
                        selected_card_index = (selected_card_index +1) % len(playerOne_hand)
                    elif playerTurn ==1 and len(playerTwo_hand) > 0:
                        selected_card_index = (selected_card_index +1) % len(playerTwo_hand)
                if event.key == pygame.K_a and placeing and hide:
                    fieldX -= 1
                if event.key == pygame.K_d and placeing and hide:
                    fieldX += 1
                if event.key == pygame.K_w and placeing and hide:
                    fieldY -= 1
                if event.key == pygame.K_s and placeing and hide:
                    fieldY += 1
                if event.key == pygame.K_e:
                    if not card_menu_open and not placeing and not hide and len(playerOne_hand) > 0 and playerTurn == 0 and not field_menu:
                        card_menu_open = True
                    elif not card_menu_open and not placeing and not hide and len(playerTwo_hand) > 0 and playerTurn == 1 and not field_menu:
                        card_menu_open = True
                    elif card_menu_open and menu_option == 0 and not hide and not field_menu:
                        placeing = True
                        hide = True
                        card_menu_open = False
                    elif card_menu_open and menu_option == 1 and not hide and not field_menu:
                        card_menu_open =False
                        converting = True
                    elif not card_menu_open and placeing and hide:
                        play_card()
                        reset_options()
                        placeing = False
                        hide = False
                    elif field_menu:
                        if field_selected == 1:
                            reset_options()
                            phase="end"
                            field_selected = 0
                            turn += 1
                            field_menu = False
                if event.key == pygame.K_q:
                    if card_menu_open and not field_menu:
                        card_menu_open = False
                        reset_options(False, True, True)
                    elif placeing:
                        placeing = False
                        hide = False
                        reset_options(False, True, True)
                    elif field_menu:
                        reset_options()
                        field_menu = False
                if card_menu_open and not field_menu:
                    if event.key == pygame.K_w:
                        menu_option = (menu_option -1) % len(action_menu)
                    if event.key == pygame.K_s:
                        menu_option = (menu_option +1) % len(action_menu)
                if event.key == pygame.K_TAB:
                    if not field_menu:
                        field_menu = True
                    else:
                        field_menu = False
                if field_menu:
                    if event.key == pygame.K_w:
                        field_selected = (field_selected -1) % len(field_menu_options)
                    if event.key == pygame.K_s:
                        field_selected = (field_selected +1) % len(field_menu_options)

def deck_draw(num):
    global p1Deck, playerOne_hand, playerTwo_hand, p2Deck

    for _ in range(num):
        if playerTurn == 0:
                draw = randint(0,len(p1Deck)-1)
                card = Card(**p1Deck[draw])
                p1Deck.pop(draw)
                playerOne_hand.append(card)
        elif playerTurn == 1:
            draw = randint(0, len(p2Deck)-1)
            card = Card(**p2Deck[draw])
            p2Deck.pop(draw)
            playerTwo_hand.append(card)

def draw_card(k):
    card = pygame.Surface((125,175))
    card.blit(k.image, k.image.get_rect(center=(card.width // 2, card.height // 2)))
    atk_surf = pygame.Surface((20,20))
    atk_value = statFont.render(str(k.atk), True, "white")
    atk_surf.blit(atk_value, (atk_surf.width // 3, atk_surf.height // 3))
    if k.cardType == "resource":
        name_surf = pygame.Surface((175, 15))
    else:
        name_surf = pygame.Surface((135, 15))
    #character limit 20 for statFont
    if len(k.name) > 20:
        name_value = smallStatFont.render(k.name, True, "white")
    else:
        name_value = statFont.render(k.name, True, "white")
    if not k.cardType == "resource":
        name_surf.blit(name_value, (0, 2))
    else:
        name_surf.blit(name_value, (20, 2))
    pos_name = pygame.transform.rotate(name_surf, 90)
    def_surf = pygame.Surface((20,20))
    def_value = statFont.render(str(k.defe), True, "white")
    def_surf.blit(def_value, (def_surf.width // 3, def_surf.height // 3))
    if not k.cardType == "resource":
        cost_surf = pygame.Surface((20,20))
        cost_value = statFont.render(str(k.cost), True, "white")
        cost_surf.blit(cost_value, (cost_value.width, cost_value.height // 3))
        card.blit(atk_surf, atk_surf.get_rect(topleft=(0,0)))
    if k.cardType == "resource":
        card.blit(pos_name, pos_name.get_rect(topright=(15,0)))
    else:
        card.blit(pos_name, pos_name.get_rect(topright=(15, 20)))
    if not k.cardType == "resource":
        card.blit(def_surf, def_surf.get_rect(bottomleft=(0,175)))
    if not k.cardType == "resource":
        card.blit(cost_surf, cost_surf.get_rect(bottomright=(card.width, card.height)))
    return card

def play_card():
    global playerOne_hand, playerOne_fields, resources, playerTwo_hand, playerTwo_fields
    if playerTurn == 0:
        if not playerOne_fields[fieldY-2][fieldX]["terrain"] and playerOne_hand[selected_card_index].cardType == "resource":
            card = playerOne_hand.pop(selected_card_index)
            playerOne_fields[fieldY-2][fieldX]["cards"].append(card)
            playerOne_fields[fieldY-2][fieldX]["terrain"] = True
        elif playerOne_fields[fieldY-2][fieldX]["terrain"] and resources >= playerOne_hand[selected_card_index].cost:
            card = playerOne_hand.pop(selected_card_index)
            resources -= card.cost
            playerOne_fields[fieldY-2][fieldX]["cards"].append(card)
            playerOne_fields[fieldY-2][fieldX]["occupied"] = True
    else:
        if not playerTwo_fields[fieldY-2][fieldX]["terrain"] and playerTwo_hand[selected_card_index].cardType == "resource":
            card = playerTwo_hand.pop(selected_card_index)
            playerTwo_fields[fieldY-2][fieldX]["cards"].append(card)
            playerTwo_fields[fieldY-2][fieldX]["terrain"] = True
        elif playerTwo_fields[fieldY-2][fieldX]["terrain"] and resources >= playerTwo_hand[selected_card_index].cost:
            card = playerTwo_hand.pop(selected_card_index)
            resources -= card.cost
            playerTwo_fields[fieldY-2][fieldX]["cards"].append(card)
            playerTwo_fields[fieldY-2][fieldX]["occupied"] = True

def reset_options(one=True, two=True, three=True):
    global selected_card_index, fieldX, fieldY, menu_option, selected
    if one:
        selected_card_index = 0
    if two:
        fieldX = 0
        fieldY = 3
    if three:
        menu_option = 0
    selected = 0

def update_game():
    global phase, resources, converting, selected_card_index, playerTurn

    if phase == "draw" and turn == 0 :
        deck_draw(4)
        phase = "main"
    elif phase == "draw" and turn ==1:
        phase = "main"
        deck_draw(4)
    elif phase == "draw":
        phase = "main"
        deck_draw(1)

    if converting:
        if playerTurn == 0:
            card = playerOne_hand[selected_card_index]
            resources += card.asResource(playerOne_hand, playerOne_fields[0][5]["cards"])
            playerOne_fields[0][5]["count"] += 1
        else:
            card = playerTwo_hand[selected_card_index]
            resources += card.asResource(playerTwo_hand, playerTwo_fields[0][5]["cards"])
            playerTwo_fields[0][5]["count"] += 1
        reset_options()
        converting = False
    if phase == "end":
        print(phase)
        if playerTurn == 0:
            playerTurn = 1
            phase = "draw"
        elif playerTurn == 1:
            playerTurn = 0
            phase="draw"

    

def draw_title():
    pos = 250
    textOffset = 40
    window.blit(title_image, title_image.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    window.blit(titleBanner_image, titleBanner_image.get_rect(center=(WIDTH // 2, 75)))
    for i, option in enumerate(title_options):
        if i >0:
            pos += 100
        if i == selected:
            currOption = font.render(option, True, "gold")
            window.blit(title_option_selected, title_option_selected.get_rect(center=(WIDTH // 2, pos)))
            window.blit(currOption, currOption.get_rect(center=(WIDTH // 2, pos-textOffset)))
        else:
            currOption = font.render(option, True, "white")
            window.blit(title_option_unselected, title_option_unselected.get_rect(center=(WIDTH // 2, pos)))
            window.blit(currOption, currOption.get_rect(center=(WIDTH // 2, pos-textOffset)))

def draw_game():
    global cardPos, fieldX, fieldY

    window.blit(board, board.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    x = 225
    y = 10
    current_resources = pygame.Surface((100,20))
    if not menu_option == 1:
        resource_text = statFont.render("Resources: " + str(resources), True, "white")
    else:
        current_resources = pygame.Surface((100,20))
        if playerTurn == 0:
            cardCost = playerOne_hand[selected_card_index].cost // 2 if playerOne_hand[selected_card_index].cost > 1 else 1
            cardCost += resources
            resource_text = statFont.render("Resources: " + str(cardCost), True, "green")
        else:
            cardCost = playerTwo_hand[selected_card_index].cost // 2 if playerTwo_hand[selected_card_index].cost > 1 else 1
            cardCost += resources
            resource_text = statFont.render("Resources: " + str(cardCost), True, "green")
    current_resources.blit(resource_text, resource_text.get_rect(topleft=(7, 5)))
    window.blit(current_resources, current_resources.get_rect(topleft=(10,10)))
    for i in range(4):
        if i > 0:
            y += 175
        for j in range(6):
            if j > 0:
                x += 125
            pygame.draw.rect(window, "light blue", ((x, y), (125,175)), 3)
            if playerTurn == 0:
                if i < 2:
                    if j > 0:
                        if len(playerTwo_fields[1 - i][5 - j]["cards"]) > 0:
                            for layer in playerTwo_fields[1 - i][5 - j]["cards"]:
                                finished_layer = draw_card(layer)
                                fixed = pygame.transform.rotate(finished_layer, 180)
                                window.blit(fixed, fixed.get_rect(topleft=(x,y)))
                else:
                    if j < 5:
                        if len(playerOne_fields[2-i][j]["cards"]):
                            for layer in playerOne_fields[2-i][j]["cards"]:
                                finished_layer = draw_card(layer)
                                window.blit(finished_layer, finished_layer.get_rect(topleft=(x,y)))
            elif playerTurn == 1:
                if i < 2:
                    if j > 0:
                        if len(playerOne_fields[1 - i][5 - j]["cards"]) > 0:
                            for layer in playerOne_fields[1-i][5-j]["cards"]:
                                finished_layer = draw_card(layer)
                                fixed = pygame.transform.rotate(finished_layer, 180)
                                window.blit(fixed, fixed.get_rect(topleft=(x,y)))
                else:
                    if j < 5:
                        if len(playerTwo_fields[2-i][j]["cards"]):
                            for layer in playerTwo_fields[2-i][j]["cards"]:
                                finished_layer = draw_card(layer)
                                window.blit(finished_layer, finished_layer.get_rect(topleft=(x,y)))
            if placeing:
                if fieldY < 2:
                    fieldY = 3
                if fieldY > 3:
                    fieldY = 2
                if fieldX < 0:
                    fieldX = 4
                if fieldX > 4:
                    fieldX = 0
                if j == fieldX and i == fieldY:
                    if playerTurn == 0:
                        newCard = draw_card(playerOne_hand[selected_card_index])
                        window.blit(newCard, newCard.get_rect(topleft=(x,y)))
                    else:
                        newCard = draw_card(playerTwo_hand[selected_card_index])
                        window.blit(newCard, newCard.get_rect(topleft=(x,y)))
            if j == 5:
                x = 225
            if j == 5 and i >= 1:
                x = 350
    if not hide:
        x = 0
        if playerTurn == 0:
            current_hand = playerOne_hand
        elif playerTurn == 1:
            current_hand = playerTwo_hand
        for l, k in enumerate(current_hand):
            if l > 0:
                x += 135
            card = draw_card(k)
            if l == selected_card_index:
                window.blit(card, card.get_rect(center=(100 + x, HEIGHT - 175)))
                cardPos[0], cardPos[1] = 100+x, HEIGHT-175
            else:
                window.blit(card, card.get_rect(center=(100 + x, HEIGHT - 100)))
        if card_menu_open:
            y =0
            menu = pygame.Surface((120,100))
            for a, b in enumerate(action_menu):
                if a > 0:
                    y += 20
                if menu_option == a:
                    text = statFont.render(b, True, "white")
                else:
                    text = statFont.render(b, True, "grey")
                menu.blit(text, text.get_rect(topleft=(0,y)))
            window.blit(menu, menu.get_rect(topleft=((cardPos[0] + (125 // 2)), (cardPos[1] - (175 // 2)))))
    if field_menu:
        menu_overlay = pygame.Surface((WIDTH // 2, HEIGHT // 2), pygame.SRCALPHA)
        menu_overlay.fill((0,0,0, 128))
        yOffset = 0
        for num, choice in enumerate(field_menu_options):
            if num > 0:
                yOffset += 100
            if num == field_selected:
                field_option = font.render(choice, True, "gold")
            else:
                field_option = font.render(choice, True, "white")
            menu_overlay.blit(field_option, field_option.get_rect(center=(menu_overlay.width//2, 75+yOffset)))
        window.blit(menu_overlay, menu_overlay.get_rect(center=(WIDTH//2,HEIGHT//2)))


while running:
    clock.tick(FPS)

    event_handler()

    if game_state == "title":
        draw_title()

    if game_state == "game":
        update_game()
        draw_game()

    pygame.display.flip()

pygame.quit()