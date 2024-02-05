import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 120, 25
BALL_SIZE = 20
BRICK_WIDTH, BRICK_HEIGHT = 80, 30
BRICK_ROWS, BRICK_COLS = 5, 10
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BRICK_COLORS = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
    (255, 0, 255), (0, 255, 255), (128, 128, 128), (255, 165, 0),
    (255, 192, 203), (0, 128, 0)
]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cyber Bricks")

background = pygame.image.load("background2.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

paddle_image = pygame.image.load("paddle_image.png")
paddle_image = pygame.transform.scale(paddle_image, (PADDLE_WIDTH, PADDLE_HEIGHT))

brick_image = pygame.image.load("brick_image.png")
brick_image = pygame.transform.scale(brick_image, (BRICK_WIDTH, BRICK_HEIGHT))

ball_surface = pygame.Surface((BALL_SIZE, BALL_SIZE), pygame.SRCALPHA)
pygame.draw.ellipse(ball_surface, (255, 255, 255, 128), ball_surface.get_rect())
ball_image = pygame.transform.scale(ball_surface, (BALL_SIZE, BALL_SIZE))

paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

bricks = []
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLS):
        brick = pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT)
        bricks.append(brick)
ball_speed = [random.choice([-5, 5]), -5]

score = 0
level = 1
brick_color = WHITE
font = pygame.font.Font(None, 36)
MENU = 0
PLAYING = 1
game_state = MENU
sparks = []
def create_spark(x, y):
    return {'rect': pygame.Rect(x, y, random.randint(3, 8), random.randint(3, 8)), 'color': (255, 255, 255)}
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if game_state == MENU and event.key == pygame.K_RETURN:
                game_state = PLAYING
            elif game_state == PLAYING and event.key == pygame.K_r:
                paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT)
                ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
                brick_color = random.choice(BRICK_COLORS)
                bricks = [pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT) for row in range(BRICK_ROWS) for col in range(BRICK_COLS)]
                ball_speed = [random.choice([-5, 5]), -5]
                score = 0
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_p:
                game_state = MENU if game_state == PLAYING else PLAYING

    keys = pygame.key.get_pressed()
    if game_state == PLAYING:
        if not bricks:
            level += 1
            brick_color = random.choice(BRICK_COLORS) if level > 1 else WHITE
            bricks = [pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT) for row in range(BRICK_ROWS) for col in range(BRICK_COLS)]
            print(f"Level {level}")

        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.x -= 7
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.x += 7

        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        if ball.top <= 0:
            ball_speed[1] = -ball_speed[1]
        elif ball.right >= WIDTH or ball.left <= 0:
            ball_speed[0] = -ball_speed[0]

        if ball.colliderect(paddle) and ball_speed[1] > 0:
            ball_speed[1] = -ball_speed[1]

            for _ in range(20):
                sparks.append(create_spark(ball.centerx, ball.centery))

        bricks_copy = bricks.copy()
        for brick in bricks_copy:
            if ball.colliderect(brick):
                ball_speed[1] = -ball_speed[1]
                bricks.remove(brick)
                score += len(bricks_copy) - len(bricks)

                for _ in range(10):
                    sparks.append(create_spark(brick.centerx, brick.centery))

    sparks = [{'rect': spark['rect'].move(5, 5), 'color': spark['color']} for spark in sparks]
    sparks = [spark for spark in sparks if spark['rect'].left < WIDTH and spark['rect'].top < HEIGHT]
    screen.blit(background, (0, 0))

    if game_state == MENU:
        menu_text = font.render("Press Enter to Start", True, WHITE)
        menu_rect = menu_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(menu_text, menu_rect)
    elif game_state == PLAYING:
        screen.blit(paddle_image, (paddle.x, paddle.y))
        screen.blit(ball_image, (ball.x, ball.y))

        for brick in bricks:
            screen.blit(brick_image, (brick.x, brick.y))

        for spark in sparks:
            pygame.draw.rect(screen, spark['color'], spark['rect'])

        score_text = font.render(str(score), True, (0, 255, 0))
        score_rect = score_text.get_rect(topright=(WIDTH - 10, 10))
        screen.blit(score_text, score_rect)

    pygame.display.flip()
    pygame.time.Clock().tick(FPS)
