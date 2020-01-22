# SmartWorkouts (c) 2019 Tara Lakdawala
# Andrew ID: tlakdawa
# Email: tlakdawa@andrew.cmu.edu
# This application was created for my 15-112 Term Project in Fall 2019

#SmartWorkouts V3.4 Last updated Wednesday 12/4/2019

from cmu_112_graphics import *
# note: cmu_112_graphics is taken from http://www.cs.cmu.edu/~112 
# and is not my creation
from tkinter import *
import pickle
import os

from userClass import *
from mealClass import *
from workoutClass import *
from simplex import *
from smsReminders import *

client=Client(acctSid, authToken)
acctSid='AC1ecb7981d8e9724b2e9b3af6a0d521cb'
authToken='f0486550029d362ad256b7b03cab0c0b'

class Buttons(object):
    def __init__(self, page, x1, x2, y1, y2, f):
        Buttons.splash=[]
        Buttons.home=[]
        Buttons.add=[]
        Buttons.log=[]
        Buttons.nutrition=[]
        self.page=page #possible pages: 'splash' 'home' 'add' 'log 'nutrition'
        self.x1=x1 #left bound
        self.x2=x2 #right bound
        self.y1=y1 #top bound
        self.y2=y2 #bottom bound
        self.f=f #function to execute onClick

        if self.page=='splash':
            Buttons.splash.append((x1,x2,y1,y2))
        elif self.page =='home':
            Buttons.home.append((x1,x2,y1,y2))
        elif self.page =='add':
            Buttons.add.append((x1,x2,y1,y2)) 
        elif self.page =='log':
            Buttons.log.append((x1,x2,y1,y2))
        elif self.page =='nutrition':
            Buttons.nutrition.append((x1,x2,y1,y2))

    def onClick(self):
        return self.f()

class SplashScreenMode(Mode):
    def appStarted(self):
        Mode.usersList=[]
        Mode.currUser=None

    def drawUserProfiles(self, canvas):
        margin=50
        x=self.width/2
        y=self.height//8
        for i in range(len(Mode.usersList)):
            canvas.create_text(x, y, text=f'{Mode.usersList[i]}', font='Helvectia 18')
            y+=50

    def redrawAll(self, canvas):
        canvas.create_text(self.width/2, 30,text='Who\'s logging in today?', font='Helvectia 26 bold')
        self.drawUserProfiles(canvas)
        canvas.create_rectangle(self.width/2-50, self.height*4/5, 
                self.width/2+50, self.height*4/5+50, 
                fill='cyan', outline='cyan')
        canvas.create_text(self.width/2, self.height*4/5+25, text='Add User')

    def getUser(self):
        name=self.getUserInput('What is your name?')
        age=self.getUserInput('What is your age?')
        weight=self.getUserInput('What is your weight?')
        height=self.getUserInput('What is your height in inches?')
        sex=self.getUserInput('What is your sex? (m/f)')
        activity=self.getUserInput('What is your daily average activity level on a scale of 1-5 (5 being most)?')
        try:
            Mode.usersList.append(User(name, int(age), float(weight), float(height), sex, int(activity)))
        except:
            print('User not added')

    def mousePressed(self, event):
        if event.x<=self.width/2+50 and event.x>=self.width/2-50\
            and event.y<=self.height*4/5+50 and event.y>=self.height*4/5:
            self.getUser()
        elif event.y>=self.height/8-15 and event.y<self.height/8+35:
            if 0<len(Mode.usersList):
                Mode.currUser=Mode.usersList[0]
                print(Mode.currUser.name)
                self.app.setActiveMode(self.app.homePage)
        elif event.y>=self.height/8+35 and event.y<self.height/8+85:
            if 1<len(Mode.usersList):
                Mode.currUser=Mode.usersList[1]
                print(Mode.currUser.name)
                self.app.setActiveMode(self.app.homePage)
        elif event.y>=self.height/8+85 and event.y<self.height/8+135:
            if 2<len(Mode.usersList):
                Mode.currUser=Mode.usersList[2]
                self.app.setActiveMode(self.app.homePage)
        elif event.y>=self.height/8+135 and event.y<self.height/8+185:
            if 3<len(Mode.usersList):
                Mode.currUser=Mode.usersList[3]
                self.app.setActiveMode(self.app.homePage)
        elif event.y>=self.height/8+185 and event.y<self.height/8+215:
            if 4<len(Mode.usersList):
                Mode.currUser=Mode.usersList[4]
                self.app.setActiveMode(self.app.homePage)
        elif event.y>=self.height/8+215 and event.y<self.height/8+265:
            if 5<len(Mode.usersList):
                Mode.currUser=Mode.usersList[5]
                self.app.setActiveMode(self.app.homePage)
        

