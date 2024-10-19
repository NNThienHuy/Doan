import pygame
import time
import random

# Khởi tạo pygame
pygame.init()

# Khởi tạo âm thanh
pygame.mixer.init()

# Định nghĩa màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)

# Kích thước cửa sổ game
WIDTH = 1000
HEIGHT = 600

# Tạo màn hình game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('SNAKE GAME')

# Kích thước và tốc độ khối rắn
snake_block = 20
snake_speed = 15

# Định dạng font chữ
font_style = pygame.font.SysFont("bahnschrift", 25)

# Ảnh của đầu rắn, thân rắn, thức ăn
head = pygame.image.load('head.png')
head = pygame.transform.scale(head, (snake_block, snake_block))
body = pygame.image.load('body.png')
body = pygame.transform.scale(body, (snake_block, snake_block))
food = pygame.image.load('food.png')
food = pygame.transform.scale(food, (snake_block, snake_block))

# Tải âm thanh
pygame.mixer.music.load('nhacnen.mp3')  # Tải nhạc nền
eat_sound = pygame.mixer.Sound('eat.mp3')  # Âm thanh khi ăn thức ăn
game_over_sound = pygame.mixer.Sound('over.mp3')  # Âm thanh kết thúc trò chơi





def diem_cuoi_cuoc(score):
    """Hiển thị điểm số hiện tại."""
    value = font_style.render("SCORE: " + str(score), True, RED)
    text_rect = value.get_rect()
    text_rect.center = (WIDTH / 2, HEIGHT / 2)
    screen.blit(value, text_rect)

def ran(snake_list):
    """Vẽ rắn trên màn hình."""
    screen.blit(head, [snake_list[0][0], snake_list[0][1]])
    for x in snake_list[1:]:
        screen.blit(body, [x[0], x[1]])

def thong_diep(msg, color):
    """Hiển thị thông điệp trên màn hình."""
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [WIDTH / 3.5, HEIGHT / 2.5])

def nhan_dau_vao(x1_change, y1_change):
    """Xử lý đầu vào từ người chơi."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return None, None  # Thoát game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and x1_change == 0:
                x1_change = -snake_block
                y1_change = 0
            elif event.key == pygame.K_RIGHT and x1_change == 0:
                x1_change = snake_block
                y1_change = 0
            elif event.key == pygame.K_UP and y1_change == 0:
                y1_change = -snake_block
                x1_change = 0
            elif event.key == pygame.K_DOWN and y1_change == 0:
                y1_change = snake_block
                x1_change = 0
    return x1_change, y1_change

def kiem_tra_va_cham_thuc_an(x1, y1, foodx, foody):
    """Kiểm tra va chạm với thức ăn.""" 
    return x1 < foodx + snake_block and x1 + snake_block > foodx and y1 < foody + snake_block and y1 + snake_block > foody

def kiem_tra_va_cham(snake_list, snake_head):
    """Kiểm tra va chạm với chính rắn.""" 
    return snake_head in snake_list[:-1]  # Kiểm tra xem đầu rắn có trong danh sách thân rắn không

def cap_nhat_thuc_an(score, obstacle_list):
    """Cập nhật vị trí thức ăn và điểm số.""" 
    global foodx, foody, length_of_snake, snake_speed

    while True:
        foodx = round(random.randrange(0, WIDTH - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, HEIGHT - snake_block) / 10.0) * 10.0
        
        # Kiểm tra va chạm với chướng ngại vật
        if not kiem_tra_va_cham_chuong_ngai_vat(foodx, foody, obstacle_list):
            break  

    length_of_snake += 1 
    score += 1  
    if score % 20 == 0:
        snake_speed += 5

    return score  



def cap_nhat_vi_tri_ran(x1, y1, x1_change, y1_change, snake_list):
    """Cập nhật vị trí rắn.""" 
    x1 += x1_change
    y1 += y1_change
    snake_head = [x1, y1]
    snake_list.append(snake_head)

    if len(snake_list) > length_of_snake:
        del snake_list[0]
        
    return x1, y1, snake_list

def ve_chuong_ngai_vat(obstacle_list):
    """Vẽ các chướng ngại vật lên màn hình."""
    for obstacle in obstacle_list:
        pygame.draw.rect(screen, GREEN, [obstacle[0], obstacle[1], snake_block, snake_block])

def tao_chuong_ngai_vat():
    """Tạo danh sách các vị trí chướng ngại vật theo dạng bức tường."""
    obstacle_list = []
    x_start = 200  
    y_start = 150  
    wall_length = 15  
    wall_Height = 25
    for i in range(wall_length):
        obstacle_list.append([x_start, y_start + i * snake_block])  
    for i in range(wall_Height):
        obstacle_list.append([x_start + i * snake_block, y_start])
    for i in range(wall_length): # Cái này test chướng ngại vật , xóa đi cũng được
        obstacle_list.append([x_start + i * snake_block , y_start + i * snake_block])
    return obstacle_list

def kiem_tra_va_cham_chuong_ngai_vat(x1, y1, obstacle_list):
    for obstacle in obstacle_list:
        if (x1 < obstacle[0] + snake_block and x1 + snake_block > obstacle[0] and y1 < obstacle[1] + snake_block and y1 + snake_block > obstacle[1]):
            return True  
    return False

def gameLoop():
    global foodx, foody, length_of_snake, snake_speed  

    game_over = False
    game_close = False

    x1 = WIDTH / 2
    y1 = HEIGHT / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1


    foodx = round(random.randrange(0, WIDTH - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, HEIGHT - snake_block) / 10.0) * 10.0

    score = 0
    clock = pygame.time.Clock()

    obstacle_list = tao_chuong_ngai_vat()

    while not game_over:

        while game_close:
            screen.fill(BLACK)
            diem_cuoi_cuoc(score)
            thong_diep("Nhấn C để Chơi Lại hoặc Q để Thoát", RED)
            pygame.draw.rect(screen,GREEN,(275,200,200,90))
            pygame.draw.rect(screen,GREEN,(550,200,200,90))
            pygame.draw.rect(screen,RED,(410,300,200,90))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()  # Gọi lại gameLoop
    
        # Nhận đầu vào từ người chơi
        x1_change, y1_change = nhan_dau_vao(x1_change, y1_change)
        if x1_change is None and y1_change is None:
            game_over = True  

        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

  
        x1, y1, snake_list = cap_nhat_vi_tri_ran(x1, y1, x1_change, y1_change, snake_list)

        if kiem_tra_va_cham_chuong_ngai_vat(x1, y1, obstacle_list):
            game_close = True  

        screen.fill(BLACK)  
        ve_chuong_ngai_vat(obstacle_list)  
        screen.blit(food, [foodx, foody]) 
        
       
        if kiem_tra_va_cham(snake_list, snake_list[-1]):
            game_close = True 

        ran(snake_list)  

        if kiem_tra_va_cham_thuc_an(x1, y1, foodx, foody):
            score = cap_nhat_thuc_an(score, obstacle_list)  
            eat_sound.play()  

        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()
