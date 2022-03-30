from cgi import test
import datetime
from doctest import OutputChecker
from random import random, sample
import this
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import Grid
from mesa.time import RandomActivation
from mesa.batchrunner import BatchRunner
from os import sep

from numpy import column_stack

from .agent import TreeCell


class ForestFire(Model):
    """
    Simple Forest Fire model.
    """

    def __init__(self, width=100, height=100, density=0.65, humidity_level=0.5):
        """
        Create a new forest fire model.

        Args:
            width, height: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        """
        # Set up model objects
        self.schedule = RandomActivation(self)
        self.grid = Grid(width, height, torus=False)

        self.count_steps = 0

        self.density = density
        self.humidity_level = humidity_level

        self.datacollector = DataCollector(
            model_reporters={
                "Fine": lambda m: self.count_type(m, "Fine"),
                "On Fire": lambda m: self.count_type(m, "On Fire"),
                "Burned Out": lambda m: self.count_type(m, "Burned Out"),
                "Humid": lambda m: self.count_type(m, "Humid"),
                "Percent": lambda m: self.count_percentage(m)
            }
        )
        self.datacollector_agent = DataCollector(
            agent_reporters={
                "Steps to fire up": lambda x: x.count_steps
            }
        )

       
        count = 1
        for (contents, x, y) in self.grid.coord_iter():
            if self.random.random() < density:
                count += 1
        quantity = count * (humidity_level)
        randomX = self.random.sample(range(count), int(quantity))
        randomY = self.random.sample(range(count), int(quantity))
        randomX.sort()
        randomY.sort()
        # Place a tree in each cell with Prob = density
        for (contents, x, y) in self.grid.coord_iter():
            if self.random.random() < density:
                # Create a tree
                new_tree = TreeCell((x, y), self)
                # Set all trees in the first column on fire.
                if x == 0:
                    new_tree.condition = "On Fire"
                if x in randomX and x != 0:
                    if y in randomY:
                        new_tree.condition = "Humid"
                self.grid._place_agent((x, y), new_tree)
                self.schedule.add(new_tree)
                self.count_steps += 1
        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Advance the model by one step.
        """
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        # Halt if no more fire
        if self.count_type(self, "On Fire") == 0:
            self.running = False

            alive = self.count_type(self, "Fine")
            humid = self.count_type(self, "Humid")
            percentage = (alive + humid)/ self.count_steps


            now = str(datetime.datetime.now()).replace(":", "-")
            model = self.datacollector.get_model_vars_dataframe()
            model.to_csv("spreadsheet" + sep + "model_data humi=" + str(self.humidity_level) + " dens=" + str(self.density) + " " + now + ".csv")

            self.datacollector_agent.collect(self)
            agent = self.datacollector_agent.get_agent_vars_dataframe()
            agent.to_csv("spreadsheet" + sep + "agent_data humi=" + str(self.humidity_level) + " dens=" + str(self.density) + " " + now + ".csv")  
        

    @staticmethod
    def count_type(model, tree_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        for tree in model.schedule.agents:
            if tree.condition == tree_condition:
                count += 1
        return count
    def count_percentage(self, model):
            total = self.count_type(self, "Humid") + self.count_type(self, "Fine") + self.count_type(self, "Burned Out")
            alive = self.count_type(self, "Humid") + self.count_type(self, "Fine")
            percentage = alive / total
            return percentage







