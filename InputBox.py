import pygame

class InputBox:
    '''
    This class is used inside the visualisation extension, to enter the x and y grid coorinates.

    The code was taken and adapted from the following source: https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame
    '''

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('lightskyblue3')
        self.text = text
        self.txt_surface = pygame.font.Font(None, 32).render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = (0,0,150) if self.active else pygame.Color('lightskyblue3') #pygame.Color('dodgerblue2')
        
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    #print(self.text)
                    output = copy.copy(self.text)
                    self.text = ''
                    #return output
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = pygame.font.Font(None, 32).render(self.text, True, self.color)
        return None

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_text(self):
    	return self.text

    def reset_text(self):
    	self.text = ''
    	self.txt_surface = pygame.font.Font(None, 32).render(self.text, True, self.color)