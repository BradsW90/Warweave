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
deck = [
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

#---------------Handle Input Events-----------------------
def event_handler():
    global running, selected, game_state, selected_card_index, card_menu_open, menu_option, placeing, converting, hide, fieldX, fieldY, oldFieldY, oldFieldX

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
                if event.key == pygame.K_a and not card_menu_open and not placeing:
                    if playerTurn == 0 and len(playerOne_hand) > 0:
                        selected_card_index = (selected_card_index -1) % len(playerOne_hand)
                    elif playerTurn == 1 and len(playerOne_hand) > 0:
                        selected_card_index = (selected_card_index -1) % len(playerTwo_hand)
                if event.key == pygame.K_d and not card_menu_open and not placeing:
                    if playerTurn == 0 and len(playerOne_hand) > 0:
                        selected_card_index = (selected_card_index +1) % len(playerOne_hand)
                    elif playerTurn ==1 and len(playerOne_hand) > 0:
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
                    if not card_menu_open and not placeing and not hide and len(playerOne_hand) > 0:
                        card_menu_open = True
                    elif card_menu_open and menu_option == 0 and not hide:
                        placeing = True
                        hide = True
                        card_menu_open = False
                    elif card_menu_open and menu_option == 1 and not hide:
                        card_menu_open =False
                        converting = True
                    elif not card_menu_open and placeing and hide:
                        play_card()
                        selected_card_index -= 1
                        placeing = False
                        hide = False
                if event.key == pygame.K_q:
                    if card_menu_open:
                        card_menu_open = False
                    if placeing:
                        placeing = False
                        hide = False
                        fieldX = 0
                        fieldY = 3
                if card_menu_open:
                    if event.key == pygame.K_w:
                        menu_option = (menu_option -1) % len(action_menu)
                    if event.key == pygame.K_s:
                        menu_option = (menu_option +1) % len(action_menu)

def deck_draw(num):
    global deck, playerOne_hand, playerTwo_hand

    for _ in range(num):
        draw = randint(0,len(deck)-1)
        card = Card(**deck[draw])
        deck.pop(draw)
        if playerTurn == 0:
            playerOne_hand.append(card)
        elif playerTurn == 1:
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
    global playerOne_hand, playerOne_fields
    if playerTurn == 0:
        if not playerOne_fields[fieldY-2][fieldX]["terrain"] and playerOne_hand[selected_card_index].cardType == "resource":
            card = playerOne_hand.pop(selected_card_index)
            playerOne_fields[fieldY-2][fieldX]["cards"].append(card)
            playerOne_fields[fieldY-2][fieldX]["terrain"] = True
        if playerOne_fields[fieldY-2][fieldX]["terrain"] and resources >= playerOne_hand[selected_card_index].cost:
            card = playerOne_hand.pop(selected_card_index)
            playerOne_fields[fieldY-2][fieldX]["cards"].append(card)
            playerOne_fields[fieldY-2][fieldX]["occupied"] = True

def update_game():
    global phase, resources, converting, selected_card_index

    if phase == "draw" and turn < 2:
        deck_draw(4)
        phase = "main"

    if converting:
        if playerTurn == 0:
            card = playerOne_hand[selected_card_index]
            resources += card.asResource(playerOne_hand, playerOne_fields[0][5]["cards"])
            playerOne_fields[0][5]["count"] += 1
            selected_card_index -= 1
        converting = False

    

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
                                window.blit(finished_layer, finished_layer.get_rect(topleft=(x,y)))
                else:
                    if j < 5:
                        if len(playerOne_fields[2-i][j]["cards"]):
                            for layer in playerOne_fields[2-i][j]["cards"]:
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