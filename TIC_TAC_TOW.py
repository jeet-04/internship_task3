import pygame
import sys

# Initialize pygame
pygame.init()

# Screen settings (Fullscreen)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
LINE_COLOR = (255, 165, 0)  # Orange for vibrant look
X_COLOR = (200, 0, 200)  # Purple for Player X
O_COLOR = (0, 200, 200)  # Cyan for Player O
BG_COLOR = (10, 10, 30)  # Dark navy gradient background
TITLE_COLOR = (255, 215, 0)  # Gold color for title
WHITE = (240, 240, 240)  # Define white color

# Enhanced Fonts
FONT = pygame.font.Font(None, 120)
TITLE_FONT = pygame.font.Font(None, 140)
RESULT_FONT = pygame.font.Font(None, 140)
MESSAGE_FONT = pygame.font.Font(None, 80)

# Board setup
board = [[" " for _ in range(3)] for _ in range(3)]
player_turn = "X"
game_over = False
winner = None

def draw_board():
    """Draws the Tic-Tac-Toe board with an attractive background and properly aligned Xs and Os."""
    screen.fill(BG_COLOR)

    # Draw title
    title_text = TITLE_FONT.render("TICTACTOE GAME", True, TITLE_COLOR)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 80))
    screen.blit(title_text, title_rect)

    # Draw grid lines
    grid_start_y = 180  # Offset for title
    cell_size = HEIGHT // 3 - 50

    for row in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (0, grid_start_y + row * cell_size), (WIDTH, grid_start_y + row * cell_size), 10)
    for col in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (col * WIDTH // 3, grid_start_y), (col * WIDTH // 3, HEIGHT), 10)

    # Draw Xs and Os with improved alignment
    for row in range(3):
        for col in range(3):
            if board[row][col] != " ":
                text = FONT.render(board[row][col], True, X_COLOR if board[row][col] == "X" else O_COLOR)
                text_rect = text.get_rect(center=((col * WIDTH // 3 + WIDTH // 6), (grid_start_y + row * cell_size + cell_size // 2)))
                screen.blit(text, text_rect)

    pygame.display.flip()

def show_post_game():
    """Displays a visually enhanced post-game screen with properly aligned text and stylish fonts."""
    screen.fill(BG_COLOR)  # Set background color

    # Apply a subtle background overlay for effect
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)  # Semi-transparent overlay
    overlay.fill((20, 20, 50))  # Slightly lighter navy shade
    screen.blit(overlay, (0, 0))

    # Centered Result Message
    result_message = f"{winner} Wins!" if winner != "Draw" else "It's a Draw!"
    result_text = RESULT_FONT.render(result_message, True, TITLE_COLOR)
    result_rect = result_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))

    # Instruction Message
    message_text = MESSAGE_FONT.render("PRESS ENTER TO RESTART OR ESC TO EXIT", True, WHITE)
    message_rect = message_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

    # Render texts
    screen.blit(result_text, result_rect)
    screen.blit(message_text, message_rect)

    pygame.display.flip()

    # Keep the window open until the player presses ENTER or ESC
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    restart_game()
                    return
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def check_winner():
    """Checks for a winner or draw."""
    global winner, game_over

    for row in board:
        if row[0] == row[1] == row[2] != " ":
            winner = row[0]
            game_over = True
            return

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != " ":
            winner = board[0][col]
            game_over = True
            return

    if board[0][0] == board[1][1] == board[2][2] != " ":
        winner = board[0][0]
        game_over = True
        return
    if board[0][2] == board[1][1] == board[2][0] != " ":
        winner = board[0][2]
        game_over = True
        return

    if all(cell != " " for row in board for cell in row):
        winner = "Draw"
        game_over = True

def restart_game():
    """Resets the game state."""
    global board, player_turn, game_over, winner
    board = [[" " for _ in range(3)] for _ in range(3)]
    player_turn = "X"
    game_over = False
    winner = None

running = True
while running:
    draw_board()

    if game_over:
        show_post_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
            pygame.quit()
            sys.exit()

        if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            grid_start_y = 180
            cell_size = HEIGHT // 3 - 50
            row, col = (y - grid_start_y) // cell_size, x // (WIDTH // 3)

            if 0 <= row < 3 and board[row][col] == " ":
                board[row][col] = player_turn
                check_winner()
                if not game_over:
                    player_turn = "O" if player_turn == "X" else "X"