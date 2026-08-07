import pygame
import sys

# Inisialisasi Pygame
pygame.init()

# Ukuran Layar & Papan (GRID_SIZE 10x10)
WIDTH, HEIGHT = 550, 710
GRID_SIZE = 10  # Papan 10x10 (100 Kotak)
CELL_SIZE = WIDTH // GRID_SIZE
BOARD_HEIGHT = WIDTH
WIN_CONDITION = 5  # Butuh 5 deret untuk menang!

# Warna-warna Modern
COLOR_BG = (15, 23, 42)
COLOR_GRID = (51, 65, 85)
COLOR_X = (56, 189, 248)      # Biru (Pemain X)
COLOR_O = (244, 63, 94)      # Merah (Pemain O)
COLOR_Y = (250, 204, 21)     # Kuning (Pemain Y)
COLOR_WHITE = (248, 250, 252)
COLOR_LINE = (34, 197, 94)     # Hijau untuk garis menang
COLOR_BTN = (30, 41, 59)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe 10x10 - 3 Players (X, O, Y)")

# Font
FONT_LARGE = pygame.font.SysFont('Segoe UI', 24, bold=True)
FONT_MED = pygame.font.SysFont('Segoe UI', 18, bold=True)
FONT_SMALL = pygame.font.SysFont('Segoe UI', 15)

# State Game
board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
players = ['X', 'O', 'Y']
turn_index = 0
winner = None
winning_line = None
game_over = False
scores = {'X': 0, 'O': 0, 'Y': 0}

def get_color(symbol):
    if symbol == 'X': return COLOR_X
    if symbol == 'O': return COLOR_O
    if symbol == 'Y': return COLOR_Y
    return COLOR_WHITE

def draw_board():
    screen.fill(COLOR_BG)
    
    # Gambar Garis Papan 10x10
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, COLOR_GRID, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 2)
        pygame.draw.line(screen, COLOR_GRID, (i * CELL_SIZE, 0), (i * CELL_SIZE, BOARD_HEIGHT), 2)
    
    # Gambar Simbol X, O, dan Y
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            symbol = board[r][c]
            if symbol != '':
                color = get_color(symbol)
                text = FONT_LARGE.render(symbol, True, color)
                rect = text.get_rect(center=(c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text, rect)

    # Gambar Garis Pemenang jika Ada
    if winning_line:
        start_pos, end_pos = winning_line
        pygame.draw.line(screen, COLOR_LINE, start_pos, end_pos, 5)

    # UI Bawah (Papan Skor 3 Pemain)
    txt_x = FONT_MED.render(f"X: {scores['X']}", True, COLOR_X)
    txt_o = FONT_MED.render(f"O: {scores['O']}", True, COLOR_O)
    txt_y = FONT_MED.render(f"Y: {scores['Y']}", True, COLOR_Y)
    
    screen.blit(txt_x, (20, BOARD_HEIGHT + 15))
    screen.blit(txt_o, (WIDTH // 2 - txt_o.get_width() // 2, BOARD_HEIGHT + 15))
    screen.blit(txt_y, (WIDTH - txt_y.get_width() - 20, BOARD_HEIGHT + 15))

    # Indikator Status / Giliran
    current_player = players[turn_index]
    if game_over:
        if winner == 'Draw':
            status_str = "Hasil Imbang (Draw)!"
            status_color = COLOR_WHITE
        else:
            status_str = f"Pemain {winner} Menang! 🎉"
            status_color = get_color(winner)
    else:
        status_str = f"Giliran: Pemain {current_player} (Susun 5)"
        status_color = get_color(current_player)

    txt_status = FONT_SMALL.render(status_str, True, status_color)
    screen.blit(txt_status, (WIDTH // 2 - txt_status.get_width() // 2, BOARD_HEIGHT + 45))

    # Tombol Restart Game
    pygame.draw.rect(screen, COLOR_BTN, (WIDTH // 2 - 70, BOARD_HEIGHT + 80, 140, 40), border_radius=8)
    lbl_reset = FONT_SMALL.render("Main Lagi", True, COLOR_WHITE)
    screen.blit(lbl_reset, (WIDTH // 2 - lbl_reset.get_width() // 2, BOARD_HEIGHT + 90))

def check_winner(last_r, last_c):
    global winner, winning_line, game_over
    player = board[last_r][last_c]
    
    # 4 Arah Pengecekan
    directions = [
        [(0, 1), (0, -1)],   # Horisontal
        [(1, 0), (-1, 0)],   # Vertikal
        [(1, 1), (-1, -1)],  # Diagonal Utama
        [(1, -1), (-1, 1)]   # Diagonal Samping
    ]

    for d1, d2 in directions:
        count = 1
        cells = [(last_r, last_c)]

        # Arah pertama
        r, c = last_r + d1[0], last_c + d1[1]
        while 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and board[r][c] == player:
            count += 1
            cells.append((r, c))
            r += d1[0]
            c += d1[1]

        # Arah sebaliknya
        r, c = last_r + d2[0], last_c + d2[1]
        while 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and board[r][c] == player:
            count += 1
            cells.append((r, c))
            r += d2[0]
            c += d2[1]

        # Jika membentuk 5 atau lebih
        if count >= WIN_CONDITION:
            winner = player
            game_over = True
            
            start_cell = min(cells)
            end_cell = max(cells)
            start_pos = (start_cell[1] * CELL_SIZE + CELL_SIZE // 2, start_cell[0] * CELL_SIZE + CELL_SIZE // 2)
            end_pos = (end_cell[1] * CELL_SIZE + CELL_SIZE // 2, end_cell[0] * CELL_SIZE + CELL_SIZE // 2)
            winning_line = (start_pos, end_pos)
            return

    # Cek Seri
    is_full = all(board[r][c] != '' for r in range(GRID_SIZE) for c in range(GRID_SIZE))
    if is_full:
        winner = 'Draw'
        game_over = True

def restart_game():
    global board, turn_index, winner, winning_line, game_over
    board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    turn_index = 0
    winner = None
    winning_line = None
    game_over = False

# Game Loop
running = True
clock = pygame.time.Clock()

while running:
    draw_board()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            # Klik Papan
            if my < BOARD_HEIGHT and not game_over:
                c = mx // CELL_SIZE
                r = my // CELL_SIZE

                if board[r][c] == '':
                    current_player = players[turn_index]
                    board[r][c] = current_player
                    check_winner(r, c)

                    if game_over:
                        if winner in players:
                            scores[winner] += 1
                    else:
                        # Rotasi giliran: X -> O -> Y -> X
                        turn_index = (turn_index + 1) % len(players)

            # Klik Tombol Restart
            elif BOARD_HEIGHT + 80 <= my <= BOARD_HEIGHT + 120:
                if WIDTH // 2 - 70 <= mx <= WIDTH // 2 + 70:
                    restart_game()

    clock.tick(30)

pygame.quit()
sys.exit()
