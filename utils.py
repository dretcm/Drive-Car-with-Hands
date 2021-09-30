import pygame, sys, time

pygame.init()

def load_images(paths, size=None, bg_color=None):
        images = [pygame.image.load(img) for img in paths]
        if size:
                images = [pygame.transform.scale(img, size) for img in images]
        if bg_color:
                for img in images:
                        img.set_colorkey(bg_color)
        return images

def load_image(path, size=None, bg_color=None):
        image = pygame.image.load(path)
        if size:
                image = pygame.transform.scale(image, size)
        if bg_color:
                image.set_colorkey(bg_color)
        return image


def exit_keys(event):
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

