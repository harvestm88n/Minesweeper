import pygame
from config import *

class Cell:
    def __init__(self, x, y):
        self.x = x            # Номер столбца (0-8)
        self.y = y            # Номер строки (0-8)
        self.mine = False     # Есть ли мина?
        self.open = False     # Открыта ли клетка?
        self.flag = False     # Есть ли флаг?
        self.count = 0        # Сколько мин вокруг? (0-8)
    
    def draw(self, screen): # Функция отрисовки клетки
        # Вычисление позицию клетки в пикселях
        px = self.x * TILE_SIZE # Столбец * на размер клетки
        py = self.y * TILE_SIZE # Строка * размер клетки
        
        if self.open:
            pygame.draw.rect(screen, (220, 220, 220),(px, py, TILE_SIZE, TILE_SIZE)) # Фон открытой клетки
            pygame.draw.rect(screen, DARK_GRAY,(px, py, TILE_SIZE, TILE_SIZE), 1) # Рамка
            
            if self.mine:  # Мина
                center_x = px + TILE_SIZE // 2 # Вычисляем центр клетки
                center_y = py + TILE_SIZE // 2
                pygame.draw.circle(screen, BLACK, (center_x, center_y), 20)

            elif self.count > 0:  # Цифра
                font = pygame.font.Font(None, 36)
                color = BLUE if self.count == 1 else GREEN
                text = font.render(str(self.count), True, color)
                screen.blit(text, (px + 22, py + 18))
                
        else:  # Закрытая клетка
            pygame.draw.rect(screen, GRAY, (px, py, TILE_SIZE, TILE_SIZE))
            
            # Верхняя и левая грани
            pygame.draw.line(screen, WHITE,(px, py), (px + TILE_SIZE, py), 3)
            pygame.draw.line(screen, WHITE,(px, py), (px, py + TILE_SIZE), 3)
            
            # Нижняя и правая грани
            pygame.draw.line(screen, DARK_GRAY,(px, py + TILE_SIZE),(px + TILE_SIZE, py + TILE_SIZE), 3)
            pygame.draw.line(screen, DARK_GRAY,(px + TILE_SIZE, py), (px + TILE_SIZE, py + TILE_SIZE), 3)
            
            if self.flag:  # Флаг
                pygame.draw.rect(screen, RED,(px + 18, py + 12, 24, 16))
                pygame.draw.line(screen, BLACK,(px + 30, py + 12),(px + 30, py + 48), 2)
    
    def reveal(self): # Метод для открытия клетки
        self.open = True
    
    def toggle_flag(self): # Метод для флага
        if not self.open:
            self.flag = not self.flag
