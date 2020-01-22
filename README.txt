Smart Workouts (c) 2019 Tara Lakdawala

README

Andrew ID: tlakdawa
Email: tlakdawa@andrew.cmu.edu
This application was created for my 15-112 Term Project in Fall 2019\
SmartWorkouts V3.2 Last updated Wednesday 12/4/2019

Project Description:
The SmartWorkouts App helps users intuitively plan workouts based on their schedules and goals. The app takes the work out of planning workouts by giving users a week-to-week schedule which breaks down their overarching fitness goals into smaller, achievable steps. Users will no longer have to face the stress of trying to achieve their goals without knowing what they need to achieve on a daily basis. Users can also set up daily text message reminders to work out and see their average calories consumer over the last few meals and average calories burned in their last few workouts. The app generates graphs to help users visualise their consumption and burning trends. Lastly, it can store user information across runs of the app, so if you create a new user, the next time you run the app, you should be able to user their account again (you need to hit the 'logout' button to save their info, otherwise it won't save).

Note: 
To send text messages on command instead of at the scheduled time, press 'r' from the home screen. This function only works to send messages to my personal phone number because I am using a trial version of the Twilio API, so I will cover this feature in the live demo.

To run this project, you will need to:

1) Have cmu_112_graphics.py (included in the folder)
2) Install the twilio API (you can easily install this by running the following command in your terminal):
		pip install twilio
If pip doesn't work, try pip3
3) Install numpy (you can easily install this by running the following command in your terminal):
		pip install numpy
If pip doesn't work, try pip3
4) run the __main__.py file in any environment.

Note: this project comes with a .pkl file which contains information of some pre-made users to make demoing the app easier. You do not need to touch this file.\


The following modules are used in this project:

1) Twilio
2) Pickle (included in Anaconda)
3) os (Included in Anaconda)
4) Tkinter (Included with Anaconda)