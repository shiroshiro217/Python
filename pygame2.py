import pygame
import sys

def main():
    pygame.init()
    pygame.display.set_caption("顯示圖片動畫")
    screen = pygame.display.set_mode((640, 360))
    clock = pygame.time.Clock()
    img_bg = pygame.image.load("img/pg_bg.png")
    img_chara = [pygame.image.load(f"img/pg_chara{i}.png") for i in range(2)]
    tmr = 0

    while True:
        tmr += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    screen = pygame.display.set_mode((640, 360), pygame.FULLSCREEN)
                
                if event.key == pygame.K_F2 or event.key == pygame.K_SPACE:
                    screen = pygame.display.set_mode((1280, 720))
        
        x = tmr%160
        for i in range(5):
            screen.blit(img_bg, [i*160-x, 0])
        
        screen.blit(img_chara[tmr%2], [224, 160])

        pygame.display.update()
        clock.tick(5)

if __name__ == "__main__":
    main()