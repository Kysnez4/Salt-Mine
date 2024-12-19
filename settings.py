import pygame

def loadim(image):
    try:
        return pygame.image.load(f'images/{image}').convert_alpha() # convert_alpha for transparency
    except pygame.error as e:
        print(f"Error loading image {image}: {e}")
        return None # Return None to handle missing images gracefully

