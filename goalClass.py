# this file controls user goals, allows them to add goals, 
# get a workout schedule, and readjust based on logged workouts

import numpy as np
import copy
from simplex import *

class Goal(object):
    def __init__(self, weightLoss, workoutDays, weeksForGoal, userDailyNeed):
        self.weightLoss=weightLoss
        self.workoutDays=workoutDays #this is a list of days the user works out
        #workoutDays list formatting: [0,1,2,3,4,5,6] (starts at sunday=0)
        # --> only includes days user will work out
        self.workoutFreq=len(self.workoutDays)
        self.weeksForGoal=weeksForGoal
        self.dailyNetCals=0
        self.dailyCalBurn=0
        self.dailyWorkoutSchedule=np.ones((self.weeksForGoal, 7))
        self.totalCalBurn=3500*self.weightLoss
        self.userDailyNeed=userDailyNeed
        self.currWeek=0
        self.netCaloriesSoFar=0
        self.mask=np.ones((self.weeksForGoal, 7))
        self.currWeek=0
        self.daysPassed=1
        self.setWorkoutSchedule()

    def setInitialValues(self):
        self.totalDays=self.weeksForGoal*7
        self.workoutsToAchieve=self.weeksForGoal*self.workoutFreq
        self.dailyCalBurn=self.totalCalBurn/self.workoutsToAchieve
        self.dailyNetCals=((self.userDailyNeed*self.totalDays)-self.totalCalBurn)
        self.dailyNetCals/=self.totalDays

    def setWorkoutSchedule(self):
        # sets daily net goals for the first time when goal is created
        self.setInitialValues()
        self.dailyWorkoutSchedule=np.multiply(self.dailyWorkoutSchedule, self.dailyNetCals)

    def recalculateDailyGoals(self, calories):
        daysLeft=(7*self.weeksForGoal)-self.daysPassed
        calsLeft=self.dailyNetCals*daysLeft-self.netCaloriesSoFar
        vals= simplex(daysLeft, calsLeft)
        print('x1',int(vals['x1']))
        return int(vals['x1'])

myGoal=Goal(20, [1,3,5], 52, 2000)
