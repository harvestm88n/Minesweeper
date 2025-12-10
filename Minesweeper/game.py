import pygame
import random
from config import *
from cell import Cell

class Minesweeper:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Сапер")
        self.clock = pygame.time.Clock() # Часы для контроля ФПС
        self.new_game() # Запуск новой игры
    
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
        while mines_placed < MINES: # Пока не поставили 10 мин
            x = random.randint(0, COLS-1)
            y = random.randint(0, ROWS-1)
            if not self.field[x][y].mine: # Рандомно берем клетку и если в этой клетки нет мины, то ставим мину.
                self.field[x][y].mine = True
                mines_placed += 1
    
    def calculate_numbers(self):
        """Метод подсчета цифр мин"""
        for x in range(COLS):
            for y in range(ROWS):
                if not self.field[x][y].mine: 
                    count = 0
                    for dx in [-1, 0, 1]: # Проверяем 3 столбца
                        for dy in [-1, 0, 1]: # Проверяем 3 строки
                            nx, ny = x + dx, y + dy # Координаты соседних клеток
                            if 0 <= nx < COLS and 0 <= ny < ROWS: # Проверка на существование соседней клетки
                                if self.field[nx][ny].mine: # Если у соседа есть мина, то увеличиваем счетчик и записываем цифру
                                    count += 1
                    self.field[x][y].count = count
    
    def open_cell(self, x, y):
        """Метод для открытия клетки"""
        cell = self.field[x][y]
        
        if cell.flag: # Если на клетке стоит флаг
            return True
        
        cell.reveal() # Открытие клетки
        
        if cell.mine: # Если в клетке мина
            self.game_over = True
            self.reveal_all_mines()
            return False
        
        if cell.count == 0: # Если вокруг нет мин, то открываем соседей автоматом
            self.open_neighbors(x, y)
        
        self.check_win() # Проверка на победу
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
                        if neighbor.count == 0: # Если у соседа тоже 0, то открываем его соседей тоже
                            self.open_neighbors(nx, ny)
    
    def reveal_all_mines(self):
        """Метод для показа всех мин"""
        for x in range(COLS):
            for y in range(ROWS):
                if self.field[x][y].mine:
                    self.field[x][y].reveal()
    
    def check_win(self):
        """Метод для проверки победы"""
        closed_safe = 0 # Счетчик безопасных закрытых клеток
        for x in range(COLS):
            for y in range(ROWS):
                cell = self.field[x][y]
                if not cell.mine and not cell.open: 
                    closed_safe += 1
        
        if closed_safe == 0: # Если нет закрытых безопасных клеток
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
        ui_y = ROWS * TILE_SIZE # Позиция интерфейса под игровым полем
        
        # Фон интерфейса
        pygame.draw.rect(self.screen, UI_BG,(0, ui_y, SCREEN_WIDTH, SCREEN_HEIGHT - ui_y))
        
        # Рамка сверху
        pygame.draw.line(self.screen, WHITE,(0, ui_y), (SCREEN_WIDTH, ui_y), 2)
        
        # Счетчик мин
        flags = self.count_flags()
        mines_left = MINES - flags # 10 - flags = кол-во оставшихся мин
        
        # Панель для счетчика
        counter_rect = pygame.Rect(20, ui_y + 20, 120, 40) # прямоугольник
        pygame.draw.rect(self.screen, DARK_GRAY, counter_rect)
        pygame.draw.rect(self.screen, WHITE, counter_rect, 2)
        
        # Текст счетчика
        counter_font = pygame.font.Font(None, 32)
        counter_text = counter_font.render(f"Мин: {mines_left}", True, WHITE)
        self.screen.blit(counter_text, (35, ui_y + 30))
        
        # Инструкция справа
        help_font = pygame.font.Font(None, 22) # создаем шрифт
        help_text = help_font.render("Управление:", True, WHITE) # изображение текста с сглаживанием
        self.screen.blit(help_text, (SCREEN_WIDTH - 200, ui_y + 15)) # отрисовка текста
        
        # Пункты управления
        controls = [
                    "• ЛКМ - открыть клетку",
                    "• ПКМ - поставить флаг",
                    "• ПРОБЕЛ - новая игра"
                                             ]
        # Отрисовка пунктов панели управления
        for i, control in enumerate(controls): # Проходимся по списку и возвращаем элементы с индексами
            control_text = help_font.render(control, True, WHITE) # Для каждой инструкции создаем изображение
            self.screen.blit(control_text, (SCREEN_WIDTH - 200, ui_y + 40 + i * 25)) # Отрисовка инструкций
    
    def draw(self):
        """Заливка фона игрового поля"""
        self.screen.fill(BG_COLOR)
        
        # Отрисовка всех клетки
        for x in range(COLS):
            for y in range(ROWS):
                self.field[x][y].draw(self.screen) # Получаем объект клетки, вызываем метод draw() передавая экран для рисования
        
        # Отрисовка нижнего интерфейса
        self.draw_interface()
        
        # Сообщение о результате
        if self.game_over or self.game_won: 
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            self.screen.blit(overlay, (0, 0))
            
            big_font = pygame.font.Font(None, 72) # Cоздание большого шрифты для результата
            if self.game_over:
                text = "ПРОИГРЫШ!"
                color = RED
            else:
                text = "ПОБЕДА!"
                color = GREEN

    
            msg = big_font.render(text, True, color) # Создание текста и тени
            msg_shadow = big_font.render(text, True, BLACK)
            
            # Отрисовка тени и текста по центру
            self.screen.blit(msg_shadow, 
                           (SCREEN_WIDTH//2 - msg.get_width()//2 + 2,
                            SCREEN_HEIGHT//2 - msg.get_height()//2 + 2))
            
            self.screen.blit(msg, 
                           (SCREEN_WIDTH//2 - msg.get_width()//2,
                            SCREEN_HEIGHT//2 - msg.get_height()//2))
            
            # Шрифт подсказки
            hint_font = pygame.font.Font(None, 28)
            hint = hint_font.render("Нажмите ПРОБЕЛ для новой игры", True, WHITE)
            hint_shadow = hint_font.render("Нажмите ПРОБЕЛ для новой игры", True, BLACK)
            
            # Отрисовка тени и текста подсказки
            self.screen.blit(hint_shadow,
                           (SCREEN_WIDTH//2 - hint.get_width()//2 + 1,
                            SCREEN_HEIGHT//2 + 40 + 1))
            self.screen.blit(hint,
                           (SCREEN_WIDTH//2 - hint.get_width()//2,
                            SCREEN_HEIGHT//2 + 40))
    
    def run(self):
        """Метод запуска игры"""
        running = True  # Флаг работы игры
        
        # Вывод в консоль
        print("=" * 40)
        print("ИГРА 'САПЕР'")
        print("Поле: 9x9, мин: 10")
        print("Управление:")
        print("  Левая кнопка мыши - открыть клетку")
        print("  Правая кнопка мыши - флаг")
        print("  ПРОБЕЛ - новая игра")
        print("=" * 40)
        
        # Главный игровой цикл, который проверяет все события в игре
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Если нажали на крестик окна, игра выключается
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN: # Если нажали кнопку мыши, то узнаем где кликнули
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    cell_x = mouse_x // TILE_SIZE
                    cell_y = mouse_y // TILE_SIZE
                    
                    if 0 <= cell_x < COLS and 0 <= cell_y < ROWS: # Проверка на то, что клик был внутри поля
                        if event.button == 1:
                            if not self.game_over and not self.game_won: # Если нажата левая кнопка мыши и игра не закончена, то открываем клетку
                                self.open_cell(cell_x, cell_y)
                        elif event.button == 3:
                            if not self.game_over and not self.game_won: # Если нажата правая кнопка мыши и игра не закончена, то ставим флаг
                                self.field[cell_x][cell_y].toggle_flag()
                
                if event.type == pygame.KEYDOWN: # Если нажат пробел, то начинаем новую игру
                    if event.key == pygame.K_SPACE:
                        self.new_game()
                    elif event.key == pygame.K_ESCAPE: # Если нажат ESC, то выключаем игру
                        running = False
            
            self.draw() # Метод отрисовывания
            pygame.display.flip() # Показываем отрисованное
            self.clock.tick(60) # Выставляем 60 fps
        
        pygame.quit() # Когда сработает running = false, выйдем из цикла и завершим игру

if __name__ == "__main__":
    game = Minesweeper()
    game.run()
