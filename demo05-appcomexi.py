import time
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class App:
    def __init__(self):
        self.color_sequence = ['cyan', 'magenta', 'yellow', 'black']
        self.current_color_index = 0
        self.steps = 0

    def standby(self):
        print("STANDBY")
        time.sleep(1)

    def animate(self, i):
        plt.clf()
        if self.steps < 8:
            self.update_color_bar()
            self.steps += 1
        else:
            self.steps = 0
            self.current_color_index = (self.current_color_index + 1) % len(self.color_sequence)

    def update_color_bar(self):
        plt.bar([0, 1, 2, 3], [1, 1, 1, 1], color=self.color_sequence[self.current_color_index])
        plt.xlim(-0.5, 3.5)
        plt.title('Color Bar Rotation')

    def run(self):
        self.standby()
        ani = animation.FuncAnimation(plt.gcf(), self.animate, frames=80, interval=1000)
        plt.show()

        # SCREEN 3 - Display TEST_VIDEO
        print("Displaying TEST_VIDEO...")

        # Loop color rotation until all bars complete
        plt.show()  # Required to display the animation

if __name__ == '__main__':
    app = App()
    app.run()