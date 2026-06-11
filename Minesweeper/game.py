import pygame
import random
from config import *
from cell import Cell

class Minesweeper:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Сапер")
        self.clock = pygame.time.Clock()
        self.new_game()
    
    def new_game(self):
        """Метод для начала новой игры"""
        self.field = []
        for x in range(COLS):
            col = []
            for y in range(ROWS):
                col.append(Cell(x, y))
            self.field.append(col)
        
        self.place_mines()
        self.calculate_numbers()
        
        self.game_over = False
        self.game_won = False
        
        print("Новая игра начата!")
    
    def place_mines(self):
        """Метод для расстановки мин"""
        mines_placed = 0
        while mines_placed < MINES: 
            x = random.randint(0, COLS-1)
            y = random.randint(0, ROWS-1)
            if not self.field[x][y].mine:
                self.field[x][y].mine = True
                mines_placed += 1
    
    def calculate_numbers(self):
        """Метод подсчета цифр мин"""
        for x in range(COLS):
            for y in range(ROWS):
                if not self.field[x][y].mine: 
                    count = 0
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            nx, ny = x + dx, y + dy 
                            if 0 <= nx < COLS and 0 <= ny < ROWS: 
                                if self.field[nx][ny].mine:
                                    count += 1
                    self.field[x][y].count = count
    
    def open_cell(self, x, y):
        """Метод для открытия клетки"""
        cell = self.field[x][y]
        
        if cell.flag: 
            return True
        
        cell.reveal() 
        
        if cell.mine:
            self.game_over = True
            self.reveal_all_mines()
            return False
        
        if cell.count == 0:
            self.open_neighbors(x, y)
        
        self.check_win()
        return True
    
    def open_neighbors(self, x, y):
        """Метод для открытия соседей"""
        for dx in [-1, 0, 1]: 
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < COLS and 0 <= ny < ROWS:
                    neighbor = self.field[nx][ny]
                    if not neighbor.open and not neighbor.flag:
                        neighbor.reveal()
                        if neighbor.count == 0: 
                            self.open_neighbors(nx, ny)
    
    def reveal_all_mines(self):
        """Метод для показа всех мин"""
        for x in range(COLS):
            for y in range(ROWS):
                if self.field[x][y].mine:
                    self.field[x][y].reveal()
    
    def check_win(self):
        """Метод для проверки победы"""
        closed_safe = 0 
        for x in range(COLS):
            for y in range(ROWS):
                cell = self.field[x][y]
                if not cell.mine and not cell.open: 
                    closed_safe += 1
        
        if closed_safe == 0:
            self.game_won = True
            for x in range(COLS):
                for y in range(ROWS):
                    if self.field[x][y].mine:
                        self.field[x][y].flag = True
    
    def count_flags(self):
        """Метод для подсчета флагов"""
        flags = 0
        for x in range(COLS):
            for y in range(ROWS):
                if self.field[x][y].flag:
                    flags += 1
        return flags
    
    def draw_interface(self):
        """Метод для рисования интерфейса"""
        ui_y = ROWS * TILE_SIZE 
        
        pygame.draw.rect(self.screen, UI_BG,(0, ui_y, SCREEN_WIDTH, SCREEN_HEIGHT - ui_y))
        
        pygame.draw.line(self.screen, WHITE,(0, ui_y), (SCREEN_WIDTH, ui_y), 2)
        
        flags = self.count_flags()
        mines_left = MINES - flags 
        
        counter_rect = pygame.Rect(20, ui_y + 20, 120, 40)
        pygame.draw.rect(self.screen, DARK_GRAY, counter_rect)
        pygame.draw.rect(self.screen, WHITE, counter_rect, 2)
        
        counter_font = pygame.font.Font(None, 32)
        counter_text = counter_font.render(f"Мин: {mines_left}", True, WHITE)
        self.screen.blit(counter_text, (35, ui_y + 30))
        
        help_font = pygame.font.Font(None, 22) 
        help_text = help_font.render("Управление:", True, WHITE)
        self.screen.blit(help_text, (SCREEN_WIDTH - 200, ui_y + 15)) 
        
        controls = [
                    "• ЛКМ - открыть клетку",
                    "• ПКМ - поставить флаг",
                    "• ПРОБЕЛ - новая игра"
                                             ]
        for i, control in enumerate(controls): 
            control_text = help_font.render(control, True, WHITE) 
            self.screen.blit(control_text, (SCREEN_WIDTH - 200, ui_y + 40 + i * 25)) 
    
    def draw(self):
        """Заливка фона игрового поля"""
        self.screen.fill(BG_COLOR)
        
        for x in range(COLS):
            for y in range(ROWS):
                self.field[x][y].draw(self.screen) 
        
        self.draw_interface()
        
        if self.game_over or self.game_won: 
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            self.screen.blit(overlay, (0, 0))
            
            big_font = pygame.font.Font(None, 72)
            if self.game_over:
                text = "ПРОИГРЫШ!"
                color = RED
            else:
                text = "ПОБЕДА!"
                color = GREEN

    
            msg = big_font.render(text, True, color)
            msg_shadow = big_font.render(text, True, BLACK)
            
            self.screen.blit(msg_shadow, 
                           (SCREEN_WIDTH//2 - msg.get_width()//2 + 2,
                            SCREEN_HEIGHT//2 - msg.get_height()//2 + 2))
            
            self.screen.blit(msg, 
                           (SCREEN_WIDTH//2 - msg.get_width()//2,
                            SCREEN_HEIGHT//2 - msg.get_height()//2))
            
            hint_font = pygame.font.Font(None, 28)
            hint = hint_font.render("Нажмите ПРОБЕЛ для новой игры", True, WHITE)
            hint_shadow = hint_font.render("Нажмите ПРОБЕЛ для новой игры", True, BLACK)
            
            self.screen.blit(hint_shadow,
                           (SCREEN_WIDTH//2 - hint.get_width()//2 + 1,
                            SCREEN_HEIGHT//2 + 40 + 1))
            self.screen.blit(hint,
                           (SCREEN_WIDTH//2 - hint.get_width()//2,
                            SCREEN_HEIGHT//2 + 40))
    
    def run(self):
        """Метод запуска игры"""
        running = True 
        
        print("=" * 40)
        print("ИГРА 'САПЕР'")
        print("Поле: 9x9, мин: 10")
        print("Управление:")
        print("  Левая кнопка мыши - открыть клетку")
        print("  Правая кнопка мыши - флаг")
        print("  ПРОБЕЛ - новая игра")
        print("=" * 40)
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    cell_x = mouse_x // TILE_SIZE
                    cell_y = mouse_y // TILE_SIZE
                    
                    if 0 <= cell_x < COLS and 0 <= cell_y < ROWS:
                        if event.button == 1:
                            if not self.game_over and not self.game_won:
                                self.open_cell(cell_x, cell_y)
                        elif event.button == 3:
                            if not self.game_over and not self.game_won:
                                self.field[cell_x][cell_y].toggle_flag()
                
                if event.type == pygame.KEYDOWN
                    if event.key == pygame.K_SPACE:
                        self.new_game()
                    elif event.key == pygame.K_ESCAPE:
                        running = False
            
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit() # Когда сработает running = false, выйдем из цикла и завершим игру

if __name__ == "__main__":
    game = Minesweeper()
    game.run()
