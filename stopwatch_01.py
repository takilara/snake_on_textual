# import logging
from time import monotonic

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.widgets import Button, Static, Log, Placeholder
from textual.containers import Center
from textual.reactive import reactive
#from textual.logging import TextualHandler
from textual import log

# logging.basicConfig(
#     level="DEBUG",
#     handlers=[TextualHandler()],
# )

class ElapsedTime(Static):
    """A widget to represent the elapsed time."""
    start_time = reactive(monotonic)
    time = reactive(0.0)
                    
    def on_mount(self) -> None:
        self.set_interval(0.1, self.update_time)
    
    def update_time(self) -> None:
        self.time = monotonic() - self.start_time
    
    def watch_time(self, time: float) -> None:
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{hours:02,.0f}:{minutes:02.0f}:{seconds:05.2f}")

class Metrics(Static):
    length = reactive(2)
    
    score = reactive(0)
    x = reactive(0)
    y = reactive(0)

    def update_length(self, length: int) -> None:
        self.length = length

    def update_position(self, pos: tuple) -> None:
        self.x= pos[0]
        self.y = pos[1]

    def watch_length(self, length: int) -> None:
        self.update_status_view()
    
    def watch_x(self, x: int) -> None:
        self.update_status_view()
    def watch_y(self, y: int) -> None:
        self.update_status_view()

    def update_status_view(self):
        lines = [
            f"Length: {self.length}",
            f"X,Y: ({self.x},{self.y})",
        ]
        self.update("\n".join(lines))
    
class StatusWindow(Static):
    # how do i give it a frame? CSS?
    m = Metrics()

    def update_length(self, length: int) -> None:
        self.m.update_length(length)

    def update_position(self, pos: tuple) -> None:
        self.m.update_position(pos)

    def compose(self) -> ComposeResult:
        yield ElapsedTime()
        yield self.m

class SnakeHead(Static):
    """A widget to represent the head of the snake."""

    x = reactive(50)
    y = reactive(50)

    def update_position(self, pos: tuple) -> None:
        self.x= pos[0]
        self.y = pos[1]

    def compose(self) -> ComposeResult:
        """Create child widgets for the head."""
        yield Static("🐍")
    pass

class SnakeBody(Static):
    """A widget to represent the body of the snake."""
    def compose(self) -> ComposeResult:
        
        yield Static("o")
    pass

class Snake(Static):
    """A widget to represent the snake."""
    head = SnakeHead()

    def update_position(self, pos: tuple) -> None:
        self.head.update_position(pos)

    def compose(self) -> ComposeResult:
        """Create child widgets for the snake."""
        yield self.head
        yield SnakeBody()
        
class PlayArea(Static):
    number_of_rows = 2
    number_of_columns = 2

    

#     CSS = """
# PlayArea { 
#     height: 1fr;
#     border: solid green;
#     layout: grid;
#     grid-size: 5 5;
# }
# """
    def update_size(self):
        log.info("Play Area size after ready:")
        log.info(self.size)

        placeholders = self.query(Placeholder)
        if placeholders:
            for placeholder in placeholders:
                placeholder.remove()


        self.number_of_columns = self.size.width //4
        self.number_of_rows = self.size.height  //4

        self.styles.grid_size_rows = self.number_of_rows
        self.styles.grid_size_columns = self.number_of_columns
        self.styles.grid_gutter_vertical = 0
        self.styles.grid_gutter_horizontal = 0
        
        #self.styles.border = "solid","blue"
        self.g = []

        for row in range(self.number_of_rows):
            the_row = []
            for col in range(self.number_of_columns):
                c = GridCell(row,col)
                the_row.append(c)
                self.mount(c)
            self.g.append(the_row)

    
    def make_active(self,pos):
        #cell = self.query_one(f"cell-{pos[0]}-{pos[1]}")
        cell = self.g[pos[1]][pos[0]]
        #cell.make_active()
        cell.update("-")
        cell.render()
    
    def compose(self) -> ComposeResult:
        size = self.size
        self.log("My size prior to population is:")
        self.log(size)
        # print(size)
        # self.number_of_rows = size.height//3
        # self.number_of_columns = size.width//3
        #log = self.query_one(Log)
        
        self.log.error("Grid compose")
        self.styles.layout = "grid"
        self.styles.height = "5fr"
        # self.styles.grid_size_rows = self.number_of_rows
        # self.styles.grid_size_columns = self.number_of_columns
        self.styles.grid_gutter_vertical = 0
        self.styles.grid_gutter_horizontal = 0
        
        #self.styles.border = "solid","blue"
        self.styles.border = ("none", "blue")
        self.g = []

        yield Placeholder(id="placeholder")

        # for row in range(self.number_of_rows):
        #     the_row = []
        #     for col in range(self.number_of_columns):
        #         c = GridCell(row,col)
        #         the_row.append(c)
        #         yield c
        #     self.g.append(the_row)
        """Create child widgets for the snake."""
        # yield Snake()
        # yield Static("🍎")
        

