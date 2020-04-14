"""Dummy main module for testing."""


class Wumpus():

    def __init__(self, name):

        self.name = name

    def talk_to(self, message):

        return f"{self.name}: hello to you to."
