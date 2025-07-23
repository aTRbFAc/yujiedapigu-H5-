import pygame
import sys
import random

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

# 带派不老铁
dpblt_sound = pygame.mixer.Sound('dpblt.mp3')
dpblt_sound.set_volume(1.0)

background = pygame.image.load('background.png')
yujie_img = pygame.image.load('yujie1.png')
yujie2_img = pygame.image.load('yujie2.png')
text_image = pygame.image.load('text-image.png')
start_img = pygame.image.load('start.png')
bzy_img = pygame.image.load('bzy.png')
text_height = text_image.get_height()

width, height = background.get_size()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('带派不老铁')

# 游戏场景
current_scene = 1  # 场景
score = 0
ejaculate = 10  # 射精感

bzy_instances = []

# 挨打跳跃
yujie_jumping = False
yujie_jump_phase = "rising"
yujie_jump_offset = 0
yujie_jump_speed = 4
yujie_jump_gravity = 0.2

# 开始游戏按钮
start_x = width // 2
start_y = height // 4 + text_height
start_width, start_height = start_img.get_size()
start_rect = pygame.Rect(start_x, start_y, start_width, start_height)

# Main
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_scene == 1:
                mouse_pos = pygame.mouse.get_pos()
                if start_rect.collidepoint(mouse_pos):
                    current_scene = 2
            elif current_scene == 2:
                mouse_pos = pygame.mouse.get_pos()
                yujie2_rect = pygame.Rect(100, height - yujie2_height, yujie2_width, yujie2_height)
                bottom_third_rect = pygame.Rect(
                    yujie2_rect.x,
                    yujie2_rect.y + yujie2_rect.height * 2/3,
                    yujie2_rect.width,
                    yujie2_rect.height * 1/3
                )
                if bottom_third_rect.collidepoint(mouse_pos):
                    new_x = mouse_pos[0] - 0
                    new_y = mouse_pos[1] - 0

                    rotation_angle = random.randint(-90, 90)

                    bzy_instances.append({
                        'x': new_x,
                        'y': new_y,
                        'angle': rotation_angle,
                        'jump_offset': 0,
                        'jumping': False
                    })

                    dpblt_sound.play()
                    score += 1

                    if not yujie_jumping:
                        yujie_jumping = True
                        yujie_jump_phase = "falling"
                        yujie_jump_speed = 4
                        yujie_jump_gravity = 0.2
                        for bzy in bzy_instances:
                            bzy['jumping'] = True


    screen.blit(background, (0, 0))
    
    # 绘制不同内容
    if current_scene == 1:
        screen.blit(text_image, (width // 2, height // 4))
        text_height = text_image.get_height()
        screen.blit(start_img, (width // 2, height // 4 + text_height))
        img_width, img_height = yujie_img.get_size()
        screen.blit(yujie_img, (0, height - img_height))
    elif current_scene == 2:
        font = pygame.font.Font(None, 48)
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(score_text, (20, 20))  # 左上角位置
        
        # 更新挨打SM动画
        if yujie_jumping:
            if yujie_jump_phase == "falling":
                yujie_jump_offset += yujie_jump_speed
                yujie_jump_speed -= yujie_jump_gravity
                
                if yujie_jump_speed <= 0:
                    yujie_jump_phase = "rising"
                    
            elif yujie_jump_phase == "rising":
                yujie_jump_speed += yujie_jump_gravity
                yujie_jump_offset -= yujie_jump_speed
                
                if yujie_jump_offset <= 0:
                    yujie_jumping = False
                    yujie_jump_offset = 0
                    yujie_jump_phase = "falling"
                    yujie_jump_speed = 4
                    yujie_jump_gravity = 0.2
        
        # 更新巴掌印实例的动画
        for bzy in bzy_instances:
            if bzy['jumping']:
                if 'jump_phase' not in bzy:
                    bzy['jump_phase'] = 'falling'
                    bzy['jump_speed'] = 4
                
                if bzy['jump_phase'] == "falling":
                    bzy['jump_offset'] += bzy['jump_speed']
                    bzy['jump_speed'] -= yujie_jump_gravity
                    
                    if bzy['jump_speed'] <= 0:
                        bzy['jump_phase'] = "rising"
                else:
                    bzy['jump_speed'] += yujie_jump_gravity
                    bzy['jump_offset'] -= bzy['jump_speed']
                    
                    if bzy['jump_offset'] <= 0:
                        bzy['jumping'] = False
                        bzy['jump_offset'] = 0
                        bzy['jump_phase'] = "falling"
                        bzy['jump_speed'] = 4
        
        yujie2_width, yujie2_height = yujie2_img.get_size()
        screen.blit(yujie2_img, (100, height - yujie2_height + yujie_jump_offset))

        for bzy in bzy_instances:
            x, y, angle = bzy['x'], bzy['y'], bzy['angle']
            rotated_img = pygame.transform.rotate(bzy_img, angle)
            
            rotated_rect = rotated_img.get_rect(center=(x, y + bzy['jump_offset']))

            screen.blit(rotated_img, rotated_rect.topleft)
    pygame.display.flip()