class GridCell(Static):

    state = reactive(" ")
                    
    def on_mount(self) -> None:
        #self.set_interval(0.1, self.update_time)
        ...
    
    def update_state(self,state) -> None:
        self.time = state
    
    def watch_state(self, state: str) -> None:
        self.update(f"{state}")

    @staticmethod
    def at(row: int, col: int) -> str:
        """Get the ID of the cell at the given location.

        Args:
            row (int): The row of the cell.
            col (int): The column of the cell.

        Returns:
            str: A string ID for the cell.
        """
        return f"cell-{row}-{col}"

    def __init__(self,row,col):
        super().__init__("", id=self.at(row, col))
        self.row = row
        self.col = col
    
    # def compose(self):
    #     self.styles.border = "solid","green"
    #     #yield Static("x",classes="cell")

    def make_active(self):
        self.update_state(".")



class SnakeApp(App):
    """A Textual app to host a snake game."""

    # TODO: can i add multiple keys to same action wouthout duplicating the action?
    CSS_PATH = "snake.css"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("+", "increase_length", "Increase the length of the snake"),
        ("q", "quit", "Quit the application"),
        ("escape", "quit", "Quit the application"),
        ("left", "point_left", "Move the snake left"),
        ("right", "point_right", "Move the snake right"),
        ("up", "point_up", "Move the snake up"),
        ("down", "point_down", "Move the snake down")
        ]
    
    sw = StatusWindow(id="status_window")
    snake = Snake()
    play_area = PlayArea()
    length = 2
    x = 5
    y = 5
    dx = 1
    dy = 0
    ticks = 0
    
    def on_mount(self) -> None:
        """Mount the app."""
        self.update_timer = self.set_interval(1 / 4, self.on_tick)

    def die(self) -> None:
        """Die."""
        self.update_timer.stop()
        self.exit()
        ...


    def on_tick(self) -> None:
        """Update the app state on each tick."""
        self.ticks += 1

        #log = self.query_one(Log)
        #log.write_line("Tick!")
        self.log("Ticking")
        
        self.x += self.dx
        self.y += self.dy

        if self.x < 0 or self.x >= self.play_area.number_of_columns:
            self.die()
        elif self.y < 0 or self.y >= self.play_area.number_of_rows:
            self.die()
        else:
            self.play_area.make_active((self.x, self.y))

            self.sw.update_position((self.x, self.y))
            self.snake.update_position((self.x, self.y))
        pass

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield self.play_area
        yield self.sw
        log.info("Play Area size:")
        log.info(self.play_area.size)
        #yield Log(auto_scroll=True)
        #yield self.snake

    def action_point_left(self) -> None:
        """An action to move the snake left."""
        self.dx = -1
        self.dy = 0
    
    def action_point_right(self) -> None:
        """An action to move the snake left."""
        self.dx = 1
        self.dy = 0
        
    def action_point_up(self) -> None:
        """An action to move the snake left."""
        self.dx = 0
        self.dy = -1

    def action_point_down(self) -> None:
        """An action to move the snake left."""
        self.dx = 0
        self.dy = +1
        
        

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_increase_length(self) -> None:
        """An action to increase the length of the snake."""
        self.length += 1
        self.sw.update_length(self.length)
        pass

    def on_ready(self) -> None:
        # log = self.query_one(Log)
        # log.write_line("Ready!")
        self.log("Ready!")
        log.info("Play Area size:")
        log.info(self.play_area.size)
        self.play_area.update_size()


if __name__ == "__main__":
    app = SnakeApp()
    app.run()
