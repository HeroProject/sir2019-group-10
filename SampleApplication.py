
import AbstractApplication as Base
from threading import Semaphore


class DialogFlowSampleApplication(Base.AbstractApplication):
    def main(self):
        # Set the correct language (and wait for it to be changed)
        self.langLock = Semaphore(0)
        self.setLanguage('en-US')
        self.langLock.acquire()
        self.name = "Granny"

        # Pass the required Dialogflow parameters (add your Dialogflow parameters)
        self.setDialogflowKey('<keyfile>.json')
        self.setDialogflowAgent('<agentname>')

        # Make the robot ask the question, and wait until it is done speaking
        self.speechLock = Semaphore(0)
        self.sayAnimated('Hello, what is your name?')
        self.speechLock.acquire()

        # Listen for an answer for at most 5 seconds
        self.name = "Granny"
        self.nameLock = Semaphore(0)
        self.setAudioContext('answer_name')
        self.startListening()
        self.nameLock.acquire(timeout=5)
        self.stopListening()

        if not self.name:  # wait one more second after stopListening (if needed)
            self.nameLock.acquire(timeout=1)

        # Respond and wait for that to finish
        if self.name:
            self.sayAnimated('Nice to meet you ' + self.name + '!')
        else:
            self.sayAnimated('Sorry, I didn\'t catch your name.')
        self.speechLock.acquire()

        # Display a gesture (replace <gestureID> with your gestureID)
        self.gestureLock = Semaphore(0)
        self.doGesture('<gestureID>/behavior_1')
        self.gestureLock.acquire()


# R: Good morning {insert name of patient}. How are you feeling today?
        self.speechLock = Semaphore(0)
        self.sayAnimated('Good morning Granny. How are you feeling today?')
        self.speechLock.acquire()

        self.mood = None
        self.moodLock = Semaphore(0)
        self.setAudioContext('answer_mood')
        self.startListening()
        self.moodLock.acquire(timeout=5)
        self.stopListening()

        if not self.mood:  # wait one more second after stopListening (if needed)
            self.moodLock.acquire(timeout=1)

        # Respond and wait for that to finish
        if self.mood == "good":
            self.sayAnimated("I am happy to hear that your are doing {}".format(self.mood))
        elif self.mood == "bad":
            self.sayAnimated("I am sorry to hear that you are {}. I will call the doctor.".format(self.mood))
        else:
            self.sayAnimated('Sorry, I didn\'t catch your answer.')
        self.speechLock.acquire()

        # Display a gesture (replace <gestureID> with your gestureID)
        self.gestureLock = Semaphore(0)
        self.doGesture('<gestureID>/behavior_1') # TODO add animation
        self.gestureLock.acquire()


# R: “Before we start the day, let's play a little game together,''

        self.speechLock = Semaphore(0)
        self.sayAnimated("Before we start the day, let's play a little game together.")
        self.speechLock.acquire()

        self.play = None
        self.playLock = Semaphore(0)
        self.setAudioContext('answer_play')
        self.startListening()
        self.playLock.acquire(timeout=5)
        self.stopListening()

        if not self.play:  # wait one more second after stopListening (if needed)
            self.playLock.acquire(timeout=1)

        # Respond and wait for that to finish
        if self.play == "yes":
            self.sayAnimated("I like your enthusiasm, {}".format(self.name))
        elif self.play == "no":
            self.sayAnimated("We don't want to miss this practice session, {}".format(self.name))
        else:
            self.sayAnimated('Sorry, I didn\'t catch your answer.')
        self.speechLock.acquire()

        # Display a gesture (replace <gestureID> with your gestureID)
        self.gestureLock = Semaphore(0)
        self.doGesture('<gestureID>/behavior_1') # TODO add animation
        self.gestureLock.acquire()