class HomePage(Mode):
    def appStarted(self):
        print(Mode.currUser.name)

    def mousePressed(self, event):
        if event.x<=(50) and event.y<=20:
            self.app.setActiveMode(self.app.homePage)
        elif event.x>=self.width/4 and event.x<self.width/2 \
            and event.y<=self.height//20:
            self.app.setActiveMode(self.app.logWorkout)
        elif event.x>=(self.width/2) and event.x<(3*self.width/4) \
            and event.y<=self.height//20:
            self.app.setActiveMode(self.app.nutritionPage)
        elif event.x>=3*self.width/4 and event.y<=self.height//20:
            self.logout()
        elif event.x>=self.width/2-130 and event.x<=self.width/2-10 \
            and event.y>=self.height*5/6 and event.y<=self.height*5/6+30:
            self.getGoal()
        elif event.x<=self.width/2+130 and event.x>=self.width/2+10 \
            and event.y>=self.height*5/6 and event.y<=self.height*5/6+30:
            self.addNumber()
    
    def addNumber(self):
        Mode.currUser.number=self.getUserInput('What is your phone number?')

    def sendMessage(self, number, client):
        message=client.api.account.messages.create(f'+1{number}', from_='+12563636816', 
            body='It\'s almost time for your workout! Let\'s hit the gym!')

    def keyPressed(self, event):
        if event.key=='r':
            self.sendMessage(Mode.currUser.number, client)

            print('To the user: please note, I am using a trial version of the Twilio API, so it will only send text messages to my personal phone number')
            

    def getGoal(self):
        weightLoss=self.getUserInput('How many pounds do you want to lose?')
        workoutDays=self.getUserInput('What days of the week can you work out?')
        weeksForGoal=self.getUserInput('How many weeks do you want to achieve this in?')
        try:
            Mode.currUser.goals.append(Goal(int(weightLoss), self.getWorkoutDays(workoutDays), int(weeksForGoal), int(Mode.currUser.calorieNeeds)))
            Mode.currUser.currGoal=Mode.currUser.goals[-1]
        except:
            print('Goal not added')       

    def getWorkoutDays(self, workoutDays):
        L=workoutDays.split(',')
        for i in range(len(L)):
            L[i]=int(L[i])
        return L

    def drawCalendar(self,canvas):
        schedule=Mode.currUser.getWorkoutSchedule()
        x=0
        x1=self.width/7
        y=self.height/2-self.height/8
        y1=y+self.height/8
        for j in range(7):
            days=(Mode.currUser.currGoal.weeksForGoal*7)-1
            self.todaysCals=int(((Mode.currUser.calorieNeeds)*(days+1)-Mode.currUser.todaysNetCals)/days)
            canvas.create_rectangle(x,y,x1, y1, outline='black')
            if j!=0:
                canvas.create_text((x+x1)/2,y+50,text=f'Net Calories: {Mode.currUser.newNets}')
            else: 
                canvas.create_text((x+x1)/2, y+50, text=f'Net Calories: {Mode.currUser.todaysNetCals}')
            x,x1=x1,x1+self.width/7


    def logout(self):
        print('Logout button clicked')
        output=open('userInfo.pkl', 'wb')
        Mode.currUser=None
        pickle.dump(Mode.usersList, output)
        self.app.setActiveMode(self.app.splashScreenMode)

    def drawNavBar(self, canvas):
        x=30
        y=20
        canvas.create_rectangle(0,0,self.width, self.height//20, fill='cyan', outline='cyan')
        buttonsList=['Home', 'Log Workout', 'My Nutrition', 'Logout']
        for i in range(4):
            canvas.create_text(x,y,text=buttonsList[i])
            x+=self.width/4

    def redrawAll(self, canvas):
        self.drawNavBar(canvas)
        canvas.create_text(self.width/2, self.height/15, text=f'Welcome back, {Mode.currUser.name}',
                            font='Helvectia 26')
        self.calsLeft=Mode.currUser.calorieNeeds-Mode.currUser.todaysNetCals
        canvas.create_text(self.width/2, self.height/8,
                text=f'You have {int(self.calsLeft)} calories left today', font='Helvectia 16')
        canvas.create_text(self.width/2, self.height/6, text='Add a goal or log a workout or a meal to see what your calorie goals should be this week!')
        if Mode.currUser.currGoal!=None:
            self.drawCalendar(canvas)
        canvas.create_rectangle(self.width/2-130, self.height*5/6, 
                                self.width/2-10, self.height*5/6+30, 
                                fill='cyan', outline='cyan')
        canvas.create_text(self.width/2-70, self.height*5/6+15, text='Update Goal')
        canvas.create_rectangle(self.width/2+10, self.height*5/6, 
                                self.width/2+130, self.height*5/6+30,
                                fill='cyan', outline='cyan')
        canvas.create_text(self.width/2+70, self.height*5/6+15, text='Add My Number')

class LogWorkout(Mode):
    
    def drawNavBar(self, canvas):
        x=30
        y=20
        canvas.create_rectangle(0,0,self.width, self.height//20, fill='cyan', outline='cyan')
        buttonsList=['Home', 'Log Workout', 'My Nutrition', 'Logout']
        for i in range(4):
            canvas.create_text(x,y,text=buttonsList[i])
            x+=self.width/4

    def redrawAll(self, canvas):
        self.drawNavBar(canvas)
        canvas.create_rectangle(self.width/2-50, self.height/5-30, 
                self.width/2+50, self.height/5+30, fill='cyan', outline='cyan')
        canvas.create_text(self.width/2, self.height/5, text='Log Workout')
        self.displayWorkouts(canvas) 

    def mousePressed(self, event):
        if event.x<=(50) and event.y<=self.height//20:
            self.app.setActiveMode(self.app.homePage)
        elif event.x>=(self.width/2) and event.x<(3*self.width/4) \
            and event.y<=self.height//20:
            self.app.setActiveMode(self.app.nutritionPage)
        elif event.x>=3*self.width/4 and event.y<=self.height//20:
            self.logout()
        elif event.x<=self.width/2+50 and event.x>=self.width/2-50 \
            and event.y<=self.height/5+30 and event.y>=self.height/5-30:
            try:
                self.logWorkout()
            except:
                print('Workout not logged')
    
    def displayWorkouts(self,canvas):
        if len(Mode.currUser.workouts)>=5:
            total=0
            for i in range(5):
                ind=(i+1)*-1
                workout=Mode.currUser.workouts[ind]
                cals=int(workout.calsBurned)
                l=5
                canvas.create_rectangle(self.width/l*(i)+self.width/(2*l)-20, 
                                        self.height/2+220-cals/3,
                                        self.width/l*(i)+self.width/(2*l)+20,
                                        self.height/2+220, fill='blue', outline='blue')
                canvas.create_text(self.width/5*(i)+self.width/10, self.height/2+250, text=f'{Mode.currUser.workouts[ind]}')
                total+=cals
            avg=total/l
    
        elif len(Mode.currUser.workouts)>0:
            total=0
            for i in range(len(Mode.currUser.workouts)):
                l=len(Mode.currUser.workouts)
                ind=(i+1)*-1
                workout=Mode.currUser.workouts[ind]
                cals=int(workout.calsBurned)
                canvas.create_rectangle(self.width/l*(i)+self.width/(2*l)-20, 
                                        self.height/2+220-cals/3,
                                        self.width/l*(i)+self.width/(2*l)+20,
                                        self.height/2+220, fill='blue', outline='blue')
                canvas.create_text(self.width/l*(i)+self.width/(2*l), self.height/2+250, text=f'{Mode.currUser.workouts[ind]}')
                total+=cals
            avg=total/l
        else:
            total=0
            canvas.create_text(self.width/2, self.height/2+250, text='Log a workout to see your past workouts here!')
            avg=total/1
        canvas.create_text(self.width/2, self.height/2+315, text=f'Average Calories Burned: {avg}', font='Helvectia 18')

    def logWorkout(self):
        calsBurned=self.getUserInput('How many calories did you burn?')
        Mode.currUser.todaysNetCals-=int(calsBurned)
        workoutType=self.getUserInput('What exercise did you do today?')
        workoutNotes=self.getUserInput('Any notes about this workout?')
        Mode.currUser.workouts.append(Workout(calsBurned, workoutType, workoutNotes))
        Mode.currUser.logCalories(-int(calsBurned))
    
    def logout(self):
        print('Logout button clicked')
        output=open('userInfo.pkl', 'wb')
        Mode.currUser=None
        pickle.dump(Mode.usersList, output)
        self.app.setActiveMode(self.app.splashScreenMode)


class NutritionPage(Mode):
    def drawNavBar(self, canvas):
        x=30
        y=20
        canvas.create_rectangle(0,0,self.width, self.height//20, fill='cyan', outline='cyan')
        buttonsList=['Home', 'Log Workout', 'My Nutrition', 'Logout']
        for i in range(4):
            canvas.create_text(x,y,text=buttonsList[i])
            x+=self.width/4
    
    def displayMeals(self,canvas):
        if len(Mode.currUser.meals)>=5:
            total=0
            for i in range(5):
                ind=(i+1)*-1
                meal=Mode.currUser.meals[ind]
                cals=int(meal.calsConsumed)
                l=5
                canvas.create_rectangle(self.width/l*(i)+self.width/(2*l)-20, 
                                        self.height/2+220-cals/5,
                                        self.width/l*(i)+self.width/(2*l)+20,
                                        self.height/2+220, fill='blue', outline='blue')
                canvas.create_text(self.width/5*(i)+self.width/10, self.height/2+250, text=f'{meal}')
                total+=cals
            avg=total/l
    
        elif len(Mode.currUser.meals)>0:
            total=0
            for i in range(len(Mode.currUser.meals)):
                l=len(Mode.currUser.meals)
                ind=(i+1)*-1
                meal=Mode.currUser.meals[ind]
                cals=int(meal.calsConsumed)
                canvas.create_rectangle(self.width/l*(i)+self.width/(2*l)-20, 
                                        self.height/2+220-cals/5,
                                        self.width/l*(i)+self.width/(2*l)+20,
                                        self.height/2+220, fill='blue', outline='blue')
                canvas.create_text(self.width/l*(i)+self.width/(2*l), self.height/2+250, text=f'{meal}')
                total+=cals
            avg=total/l
        else:
            total=0
            canvas.create_text(self.width/2, self.height/2+250, text='Log a meal to see your past meals here!')
            avg=total/1
        canvas.create_text(self.width/2, self.height/2+315, text=f'Average Calories Consumed: {avg}', font='Helvectia 18')

    def redrawAll(self, canvas):
        self.drawNavBar(canvas)
        canvas.create_rectangle(self.width/2-50, self.height/5-30, 
                self.width/2+50, self.height/5+30, fill='cyan', outline='cyan')
        canvas.create_text(self.width/2, self.height/5, text='Log a Meal') 
        self.displayMeals(canvas) 

    def mousePressed(self, event):
        if event.x<=(50) and event.y<=20:
            self.app.setActiveMode(self.app.homePage)
        elif event.x>=self.width/4 and event.x<self.width/2 \
            and event.y<=self.height//20:
            self.app.setActiveMode(self.app.logWorkout)
        elif event.x>=(self.width/2) and event.x<(3*self.width/4) \
            and event.y<=self.height//20:
            self.app.setActiveMode(self.app.nutritionPage)
        elif event.x>=3*self.width/4 and event.y<=self.height//20:
            self.logout()
        elif event.x<=self.width/2+50 and event.x>=self.width/2-50 \
            and event.y<=self.height/5+30 and event.y>=self.height/5-30:
            try:
                self.logMeal()
            except:
                print('Meal not logged')
            
    def logMeal(self):
        calsConsumed=self.getUserInput('How many calories was you meal?')
        Mode.currUser.todaysNetCals+=int(calsConsumed)
        food=self.getUserInput('What did you eat?')
        Mode.currUser.meals.append(Meal(calsConsumed, food))
        Mode.currUser.logCalories(int(calsConsumed))

    def logout(self):
        print('Logout button clicked')
        output=open('userInfo.pkl', 'wb')
        Mode.currUser=None
        pickle.dump(Mode.usersList, output)
        self.app.setActiveMode(self.app.splashScreenMode)


class MyModalApp(ModalApp):
    def appStarted(self):
        self.splashScreenMode=SplashScreenMode()
        self.homePage=HomePage()
        self.logWorkout=LogWorkout()
        self.nutritionPage=NutritionPage()
        self.setActiveMode(self.splashScreenMode)
        self.timerDelay=50
        if os.path.exists('userInfo.pkl'):
            output=open('userInfo.pkl', 'rb')
            Mode.usersList=pickle.load(output)

app = MyModalApp(width=1200, height=750)