# this file handles user information and stores all 
# information on the app's users
# 
from goalClass import *
from mealClass import *
import numpy as np

class User(object):
    def __init__(self, name, age, weight, height, sex, activity):
        self.name=name
        self.age=age
        self.weight=weight
        self.height=height
        self.sex=sex
        self.activity=activity
        self.goals=[None]
        self.currGoal=self.goals[-1]
        self.calorieNeeds=self.getCalorieNeeds()
        self.todaysNetCals=0
        self.meals=[]
        self.workouts=[]
        self.newNets=0
        self.number=6788187735
    
    def __repr__(self):
        return self.name

    def getCalorieNeeds(self):
        if self.sex=='f':
            calorieNeeds=4.7*self.height+4.35*self.weight-4.7*self.age+655
            if self.activity==1:
                calorieNeeds*=1.2
            elif self.activity==2:
                calorieNeeds*=1.375
            elif self.activity==3:
                calorieNeeds*=1.55
            elif self.activity==4:
                calorieNeeds*=1.725
            else:
                calorieNeeds*=1.9
        else:
            calorieNeeds=12.7*self.height+6.23*self.weight -6.8*self.age +66
            if self.activity==1:
                calorieNeeds*=1.2
            elif self.activity==2:
                calorieNeeds*=1.375
            elif self.activity==3:
                calorieNeeds*=1.55
            elif self.activity==4:
                calorieNeeds*=1.725
            else:
                calorieNeeds*=1.9
        return calorieNeeds

    def setGoal(self, weightLoss, workoutFreq, weeksForGoal):
        print(self.calorieNeeds)
        self.goals.append(Goal(weightLoss, workoutFreq, weeksForGoal, self.calorieNeeds))
        self.currGoal=self.goals[-1]
        self.currGoal.setInitialValues()

    def getWorkoutSchedule(self):
        self.currWorkoutSchedule=self.currGoal.dailyWorkoutSchedule.tolist()
        return self.currWorkoutSchedule
        #return 2D list of daily expected workout burns

    def logCalories(self, calories): #calories burned must be negative
        self.currGoal.netCaloriesSoFar+=calories
        goal=self.currGoal
        self.newNets=self.currGoal.recalculateDailyGoals(self.todaysNetCals)


