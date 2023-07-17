#!/usr/bin/env python3

"""gui calendar to track exersize data inherits WorkoutTracker from workout_tracker"""

from workout_tracker import WorkoutTracker
from datetime import date
import pygame, os

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class GuiWorkoutTracker(WorkoutTracker):
    """Uses pygame to draw a calendar and display and record exersize data"""

    def __init__(self, filename: str = 'data.json', window_size: (int, int) = (700, 700), window_pos: (int, int) = (15, 30)):
        super().__init__(filename)
        os.environ['SDL_VIDEO_WINDOW_POS'] = f'{window_pos[0]},{window_pos[1]}'
        self.running = False
        self.window_size = window_size
        try:
            self.get_data()
            if self.data == {}:
                raise RuntimeError('Data empty')
        except:
            self.new_data()
        self.scale = (self.window_size[0] / 7, self.window_size[1] / 7)
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(self.window_size)
        self.day_font = pygame.font.SysFont('Arial', int(self.window_size[1] / 23))
        self.title_font = pygame.font.SysFont('Arial', int(self.window_size[1] / 12))
        self.corner_number_font = pygame.font.SysFont('Arial', int(self.window_size[1]/ 35))
        self.selected_date = date.today()
        self.saved = True

    def quit(self):
        """close the main loop and save the data"""
        self.save_data()
        self.running = False

    def draw_cross(self, pos: (int, int), size: (int, int), width: int = 1):
        """Draw a red cross at {pos} with a size of {size} and a width of {width}"""
        pygame.draw.line(self.screen, RED, pos, (pos[0] + size[0], pos[1] + size[1]), width)
        pygame.draw.line(self.screen, RED, (pos[0], pos[1] + size[1]), (pos[0] + size[0], pos[1]), width)

    def draw_check(self, pos: (int, int), size: (int, int), width: int = 1):
        """Draw a green check at {pos} with a size of {size} and a width of {width}"""
        middle = (pos[0] + size[0] / 2, pos[1] + size[1] / 2)
        pygame.draw.line(self.screen, GREEN, (pos[0], middle[1]), (middle[0], pos[1] + size[1]), width)
        pygame.draw.line(self.screen, GREEN, (middle[0], pos[1] + size[1]), (pos[0] + size[0], pos[1]), width)

    def draw_saved(self):
        """Draw in the top right corner whether or not the changes have been saved"""
        padding = 10
        r = self.window_size[1] / 21 - padding
        pos = (self.window_size[0] - r - padding, r + padding)
        if self.saved:
            color = GREEN
            draw_fn = self.draw_check
        else:
            color = RED
            draw_fn = self.draw_cross
        draw_fn((pos[0] - r / 2 - 1, pos[1] - r / 2), (r, r), 4)
        pygame.draw.circle(self.screen, color, pos, r, 2)

    def draw_empty_calendar(self):
        """Draw an empty calendar"""
        top_line_height = self.window_size[1] / 10.5
        # draw horizontal lines
        pygame.draw.line(self.screen, WHITE, (0, top_line_height), (self.window_size[0], top_line_height))
        for i in range(7):
            line_y = i * self.scale[1]
            pygame.draw.line(self.screen, WHITE, (0, line_y), (self.window_size[0], line_y))
        # draw verticle lines
        for i in range(7):
            line_x = i * self.scale[0]
            pygame.draw.line(self.screen, WHITE, (line_x, top_line_height), (line_x, self.window_size[1]))
        # draw weekday names
        for i, weekday in enumerate(['Sun', 'Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat']):
            text = self.day_font.render(weekday, True, WHITE)
            x_offset = self.scale[0] / 2 - text.get_size()[0] / 2
            self.screen.blit(text, (i * self.scale[0] + x_offset, top_line_height))
        # draw title
        title_string = self.selected_date.strftime('%B %Y')
        text = self.title_font.render(title_string, True, WHITE)
        self.screen.blit(text, (self.window_size[0] / 2 - text.get_size()[0] / 2, 0))

    def keyboard_input(self, key: int):
        """Handle keyboard input"""
        if key == pygame.K_RIGHT or key == pygame.K_LEFT:
            new_year = self.selected_date.year
            new_month = self.selected_date.month + (1 if key == pygame.K_RIGHT else -1)
            if new_month < 1:
                new_month += 12
                new_year -= 1
                if new_year == 2020:
                    new_month = 1
                    new_year = 2021
            if new_month > 12:
                new_month -= 12
                new_year += 1
            try:
                self.selected_date = self.selected_date.replace(new_year, new_month)
            except:
                self.selected_date = self.selected_date.replace(new_year, new_month, 1)
        elif key == pygame.K_SPACE:
            self.toggle_day(date.today().isoformat())
        elif key == pygame.K_q or key == pygame.K_ESCAPE:
            self.quit()
        elif key == pygame.K_s:
            self.save_data()

    def save_data(self):
        """Save data to file and reset save flag"""
        super().save_data()
        self.saved = True

    def toggle_day(self, day: str):
        """Toggle a day and change if saved flag"""
        super().toggle_day(day)
        self.saved = False

    def mouse_input(self):
        """Handle mouse input"""
        pos = pygame.mouse.get_pos()
        if pos[1] > self.scale[1]:
            real_pos = self.window_to_calendar(pos)
            day = self.days[real_pos[1]][real_pos[0]]
            if day != None:
                self.toggle_day(day)

    def calendar_to_window(self, pos: (int, int)) -> (int, int):
        """Takes an input in coordinates of what box is selected and translates that into pixel coordinates"""
        return pos[0] * self.scale[0], (pos[1] + 1) * self.scale[1]

    def window_to_calendar(self, pos: (int, int)) -> (int, int):
        """Takes an input in coordinates of pixel coordinates and translates that into what box is selected"""
        return int(pos[0] / self.scale[0]), int(pos[1] / self.scale[1]) - 1

    def draw_days(self):
        """Draw the contents of the calendar"""
        self.days = [[None for i in range(7)] for j in range(6)]
        current_x = current_y = 0
        corner_offset = (3, 0)
        pos_offset = (22, 22)
        size_offset = (pos_offset[0] * 2, pos_offset[1] * 2)
        today = date.today()
        no_days = True
        for key, val in self.data.items():
            d = date.fromisoformat(key)
            if d.year == self.selected_date.year and d.month == self.selected_date.month:
                no_days = False
                while d.isoweekday() % 7 != current_x:
                    current_x += 1
                real_pos = self.calendar_to_window((current_x, current_y))
                corner_number = self.corner_number_font.render(str(d.day), True, WHITE)
                self.screen.blit(corner_number, (real_pos[0] + corner_offset[0], real_pos[1] + corner_offset[1]))
                if d <= today:
                    self.days[current_y][current_x] = key
                    draw_func = self.draw_check if val else self.draw_cross
                    draw_func((real_pos[0] + pos_offset[0], real_pos[1] + pos_offset[1]), (self.scale[0] - size_offset[0], self.scale[1] - size_offset[1]), 10)
                # text = self.get_split_text(d.isoweekday())
                # self.screen.blit(text, (real_pos[0] + self.scale[0] / 15, real_pos[1] + self.scale[1] * 0.75))
                current_x += 1
                if current_x > 6:
                    current_x = 0
                    current_y += 1
        if no_days:
            self.new_month(self.selected_date.month, self.selected_date.year)

    def draw_streak(self):
        streak = 0
        today = date.today()
        for key, val in self.data.items():
            if date.fromisoformat(key) > today:
                break
            if val:
                streak += 1
            else:
                streak = 0
        self.screen.blit(self.day_font.render(f'Streak: {streak}', True, WHITE), (10, 10))

    def get_split_text(self, day: int) -> pygame.Surface:
        '''
        :day: int, the number corresponding to the day of the week e.g. 1 = monday, 2 = tuesday, ..., 6 = saturday, 7 = sunday
        '''
        s = 'Full Body' if day in (1, 3, 5) else 'Cardio'
        # s = [
        #     '', # First is blank because 0 is not an isoweekday
        #     'Push',
        #     'Pull',
        #     'Legs',
        #     'Push',
        #     'Pull',
        #     'Legs',
        #     'Rest'
        # ][day]
        return self.corner_number_font.render(s, True, WHITE)

    def run(self):
        """Run the main loop"""
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    self.keyboard_input(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_input()
            self.screen.fill(BLACK)
            self.draw_empty_calendar()
            self.draw_days()
            self.draw_streak()
            self.draw_saved()
            pygame.display.update()

if __name__ == '__main__': # driver code
    tracker = GuiWorkoutTracker(os.environ.get('WORKOUT_DATA_PATH', 'data.json'))
    tracker.run()
