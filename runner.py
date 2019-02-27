class Runner:
    def __init__(self, maze, bot):
        self.maze = maze
        self.bot = bot

    def add_event(self, iteration):
        # For making the maze dynamic
        pass

    def run(self, max=1000):
        iterations = 0

        while iterations < max:
            # See where the bot is placed
            bot_position = self.bot.position

            # Find the surrounding positions for the bot
            surroundings = maze.get_surroundings(bot_position)
            pass