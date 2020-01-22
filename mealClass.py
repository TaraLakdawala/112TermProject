# meal class tracks user's meals, cals consumed, and food name to see their eating history

import datetime

class Meal(object):
    def __init__(self, calsConsumed, food):
        self.calsConsumed=calsConsumed
        self.food=food
        now=datetime.datetime.now()
        self.time=now.strftime('%H:%M:%S')
        self.day=now.strftime('%Y-%m-%d')
    
    def __repr__(self):
        return f'''Food: {self.food}
Calories: {self.calsConsumed}'''