# R: What game do you want to play.
        # X: Ohhh gee I don't know dear.
        # R: Last time we played X game, what do you think of the numbers game?
        # X: That sounds good to me.
        # R: Great let's start!. {The robot starts the game}, {the SKT test starts on the tablet}

        self.speechLock = Semaphore(0)
        self.sayAnimated("What kind of game would you like to play?")
        self.speechLock.acquire()

        self.game = None
        self.gameLock = Semaphore(0)
        self.setAudioContext('answer_game')
        self.startListening()
        self.gameLock.acquire(timeout=5)
        self.stopListening()

        if not self.game:  # wait one more second after stopListening (if needed)
            self.gameLock.acquire(timeout=1)

        # Respond and wait for that to finish
        if self.game == "numbers":
            self.sayAnimated("Let's play that, {}".format(self.name))
        elif self.game == "no": # i don't know answer
            self.sayAnimated("I believe last time we played Sudoku, how about playing the numbers game?")
        else:
            self.sayAnimated('Sorry, I didn\'t catch your answer.')
        self.speechLock.acquire()

        # Display a gesture (replace <gestureID> with your gestureID)
        self.gestureLock = Semaphore(0)
        self.doGesture('<gestureID>/behavior_1') # TODO add animation
        self.gestureLock.acquire()



        # TODO add a listener here so we can pick the yes
        # not sure what speechLock is
        self.speechLock = Semaphore(0)
        self.speechLock.acquire()

        self.yesno = None
        self.yesnoLock = Semaphore(0)
        self.setAudioContext('answer_yesno')
        self.startListening()
        self.yesnoLock.acquire(timeout=5)
        self.stopListening()

        if not self.yesno:  # wait one more second after stopListening (if needed)
            self.yesnoLock.acquire(timeout=1)

        # Respond and wait for that to finish
        if self.yesno == "yes":
            self.sayAnimated("Great let's start, {}!".format(self.name))
        elif self.yesno == "no": # i don't know answer
            self.sayAnimated("We need to play it either way.")
        else:
            self.sayAnimated('Sorry, I didn\'t catch your answer.')
        self.speechLock.acquire()

        # Display a gesture (replace <gestureID> with your gestureID)
        self.gestureLock = Semaphore(0)
        self.doGesture('<gestureID>/behavior_1') # TODO add animation
        self.gestureLock.acquire()




# R: Remember {name patient} the goal of the game is to place the numbers in the right order.
# X: Like this? {patient makes a correct move}
# R: Yes {name patient} you’re doing great!

        self.speechLock = Semaphore(0)
        self.sayAnimated("Remember {} the goal of the game is to place the numbers in the right order.".format(self.name))
        self.speechLock.acquire()

        self.gamemove = None
        self.gamemoveLock = Semaphore(0)
        self.setAudioContext('answer_play')
        self.startListening()
        self.gamemoveLock.acquire(timeout=5)
        self.stopListening()

        if not self.gamemove:  # wait one more second after stopListening (if needed)
            self.gamemoveLock.acquire(timeout=1)


        # TODO I can loop this over and go through the answers
        # Respond and wait for that to finish
        if self.gamemove == "yes":
            self.sayAnimated("Yes, {}. You are doing great!".format(self.name))
        elif self.gamemove == "no":
            self.sayAnimated("We don't want to miss this practice session, {}".format(self.name))
        else:
            self.sayAnimated('Sorry, I didn\'t catch your answer.')
        self.speechLock.acquire()

        # Display a gesture (replace <gestureID> with your gestureID)
        self.gestureLock = Semaphore(0)
        self.doGesture('<gestureID>/behavior_1') # TODO add animation
        self.gestureLock.acquire()


# R: Insert random fact about the patient.
# X: I think number 76 goes next to 34, right?
# R: That is not completely correct {name patient}, maybe we should look at this one first {robot points to the next number}.
# X: Oh, you are right darling. Let me put 76 next to the {robot points to the next number}.
# Game goes on (cut to the end of the game)
# X: And the final number goes here.
# R: Congratulations, you finished the game and did a good job?
# X: Thank you {robot}, it was fun playing together.
# R: {robot calls the caregiver}


    def onRobotEvent(self, event):
        if event == 'LanguageChanged':
            self.langLock.release()
        elif event == 'TextDone':
            self.speechLock.release()
        elif event == 'GestureDone':
            self.gestureLock.release()

    def onAudioIntent(self, *args, intentName):
        if intentName == 'answer_name' and len(args) > 0:
            self.name = args[0]
            self.nameLock.release()
        elif intentName == 'answer_mood' and len(args) > 0:
            self.mood = args[0]
            self.moodLock.release()
        # TODO add all instances here


# Run the application
sample = DialogFlowSampleApplication()
sample.main()
sample.stop()