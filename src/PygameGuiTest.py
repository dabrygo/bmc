import pygame
import pygame_gui



pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager(
    (800, 600), 
    theme_path="rsc/PygameGuiTestTheme.json"
)

class ScoreBox:
    BOX_SIZE = 100

    def __init__(self, label, increment_rule, position):
        self._label = label
        self._tally = 0
        self._increment_rule = increment_rule
        self._position = position
        self._gui_element = pygame_gui.elements.UITextBox(
            html_text=self._text(),
            relative_rect=pygame.Rect(
                self._position,
                (ScoreBox.BOX_SIZE, ScoreBox.BOX_SIZE)
            ),
            manager=manager,
            object_id=pygame_gui.core.ObjectID(
                class_id='@score_box',
                object_id=f'#score_box_{self._label.lower()}'
            )
        )

    def _text(self):
        return f"{self._label.title()}\n{self._tally:05d}"

    def increment(self):
        self._tally += 1
        text = self._text()
        self._gui_element.set_text(text)

# Game timer
clock = pygame.time.Clock()
TIMER_EVENT = pygame.USEREVENT + 1 # Define a unique custom event ID
# Set the timer to trigger every second 
MS_PER_SECOND = 1000
pygame.time.set_timer(TIMER_EVENT, millis=MS_PER_SECOND) 


box_size = 100
correct_box = ScoreBox("Correct", 0, (0, 0))
incorrect_box = ScoreBox("Incorrect", 0, (box_size, 0))
timer_box = ScoreBox("Timer", 0, (2 * box_size, 0))


#hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
#                                             text='Say Hello',
#                                             manager=manager)

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == TIMER_EVENT:
            timer_box.increment()

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()

pygame.quit()