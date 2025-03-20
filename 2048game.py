import tkinter as tk
import random

GRID_SIZE = 4       # 4x4 grid
CELL_SIZE = 100     # Size of each cell in pixels

class Game2048(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.init_game()
        self.create_widgets()
        self.master.bind("<Key>", self.key_handler)

    def init_game(self):
        # Initialize the board and score, and add two initial tiles.
        self.board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def create_widgets(self):
        # Create a canvas to draw the game board.
        self.canvas = tk.Canvas(self, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE, bg="azure3")
        self.canvas.grid(row=0, column=0)
        self.draw_board()

    def draw_board(self):
        # Clear the canvas and redraw the grid with the current board state.
        self.canvas.delete("all")
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = self.board[i][j]
                x0 = j * CELL_SIZE
                y0 = i * CELL_SIZE
                x1 = x0 + CELL_SIZE
                y1 = y0 + CELL_SIZE
                color = self.get_color(value)
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")
                if value != 0:
                    self.canvas.create_text((x0+x1)//2, (y0+y1)//2, text=str(value), font=("Helvetica", 24, "bold"))
        # Display the current score at the bottom.
        self.canvas.create_text(10, GRID_SIZE * CELL_SIZE - 10, anchor="sw", 
                                text=f"Score: {self.score}", font=("Helvetica", 16, "bold"))

    def get_color(self, value):
        # Returns a color based on the tile value.
        colors = {
            0: "azure3",
            2: "lightyellow",
            4: "lightgoldenrod",
            8: "orange",
            16: "darkorange",
            32: "tomato",
            64: "red",
            128: "gold",
            256: "yellow",
            512: "goldenrod",
            1024: "lightcoral",
            2048: "green",
        }
        return colors.get(value, "gray")

    def add_new_tile(self):
        # Choose a random empty cell and set it to 2 (90%) or 4 (10%).
        empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = random.choices([2, 4], [0.9, 0.1])[0]

    def key_handler(self, event):
        # Handle arrow key presses and update the game state accordingly.
        key = event.keysym
        if key in ("Up", "Down", "Left", "Right"):
            if self.move(key):
                self.add_new_tile()
                self.draw_board()
                if self.check_game_over():
                    self.game_over()

    def move(self, direction):
        # Save board state to check if move changes anything.
        board_before = [row[:] for row in self.board]
        if direction == "Left":
            self.board = [self.merge(row) for row in self.board]
        elif direction == "Right":
            self.board = [list(reversed(self.merge(list(reversed(row))))) for row in self.board]
        elif direction == "Up":
            self.board = self.transpose(self.board)
            self.board = [self.merge(row) for row in self.board]
            self.board = self.transpose(self.board)
        elif direction == "Down":
            self.board = self.transpose(self.board)
            self.board = [list(reversed(self.merge(list(reversed(row))))) for row in self.board]
            self.board = self.transpose(self.board)
        return board_before != self.board

    def merge(self, row):
        # Slide non-zero numbers to the left, merge equal numbers, and then pad with zeros.
        non_zero = [num for num in row if num != 0]
        merged = []
        i = 0
        while i < len(non_zero):
            if i + 1 < len(non_zero) and non_zero[i] == non_zero[i+1]:
                merged_val = non_zero[i] * 2
                self.score += merged_val
                merged.append(merged_val)
                i += 2
            else:
                merged.append(non_zero[i])
                i += 1
        merged.extend([0] * (GRID_SIZE - len(merged)))
        return merged

    def transpose(self, board):
        # Transpose the board (swap rows and columns).
        return [list(row) for row in zip(*board)]

    def check_game_over(self):
        # The game is over if there are no empty cells and no adjacent cells can be merged.
        if any(0 in row for row in self.board):
            return False
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if i < GRID_SIZE - 1 and self.board[i][j] == self.board[i+1][j]:
                    return False
                if j < GRID_SIZE - 1 and self.board[i][j] == self.board[i][j+1]:
                    return False
        return True

    def game_over(self):
        # Display a game over message and unbind key events.
        self.canvas.create_text(GRID_SIZE * CELL_SIZE // 2, GRID_SIZE * CELL_SIZE // 2, 
                                text="Game Over!", font=("Helvetica", 48, "bold"), fill="black")
        self.master.unbind("<Key>")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("2048")
    game = Game2048(master=root)
    game.mainloop()
