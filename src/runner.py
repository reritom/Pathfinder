class Runner:
    def __init__(self, maze, bot):
        self.maze = maze
        self.bot = bot

    def add_event(self, iteration, event):
        # For making the maze dynamic
        pass

    def run(self, max_iterations=50, to_gif=True, gif_path='./test.gif', gif_fps=5):
        iterations = 0

        while iterations < max_iterations or self.bot.position != self.bot.target:
            # See where the bot is placed
            bot_position = self.bot.position

            # Find the surrounding positions for the bot
            surroundings = maze.get_surroundings(bot_position)
            pass
