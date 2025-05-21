import pygame
import sys
import random
import os

# 初期化
pygame.init()

# 画面設定
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("タイピングゲーム")

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
PURPLE = (128, 0, 128)

# フォント設定
font_large = pygame.font.SysFont(None, 48)
font_medium = pygame.font.SysFont(None, 36)
font_small = pygame.font.SysFont(None, 24)
font_boss = pygame.font.SysFont(None, 60)

# 敵のイメージを作成する関数
def create_enemy_image(word, color, size=40):
    # 単語に基づいた簡単な絵を描画
    surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
    
    if "python" in word.lower():
        # Pythonのヘビのような形
        pygame.draw.lines(surf, color, False, [(0, size), (size/2, size/2), (size, size), (size*1.5, size/2)], 5)
        # 目
        pygame.draw.circle(surf, WHITE, (size*1.5, size/2), 5)
    elif "game" in word.lower():
        # ゲームコントローラーのような形
        pygame.draw.rect(surf, color, (size/2, size/2, size, size/2), border_radius=5)
        pygame.draw.circle(surf, WHITE, (size/2 + 10, size/2 + 10), 5)
        pygame.draw.circle(surf, WHITE, (size*1.5 - 10, size/2 + 10), 5)
    elif "code" in word.lower() or "program" in word.lower():
        # コードのような形（<>記号）
        pygame.draw.line(surf, color, (size/2, size/2), (size/4, size), 3)
        pygame.draw.line(surf, color, (size/4, size), (size/2, size*1.5), 3)
        pygame.draw.line(surf, color, (size*1.5, size/2), (size*1.75, size), 3)
        pygame.draw.line(surf, color, (size*1.75, size), (size*1.5, size*1.5), 3)
    elif "typing" in word.lower():
        # キーボードのような形
        pygame.draw.rect(surf, color, (size/2, size, size, size/2), border_radius=3)
        for i in range(3):
            pygame.draw.rect(surf, WHITE, (size/2 + 10 + i*20, size + 5, 15, 15), 1)
    else:
        # デフォルトの形（円）
        pygame.draw.circle(surf, color, (size, size), size/2)
        pygame.draw.circle(surf, (color[0]//2, color[1]//2, color[2]//2), (size, size), size/3)
    
    return surf

# ボスのイメージを作成する関数
def create_boss_image(word, color, size=80):
    surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
    
    # ボスの基本形状（大きな円）
    pygame.draw.circle(surf, color, (size, size), size/1.5)
    
    # 王冠のような形
    points = [(size/2, size/2), (size*0.7, size/4), (size, size/2), (size*1.3, size/4), (size*1.5, size/2)]
    pygame.draw.polygon(surf, GOLD, points)
    
    # 目
    eye_color = RED
    pygame.draw.circle(surf, eye_color, (size*0.7, size*0.7), size/10)
    pygame.draw.circle(surf, eye_color, (size*1.3, size*0.7), size/10)
    
    # 口
    mouth_points = [(size*0.7, size*1.2), (size, size*1.3), (size*1.3, size*1.2)]
    pygame.draw.polygon(surf, BLACK, mouth_points)
    
    return surf

# ゲーム変数
class Enemy:
    def __init__(self):
        self.word = random.choice(["python", "pygame", "typing", "game", "code", "program"])
        self.x = random.randint(50, WIDTH - 100)
        self.y = 50
        self.speed = 1
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.is_boss = False
        self.image = create_enemy_image(self.word, self.color)
        
    def draw(self):
        # 敵の絵を描画
        screen.blit(self.image, (self.x - self.image.get_width()//2, self.y - 50))
        
        # 単語を描画
        text = font_medium.render(self.word, True, self.color)
        screen.blit(text, (self.x, self.y))
        
    def move(self):
        self.y += self.speed
        
    def is_out(self):
        return self.y > HEIGHT - 50

class Boss(Enemy):
    def __init__(self):
        super().__init__()
        self.word = random.choice(["algorithm", "programming", "developer", "javascript", "framework"])
        self.x = WIDTH // 2 - 100
        self.y = 50
        self.speed = 0.5
        self.color = GOLD
        self.health = 3
        self.is_boss = True
        self.image = create_boss_image(self.word, self.color)
        self.pulse = 0
        self.pulse_dir = 1
        
    def draw(self):
        # ボスの体力表示
        health_text = font_small.render(f"HP: {self.health}", True, RED)
        screen.blit(health_text, (self.x, self.y - 30))
        
        # 脈動エフェクト
        self.pulse += 0.05 * self.pulse_dir
        if self.pulse > 1.0:
            self.pulse = 1.0
            self.pulse_dir = -1
        elif self.pulse < 0.0:
            self.pulse = 0.0
            self.pulse_dir = 1
            
        # ボスの絵を描画（少し大きく）
        scaled_image = pygame.transform.scale(self.image, 
                                             (int(self.image.get_width() * (1 + self.pulse * 0.1)), 
                                              int(self.image.get_height() * (1 + self.pulse * 0.1))))
        screen.blit(scaled_image, (self.x - scaled_image.get_width()//2, self.y - 80))
        
        # ボスの単語表示（通常の敵より大きく表示）
        text = font_boss.render(self.word, True, self.color)
        screen.blit(text, (self.x, self.y))
        
        # ボスの周りに輝きエフェクト
        pygame.draw.circle(screen, PURPLE, (self.x + text.get_width() // 2, self.y + text.get_height() // 2), 
                          text.get_width() // 2 + 10 + self.pulse * 5, 2)

# ゲーム状態
score = 0
defeated_enemies = 0
current_input = ""
enemies = [Enemy()]
spawn_timer = 0
game_over = False
boss_appeared = False
boss_defeated = False

# メインループ
clock = pygame.time.Clock()
while True:
    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    current_input = current_input[:-1]
                elif event.key == pygame.K_RETURN:
                    # 入力確定
                    for enemy in enemies[:]:
                        if current_input.lower() == enemy.word.lower():
                            if enemy.is_boss:
                                enemy.health -= 1
                                if enemy.health <= 0:
                                    enemies.remove(enemy)
                                    score += len(enemy.word) * 30
                                    boss_defeated = True
                            else:
                                enemies.remove(enemy)
                                score += len(enemy.word) * 10
                                defeated_enemies += 1
                                
                                # 10体倒したらボス出現
                                if defeated_enemies % 10 == 0 and not boss_appeared:
                                    boss = Boss()
                                    enemies.append(boss)
                                    boss_appeared = True
                            break
                    current_input = ""
                elif event.unicode.isprintable():
                    current_input += event.unicode
    
    if game_over:
        # ゲームオーバー画面
        screen.fill(BLACK)
        game_over_text = font_large.render("GAME OVER", True, RED)
        score_text = font_medium.render(f"Score: {score}", True, WHITE)
        restart_text = font_small.render("Press R to restart", True, WHITE)
        
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # リセット
            score = 0
            defeated_enemies = 0
            current_input = ""
            enemies = [Enemy()]
            spawn_timer = 0
            game_over = False
            boss_appeared = False
            boss_defeated = False
    else:
        # ゲーム更新
        screen.fill(BLACK)
        
        # ボス撃破メッセージ表示
        if boss_defeated:
            boss_text = font_large.render("BOSS DEFEATED!", True, GOLD)
            screen.blit(boss_text, (WIDTH//2 - boss_text.get_width()//2, HEIGHT//2 - 100))
            boss_defeated = False
            boss_appeared = False
        
        # 敵の更新
        for enemy in enemies[:]:
            enemy.move()
            enemy.draw()
            
            if enemy.is_out():
                game_over = True
        
        # 新しい敵の生成（ボスが出現中は新しい敵は出さない）
        if not any(enemy.is_boss for enemy in enemies):
            spawn_timer += 1
            if spawn_timer >= 180:  # 約3秒ごと
                enemies.append(Enemy())
                spawn_timer = 0
        
        # UI描画
        score_text = font_small.render(f"Score: {score}", True, WHITE)
        enemies_text = font_small.render(f"Defeated: {defeated_enemies}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(enemies_text, (10, 40))
        
        input_text = font_medium.render(current_input, True, GREEN)
        pygame.draw.rect(screen, WHITE, (WIDTH//2 - 150, HEIGHT - 50, 300, 40), 2)
        screen.blit(input_text, (WIDTH//2 - input_text.get_width()//2, HEIGHT - 45))
    
    # 画面更新
    pygame.display.flip()
    clock.tick(60)
