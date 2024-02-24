import pygame, sys
from time import sleep

rgb_colors = [
    (255, 0, 0),  # Red
    (255, 69, 0),  # Orange Red
    (255, 165, 0),  # Orange
    (255, 192, 203),  # Pink
    (255, 0, 255),  # Magenta
    (138, 43, 226),  # Blue Violet
    (0, 0, 255),  # Blue
    (0, 128, 128),  # Teal
    (0, 255, 255),  # Cyan
    (0, 255, 127),  # Spring Green
    (0, 128, 0),  # Dark Green
    (128, 128, 0),  # Olive
    (128, 0, 128),  # Purple
    (106, 90, 205),  # Slate Blue
    (135, 206, 235),  # Sky Blue
    (0, 255, 0),  # Green
    (128, 0, 0),  # Maroon
    (255, 255, 0),  # Yellow
]

pygame.init()

# Display surface
width, height = 700, 500
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Ibrahim's Pong Game")
pygame.display.set_icon(pygame.image.load("Graphics/Pictures/wizardjump4.png"))

fps = 60
ball_radius = 8
winning_score = 10
paddle_width, paddle_height = 15, 100
score_font = pygame.font.Font("Graphics/Fonts/flappyfont.ttf", 40)

player1 = "1"  # input("Player 1: ").strip().upper()
player2 = "2"  # input("Player 2: ").strip().upper()

if len(player1) < 3 or len(player2) < 3:
    player1 = "LEFT PLAYER"
    player2 = "RIGHT PLAYER"


class Paddle:
    vel = 4

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, screen):
        pygame.draw.rect(
            screen, (255, 255, 255), (self.x, self.y, self.width, self.height)
        )

    def move(self, up=True):
        if up:
            self.y -= self.vel
        else:
            self.y += self.vel

    # Reset the paddles at center
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


class Ball:
    max_vel = 6

    def __init__(self, x, y, radius, rgb_colors):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.max_vel
        self.y_vel = 0
        self.rgb_colors = rgb_colors
        self.color_index = 0

    def draw(self, screen):
        color = self.rgb_colors[self.color_index]
        pygame.draw.circle(screen, color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    # Reset the ball at center
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1


def draw(screen, paddles, ball, left_score, right_score):
    screen.fill("#040622")

    right_score_text = score_font.render(str(right_score), 0, (255, 255, 255))
    left_score_text = score_font.render(str(left_score), 0, (255, 255, 255))

    screen.blit(left_score_text, (width // 4 - left_score_text.get_width() // 2, 20))
    screen.blit(
        right_score_text, (width * (3 / 4) - right_score_text.get_width() // 2, 20)
    )

    for paddle in paddles:
        paddle.draw(screen)

    # Dashed line
    for i in range(10, height, height // 20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(screen, (255, 255, 255), (width // 2 - 3, i, 6, height // 20))

    ball.draw(screen)

    pygame.display.update()


# Collision
def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= height or ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    # Check for collision with paddles
    # Right
    if ball.x_vel < 0:
        if left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = left_paddle.height / (2 * ball.max_vel)
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -y_vel

    # Left
    else:
        if right_paddle.y <= ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = right_paddle.height / (2 * ball.max_vel)
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -y_vel


# Key presses/movement
def press_keys(keys, left_paddle, right_paddle):
    # left
    if keys[pygame.K_w] and left_paddle.y - left_paddle.vel >= 0:
        left_paddle.move(up=True)
    if (
        keys[pygame.K_s]
        and left_paddle.y + left_paddle.vel + left_paddle.height <= height
    ):
        left_paddle.move(up=False)

    # right
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.vel >= 0:
        right_paddle.move(up=True)
    if (
        keys[pygame.K_DOWN]
        and right_paddle.y + right_paddle.vel + right_paddle.height <= height
    ):
        right_paddle.move(up=False)


# Game loop
def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(
        10, height // 2 - paddle_height // 2, paddle_width, paddle_height
    )
    right_paddle = Paddle(
        width - paddle_width - 10,
        height // 2 - paddle_height // 2,
        paddle_width,
        paddle_height,
    )

    ball = Ball(width // 2, height // 2, ball_radius, rgb_colors)

    left_score = 0
    right_score = 0

    color_change_interval = 2  # Change color every 2 seconds
    last_color_change_time = pygame.time.get_ticks()

    while run:
        clock.tick(fps)

        draw(screen, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        press_keys(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        # Score
        if ball.x < 0:
            ball.x -= 5
            right_score += 1
            ball.reset()
        elif ball.x > width:
            ball.y = ball.y - 5
            left_score += 1
            ball.reset()

        won = False
        if left_score >= winning_score:
            won = True
            win_text = f"{player1} WINS!"
        elif right_score >= winning_score:
            won = True
            win_text = f"{player2} WINS!"

        if won:
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            text = score_font.render(win_text, 1, "green")
            text_rect = text.get_rect(
                topleft=(
                    width // 2 - text.get_width() // 2,
                    height // 2 - text.get_height() // 2,
                )
            )
            screen.blit(text, text_rect)
            pygame.display.update()
            pygame.time.delay(5000)
            left_score = 0
            right_score = 0

        # Color changing logic
        current_time = pygame.time.get_ticks()
        if (current_time - last_color_change_time) / 1000 >= color_change_interval:
            ball.color_index = (ball.color_index + 1) % len(rgb_colors)
            last_color_change_time = current_time

    pygame.quit()


if __name__ == "__main__":
    main()
