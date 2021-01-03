"""gui calendar to track exersize data inherits WorkoutTracker from workout_tracker"""

from workout_tracker import WorkoutTracker
from datetime import date
import pygame, os

class GuiWorkoutTracker(WorkoutTracker):
    """Uses pygame to draw a calendar and display and record exersize data"""

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    def __init__(self, filename: str = 'data.json', window_size: (int, int) = (700, 700), window_pos: (int, int) = (15, 30)):
        super().__init__(filename)
        os.environ['SDL_VIDEO_WINDOW_POS'] = f'{window_pos[0]},{window_pos[1]}'
        self.running = False
        self.window_size = window_size
        try:
            self.get_data()
            if self.data == {}:
                raise 'Data empty'
        except:
            self.new_data()
        self.scale = (self.window_size[0] / 7, self.window_size[1] / 6)
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(self.window_size)
        self.day_font = pygame.font.SysFont('Arial', int(self.window_size[1] / 23))
        self.title_font = pygame.font.SysFont('Arial', int(self.window_size[1] / 10.5))

    def quit(self):
        """close the main loop and save the data"""
        self.save_data()
        self.running = False

    def draw_cross(self, pos: (int, int), size: (int, int), width: int = 1):
        """Draw a red cross at {pos} with a size of {size} and a width of {width}"""
        pygame.draw.line(self.screen, self.RED, pos, (pos[0] + size[0], pos[1] + size[1]), width)
        pygame.draw.line(self.screen, self.RED, (pos[0], pos[1] + size[1]), (pos[0] + size[0], pos[1]), width)

    def draw_check(self, pos: (int, int), size: (int, int), width: int = 1):
        """Draw a green check at {pos} with a size of {size} and a width of {width}"""
        middle = (pos[0] + size[0] / 2, pos[1] + size[1] / 2)
        pygame.draw.line(self.screen, self.GREEN, (pos[0], middle[1]), (middle[0], pos[1] + size[1]), width)
        pygame.draw.line(self.screen, self.GREEN, (middle[0], pos[1] + size[1]), (pos[0] + size[0], pos[1]), width)

    def draw_empty_calendar(self):
        """Draw an empty calendar"""
        top_line_height = self.window_size[1] / 9
        # draw horizontal lines
        pygame.draw.line(self.screen, self.WHITE, (0, top_line_height), (self.window_size[0], top_line_height))
        for i in range(6):
            line_y = i * self.scale[1]
            pygame.draw.line(self.screen, self.WHITE, (0, line_y), (self.window_size[0], line_y))
        # draw verticle lines
        for i in range(7):
            line_x = i * self.scale[0]
            pygame.draw.line(self.screen, self.WHITE, (line_x, top_line_height), (line_x, self.window_size[1]))
        # draw weekday names
        for i, weekday in enumerate(['Sun', 'Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat']):
            text = self.day_font.render(weekday, True, self.WHITE)
            x_offset = self.scale[0] / 2 - text.get_size()[0] / 2
            self.screen.blit(text, (i * self.scale[0] + x_offset, top_line_height))
        # draw title
        current_date = date.today()
        title_string = current_date.strftime('%B %Y')
        text = self.title_font.render(title_string, True, self.WHITE)
        self.screen.blit(text, (self.window_size[0] / 2 - text.get_size()[0] / 2, 0))

    def run(self):
        """Run the main loop"""
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
            self.screen.fill(self.BLACK)
            self.draw_empty_calendar()
            pygame.display.update()

if __name__ == '__main__': # driver code
    tracker = GuiWorkoutTracker()
    tracker.run()
