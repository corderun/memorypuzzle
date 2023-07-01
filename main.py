import pygame
import random

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
CARD_WIDTH, CARD_HEIGHT = 64, 64
CARDS_X, CARDS_Y = 8, 6
CARD_MARGIN = 10
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50

PAIRS_COUNT = CARDS_X * CARDS_Y // 2

BACKGROUND = (237, 234, 216)
TEXT_COLOR = (48, 46, 29)
OPEN_CARD = (224, 219, 182)
HIDDEN_COLOR = (128, 124, 97)
BUTTON_COLOR = (150, 139, 68)

SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class Card:
    def __init__(self, pair_id, symbol):
        self.pair_id = pair_id
        self.symbol = symbol
        self.is_open = False
        self.is_removed = False


def init_cards():
    symbols = list(range(1, BOARD_WIDTH * BOARD_HEIGHT // 2 + 1)) * 2
    random.shuffle(symbols)

    return [[Card(symbols[i * BOARD_WIDTH + j], SYMBOLS[symbols[i * BOARD_WIDTH + j] % len(SYMBOLS)]) for j in
             range(BOARD_WIDTH)] for i in range(BOARD_HEIGHT)]


BOARD_WIDTH = 6
BOARD_HEIGHT = 6


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Memory Puzzle")

    clock = pygame.time.Clock()

    cards = init_cards()

    selected_cards = []
    score = 0
    combo = 0
    bestscore = 0

    font = pygame.font.Font(None, CARD_HEIGHT // 2)

    total_width = BOARD_WIDTH * (CARD_WIDTH + CARD_MARGIN) - CARD_MARGIN
    total_height = BOARD_HEIGHT * (CARD_HEIGHT + CARD_MARGIN) - CARD_MARGIN

    offset_x = (SCREEN_WIDTH - total_width) // 2
    offset_y = (SCREEN_HEIGHT - total_height) // 2

    button = pygame.Rect((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT)

    show_all = True
    show_all_timer = pygame.time.get_ticks() + 3000

    running = True
    while running:
        all_open = all(card.is_removed for row in cards for card in row)

        screen.fill(BACKGROUND)
        for i, row in enumerate(cards):
            for j, card in enumerate(row):
                if not card.is_removed:
                    rect = pygame.Rect(j * (CARD_WIDTH + CARD_MARGIN) + offset_x, i * (CARD_HEIGHT + CARD_MARGIN) + offset_y, CARD_WIDTH, CARD_HEIGHT)
                    color = HIDDEN_COLOR
                    if card.is_open or (show_all and pygame.time.get_ticks() < show_all_timer):
                        color = OPEN_CARD
                    pygame.draw.rect(screen, color, rect)
                    if card.is_open or (show_all and pygame.time.get_ticks() < show_all_timer):
                        text = font.render(str(card.symbol), True, TEXT_COLOR)
                        screen.blit(text, rect.move((CARD_WIDTH - text.get_width()) // 2, (CARD_HEIGHT - text.get_height()) // 2))

        if all_open:
            if(score > bestscore):
                bestscore = score
            text = font.render('Вы выиграли!', True, TEXT_COLOR)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, button.top - 40))
            screen.blit(text, text_rect)

            text = font.render('Лучший счет: ' + str(bestscore), True, TEXT_COLOR)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, button.top - 20))
            screen.blit(text, text_rect)

            pygame.draw.rect(screen, BUTTON_COLOR, button)
            text = font.render('Заново', True, TEXT_COLOR)
            screen.blit(text, button.move((BUTTON_WIDTH - text.get_width()) // 2, (BUTTON_HEIGHT - text.get_height()) // 2))

        score_text = font.render('Счет: ' + str(score), True, TEXT_COLOR)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if all_open and not show_all and button.collidepoint(x, y):
                    cards = init_cards()
                    selected_cards = []
                    show_all = True
                    show_all_timer = pygame.time.get_ticks() + 1000
                    score = 0
                    combo = 0
                    continue

                i = (y - offset_y) // (CARD_HEIGHT + CARD_MARGIN)
                j = (x - offset_x) // (CARD_WIDTH + CARD_MARGIN)
                if 0 <= i < BOARD_HEIGHT and 0 <= j < BOARD_WIDTH:
                    card = cards[i][j]
                    if not card.is_open and not card.is_removed:
                        card.is_open = True
                        selected_cards.append(card)
                        if len(selected_cards) == 2:
                            rect = pygame.Rect(j * (CARD_WIDTH + CARD_MARGIN) + offset_x, i * (CARD_HEIGHT + CARD_MARGIN) + offset_y, CARD_WIDTH, CARD_HEIGHT)
                            color = OPEN_CARD
                            pygame.draw.rect(screen, color, rect)
                            text = font.render(str(card.symbol), True, TEXT_COLOR)
                            screen.blit(text, rect.move((CARD_WIDTH - text.get_width()) // 2, (CARD_HEIGHT - text.get_height()) // 2))
                            pygame.display.flip()

                            pygame.time.wait(1000)
                            if selected_cards[0].pair_id != selected_cards[1].pair_id:
                                selected_cards[0].is_open = False
                                selected_cards[1].is_open = False
                                combo = 0
                            else:
                                selected_cards[0].is_removed = True
                                selected_cards[1].is_removed = True
                                if combo == 1:
                                    score *= 2
                                else:
                                    score += 2
                                    combo = 1

                            selected_cards = []

                            score += 0

        if show_all and pygame.time.get_ticks() >= show_all_timer:
            show_all = False
            for row in cards:
                for card in row:
                    card.is_open = False

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()