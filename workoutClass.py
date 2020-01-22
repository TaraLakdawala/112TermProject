#workout class

class Workout(object):
    def __init__(self, calsBurned, workoutType, workoutNotes):
        self.calsBurned=calsBurned
        self.workoutType=workoutType
        self.workoutNotes=workoutNotes
    
    def __repr__(self):
        return f'''You burned {self.calsBurned} calories.
Workout Type: {self.workoutType}
Workout Notes: {self.workoutNotes}'''