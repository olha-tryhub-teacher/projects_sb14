import pygame
import sys

# Налаштування
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Вікторина")
clock = pygame.time.Clock()
FPS = 60

# Кольори
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

# Шрифти
font_question = pygame.font.SysFont(None, 36)
font_button = pygame.font.SysFont(None, 28)
font_score = pygame.font.SysFont(None, 32)

# Данні
themes = ["категорія 1", "категорія 2", "категорія 3"]

# Питання для прикладу
questions = {
    "категорія 1": [
        {"q": "питання1", "options": ["відповідь1","відповідь2","відповідь3","відповідь4"], "answer": 2},
        {"q": "питання2", "options": ["відповідь1","відповідь2","відповідь3","відповідь4"], "answer": 1},
        {"q": "питання3", "options": ["відповідь1","відповідь2","відповідь3","відповідь4"], "answer": 0},
        {"q": "питання4", "options": ["відповідь1","відповідь2","відповідь3","відповідь4"], "answer": 0},
        {"q": "питання5", "options": ["відповідь1","відповідь2","відповідь3","відповідь4"], "answer": 1},
        {"q": "питання6", "options": ["відповідь1","відповідь2","відповідь3","відповідь4"], "answer": 3},
        {"q": "питання7", "options": ["відповідь1","відповідь2","відповідь3","відповідь4"], "answer": 0},
        {"q": "питання8", "options": ["відповідь1","відповідь2","відповідь3","відповідь4"], "answer": 2},
        {"q": "питання9", "options": ["відповідь1","відповідь2","відповідь3","відповідь4"], "answer": 1},
        {"q": "питання10", "options": ["відповідь1","відповідь2","відповідь3","відповідь4"], "answer": 0},
    ],
    "категорія 2": [
        {"q": "питання1", "options": ["відповідь1","відповідь2","відповідь3","відповідь4"], "answer": 2},
        {"q": "питання2", "options": ["відповідь1","відповідь2","відповідь3","відповідь4"], "answer": 1},
        {"q": "питання3", "options": ["відповідь1","відповідь2","відповідь3","відповідь4"], "answer": 0},
        {"q": "питання4", "options": ["відповідь1","відповідь2","відповідь3","відповідь4"], "answer": 0},
        {"q": "питання5", "options": ["відповідь1","відповідь2","відповідь3","відповідь4"], "answer": 1},
        {"q": "питання6", "options": ["відповідь1","відповідь2","відповідь3","відповідь4"], "answer": 3},
        {"q": "питання7", "options": ["відповідь1","відповідь2","відповідь3","відповідь4"], "answer": 0},
        {"q": "питання8", "options": ["відповідь1","відповідь2","відповідь3","відповідь4"], "answer": 2},
        {"q": "питання9", "options": ["відповідь1","відповідь2","відповідь3","відповідь4"], "answer": 1},
        {"q": "питання10", "options": ["відповідь1","відповідь2","відповідь3","відповідь4"], "answer": 0},
    ],
    "категорія 3": [
        {"q": "питання1", "options": ["відповідь1","відповідь2","відповідь3","відповідь4"], "answer": 2},
        {"q": "питання2", "options": ["відповідь1","відповідь2","відповідь3","відповідь4"], "answer": 1},
        {"q": "питання3", "options": ["відповідь1","відповідь2","відповідь3","відповідь4"], "answer": 0},
        {"q": "питання4", "options": ["відповідь1","відповідь2","відповідь3","відповідь4"], "answer": 0},
        {"q": "питання5", "options": ["відповідь1","відповідь2","відповідь3","відповідь4"], "answer": 1},
        {"q": "питання6", "options": ["відповідь1","відповідь2","відповідь3","відповідь4"], "answer": 3},
        {"q": "питання7", "options": ["відповідь1","відповідь2","відповідь3","відповідь4"], "answer": 0},
        {"q": "питання8", "options": ["відповідь1","відповідь2","відповідь3","відповідь4"], "answer": 2},
        {"q": "питання9", "options": ["відповідь1","відповідь2","відповідь3","відповідь4"], "answer": 1},
        {"q": "питання10", "options": ["відповідь1","відповідь2","відповідь3","відповідь4"], "answer": 0},
    ]
}

# Клас кнопки
class Button:
    def __init__(self, rect, text, color=BLUE, text_color=WHITE):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.color = color
        self.text_color = text_color
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        txt = font_button.render(self.text, True, self.text_color)
        txt_rect = txt.get_rect(center=self.rect.center)
        surface.blit(txt, txt_rect)
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Гра
def main():
    state = "theme"  # theme, quiz, result
    selected_theme = None
    question_index = 0
    score = 0

    # Кнопки тем
    theme_buttons = []
    for i, t in enumerate(themes):
        theme_buttons.append(Button((WIDTH//2-100, 150 + i*100, 200, 50), t))

    # Кнопки відповідей (2x2)
    answer_buttons = []
    btn_width, btn_height = 250, 50
    gap_x, gap_y = 50, 20  # відстань між кнопками
    start_x = WIDTH // 2 - btn_width - gap_x // 2
    start_y = 300

    for row in range(2):
        for col in range(2):
            x = start_x + col * (btn_width + gap_x)
            y = start_y + row * (btn_height + gap_y)
            answer_buttons.append(Button((x, y, btn_width, btn_height), ""))

    running = True
    while running:
        screen.fill(BLACK)
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if state == "theme":
                    for i, btn in enumerate(theme_buttons):
                        if btn.is_clicked((mx,my)):
                            selected_theme = themes[i]
                            state = "quiz"
                            question_index = 0
                elif state == "quiz":
                    q = questions[selected_theme][question_index]
                    for i, btn in enumerate(answer_buttons):
                        if btn.is_clicked((mx,my)):
                            if i == q["answer"]:
                                score += 100
                            question_index += 1
                            if question_index >= len(questions[selected_theme]):
                                state = "result"

        # Малювання
        if state == "theme":
            title = font_question.render("Оберіть тему:", True, WHITE)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
            for btn in theme_buttons:
                btn.draw(screen)
        elif state == "quiz":
            q = questions[selected_theme][question_index]
            # Питання
            question_txt = font_question.render(q["q"], True, YELLOW)
            screen.blit(question_txt, (WIDTH//2 - question_txt.get_width()//2, 50))
            # Кнопки відповідей
            for i, btn in enumerate(answer_buttons):
                btn.text = q["options"][i]
                btn.draw(screen)
            # Показати номер питання
            q_num = font_score.render(f"Питання {question_index+1}/10", True, WHITE)
            screen.blit(q_num, (WIDTH-150, 10))
            # Поточний рахунок
            s_txt = font_score.render(f"Гроші: {score} грн", True, GREEN)
            screen.blit(s_txt, (10, 10))
        elif state == "result":
            res_txt = font_question.render(f"Ви заробили {score} грн!", True, YELLOW)
            screen.blit(res_txt, (WIDTH//2 - res_txt.get_width()//2, HEIGHT//2 - 50))
            retry_txt = font_button.render("Натисніть мишку щоб почати знову", True, WHITE)
            screen.blit(retry_txt, (WIDTH//2 - retry_txt.get_width()//2, HEIGHT//2 + 20))
            if event.type == pygame.MOUSEBUTTONDOWN:
                state = "theme"

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
