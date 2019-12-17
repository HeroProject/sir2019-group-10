import AbstractApplication as Base
from threading import Semaphore
import numpy as np
import random
import time
import sys

class DialogFlowSampleApplication(Base.AbstractApplication):

        # NAO variable resets
    def reset(self):
        self.times = 0
        self.noAnswer = True
        self.repeat = 0

    def main(self):

        # -- Initialization --
        # in-game variables
        self.noAnswer = True
        self.repeat = 0
        self.name = "Granny" # The name of our patient
        self.setEyeColour("blue") # set the Nao's eyes to blue

        # responses variables when NAO doesn't recognize the answer
        self.responses = ["Sorry, I didn't catched that. Can you repeat it loud and clear for me?",
                          "I think I'm getting a bit old. Could you repeat what you said?",
                          "Sorry, I didn't heard you well. Please repeat it one more time?",
                          "I'm having trouble hearing you. Can you say it one more time?",
                          "Sorry, I wasn't paying attention. Can you repeat it?"]

        # NAO stores information about the patient. This section is the starting point for such thing, but future
        # improvements should be made such as storing the information into a database, categorizing them based on the
        # type of information (good/bad etc)..
        self.userExperience = {22: "On twenty two of July is your birthday!",
                               64: "On your next birthday, you will be 18 years old with 46 years of experience!"
                               }

        # gesture location
        self.bodygesture = self.populate("animation/bodygesture.txt")
        self.finish = self.populate("animation/finish.txt")
        self.happy = self.populate("animation/happy.txt")
        self.listening = self.populate("animation/listening.txt")
        self.thinking = self.populate("animation/thinking.txt")
        self.bad = self.populate("animation/bad.txt")

        # language variables
        self.langLock = Semaphore(0)
        self.setLanguage('en-US')
        self.langLock.acquire()

        # Dialogflow variables (add your Dialogflow parameters)
        self.setDialogflowKey('agentsmith-ljpfky-b35f1421d237.json')
        self.setDialogflowAgent('agentsmith-ljpfky')

        # Case scenario as described in the Design Template. In this example, the patient will play a SKT test in order
        # to analyze the cognitive performances of the patient.

        # -- Main --
        self.act1()  # NAO Wakes up
        self.act2()  # NAO invites the patient for a game
        self.act3()  # Choosing the game
        self.act4()  # Confirmation of the game
        self.act5()  # Game start & play
        self.act6()  # Game finished, do another activity...

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
        elif intentName == 'answer_play' and len(args) > 0:
            self.play = args[0]
            self.playLock.release()
        elif intentName == 'answer_yesno' and len(args) > 0:
            self.yesno = args[0]
            self.yesnoLock.release()
        elif intentName == 'answer_gamemove' and len(args) > 0:
            self.gamemove = args[0]
            if len(args) >= 2:
                self.number = args[1]
            self.gamemoveLock.release()
        elif intentName == 'answer_game' and len(args) > 0:
            self.game = args[0]
            self.gameLock.release()
        elif intentName == 'answer_finish' and len(args) > 0:
            self.finish = args[0]
            self.finishLock.release()


    def exit(self):
        sys.exit('Emergency exit')

    # Good morning
    def act1(self):
        self.reset()  # reset the variables
        self.speechLock = Semaphore(0)
        self.sayAnimated('Good morning {}. How are you feeling today?'.format(self.name))
        self.speechLock.acquire()
        self.animation(random.choice(self.bodygesture))  # performs a random animation from the given list


        while self.noAnswer and self.times != 3:

            self.mood = None
            self.moodLock = Semaphore(0)
            self.setAudioContext('answer_mood')
            self.startListening()
            self.moodLock.acquire(timeout=5)
            self.stopListening()

            if not self.mood:  # wait one more second after stopListening (if needed)
                self.moodLock.acquire(timeout=1)

            # Respond and wait for that to finish
            # multiple answers are detected, based on the Interaction Diagram created.
            if self.mood == "good":  # NAO detects positive answer, will proceed to the next phase
                self.sayAnimated("I am happy to hear that your are doing {}".format(self.mood))
                self.noAnswer = False
                self.animation(random.choice(self.happy))  # performs a random animation from the given list
            elif self.mood == "bad":  # NAO detects bad mood, will alert the caregiver
                self.sayAnimated("I am sorry to hear that you are {}. I will call the doctor.".format(self.mood))
                self.animation(random.choice(self.bad))
                self.sayAnimated("The doctor is on it's way.")
                self.animation(random.choice(self.bodygesture))  # performs a random animation from the given list
                self.exit()
            else:  # NAO will proceed at the next step after 2 failed attempts.
                if self.times == 2:
                    self.sayAnimated("Even after two tries, I still didn't figured it out. I guess we will go to the"
                                     "next point")
                    self.times += 1
                else:
                    self.sayAnimated(random.choice(self.responses))
                    self.times += 1
                self.animation(random.choice(self.bodygesture))  # performs a random animation from the given list

            self.speechLock.acquire()
            # time.sleep(1)

    # Do you want to play with me?
    def act2(self):
        self.reset()  # reset the variables
        self.speechLock = Semaphore(0)
        self.sayAnimated("Before we start the day, let's play a little game together.")
        self.speechLock.acquire()
        self.animation(random.choice(self.bodygesture))

        while self.noAnswer and self.times != 3:
            self.play = None
            self.playLock = Semaphore(0)
            self.setAudioContext('answer_play')
            self.startListening()
            self.playLock.acquire(timeout=5)
            self.stopListening()

            if not self.play:  # wait one more second after stopListening (if needed)
                self.playLock.acquire(timeout=1)

            # Respond and wait for that to finish
            if self.play == "yes":  # NAO detects positive answer, will proceed to the next phase
                self.sayAnimated("I like your enthusiasm, {}".format(self.name))
                self.noAnswer = False
                self.animation(random.choice(self.happy))
            elif self.play == "no":  # NAO detects answer
                self.sayAnimated("We don't want to miss this practice session, {}. This will help you. "
                                 "Let's play it!".format(self.name))
                self.noAnswer = False
                self.animation(random.choice(self.bad))
            else:  # NAO will proceed at the next step after 2 failed attempts.
                if self.times == 2:
                    self.sayAnimated("Even after two tries, I still didn't figured it out. I guess we will go to the"
                                     "next point")
                    self.times += 1
                else:
                    self.sayAnimated(random.choice(self.responses))
                    self.times += 1
                self.animation(random.choice(self.bodygesture))
            self.speechLock.acquire()


        # Display a gesture (replace <gestureID> with your gestureID)
        time.sleep(1)

    # Choosing the game
    def act3(self):
        self.reset()  # reset the variables

        self.speechLock = Semaphore(0)
        self.sayAnimated("What kind of game would you like to play?")
        self.speechLock.acquire()
        self.animation(random.choice(self.thinking))

        while self.noAnswer and self.times != 3:
            self.game = None
            self.gameLock = Semaphore(0)
            self.setAudioContext('answer_game')
            self.startListening()
            self.gameLock.acquire(timeout=5)
            self.stopListening()

            if not self.game:  # wait one more second after stopListening (if needed)
                self.gameLock.acquire(timeout=1)
            # print(self.game)
            # Respond and wait for that to finish
            if self.game == "numbers" or self.game == "random":
                self.sayAnimated("Let's play that, {}".format(self.name))
                self.noAnswer = False
                self.animation(random.choice(self.happy))
            elif self.game == "no" or self.game == "sudoku" or self.game == "random": # i don't know answer
                self.sayAnimated("I believe last time we played Sudoku, how about playing the numbers game?")
                self.noAnswer = False
                self.animation(random.choice(self.bad))
            else:  # NAO will proceed at the next step after 2 failed attempts.
                if self.times == 2:
                    self.sayAnimated("Even after two tries, I still didn't figured it out. I guess we will go to the"
                                     "next point")
                    self.times += 1
                else:
                    self.sayAnimated(random.choice(self.responses))
                    self.times += 1
                self.animation(random.choice(self.bodygesture))
            self.speechLock.acquire()


    # Start the game
    def act4(self):
        self.reset()
        self.speechLock = Semaphore(0)


        while self.noAnswer and self.times != 3:
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
                self.sayAnimated("Great, let's start, {}!".format(self.name))
                # self.speechLock.acquire()
                self.noAnswer = False
                self.animation(random.choice(self.happy))
            elif self.yesno == "no": # i don't know answer
                self.sayAnimated("We need to play it either way.")
                self.noAnswer = False
                self.animation(random.choice(self.bad))
            else:  # NAO will proceed at the next step after 2 failed attempts.
                if self.times == 2:
                    self.sayAnimated("Even after two tries, I still didn't figured it out. I guess we will go to the"
                                     "next point")
                    self.times += 1
                else:
                    self.sayAnimated(random.choice(self.responses))
                    self.times += 1
                self.animation(random.choice(self.bodygesture))
            self.speechLock.acquire()

    # Moves, ordering, etc...
    def act5(self):
        # In act5, the NAO will listen to 2 different type of answers from the patient simultaneously. One is the
        # answer regarding the game (if the patient made a correct move or not) and the other one is the user experience
        # where the NAO tries to identify previous experiences and add them into the discussion.
        self.reset()
        self.speechLock = Semaphore(0)
        self.sayAnimated("Remember {} the goal of the game is to place the numbers in the right order.".format(self.name))
        self.speechLock.acquire()
        self.animation(random.choice(self.bodygesture))

        while self.noAnswer and self.times != 3:

            if self.repeat > 0:
                self.speechLock = Semaphore(0)
                self.sayAnimated("Let's make another move.".format(self.name))
                self.speechLock.acquire()

            self.gamemove = None
            self.number = None
            self.gamemoveLock = Semaphore(0)
            self.setAudioContext('answer_gamemove')
            self.startListening()
            self.gamemoveLock.acquire(timeout=7)
            self.stopListening()

            if not self.gamemove:  # wait one more second after stopListening (if needed)
                self.gamemoveLock.acquire(timeout=1)

            # Respond and wait for that to finish
            if self.gamemove == "correct":
                self.sayAnimated("Yes, {}. You are doing great!".format(self.name))
                if self.repeat == 2:
                    self.noAnswer = False
                else:
                    self.repeat += 1
                self.animation(random.choice(self.happy))
            elif self.gamemove == "uncertain":
                self.sayAnimated("That is not completely correct, {}. Take a look at number {} and see if that is "
                                 "bigger with the number you have chosen.".format(self.name, np.random.randint(0, 100, 1)))
                self.animation(random.choice(self.thinking))
                if self.number is not None:
                    self.sayAnimated("By the way, {}".format(str(self.userExperience[int(self.number)])))
                    self.animation(random.choice(self.bodygesture))
                if self.repeat == 2:
                    self.noAnswer = False
                else:
                    self.repeat += 1

            elif self.gamemove == "wrong":
                self.sayAnimated("That is not correct, {}.".format(self.name))
                self.animation(random.choice(self.bad))
                if self.repeat == 2:
                    self.noAnswer = False
                else:
                    self.repeat += 1
            else:  # NAO will proceed at the next step after 2 failed attempts.
                if self.times == 2:
                    self.sayAnimated("Even after two tries, I still didn't figured it out. I guess we will go to the"
                                     "next point")
                    self.times += 1
                else:
                    self.sayAnimated(random.choice(self.responses))
                    self.times += 1
                self.animation(random.choice(self.bodygesture))
            self.speechLock.acquire()
            time.sleep(1)


    # Congratulations, it's time to say goodbye.
    def act6(self):
        self.reset()
        self.speechLock = Semaphore(0)
        self.sayAnimated("I'm fast forwarding to the end of the game.".format(self.name))
        time.sleep(2)
        self.sayAnimated("Congratulations {}, you finished the game and you did a good job.".format(self.name))
        self.animation(random.choice(self.finish))
        self.speechLock.acquire()

        while self.noAnswer and self.times != 3:
            self.finish = None
            self.finishLock = Semaphore(0)
            self.setAudioContext('answer_finish')
            self.startListening()
            self.finishLock.acquire(timeout=5)
            self.stopListening()

            if not self.finish:  # wait one more second after stopListening (if needed)
                self.finishLock.acquire(timeout=1)

            # Respond and wait for that to finish
            if self.finish == "finish":
                self.sayAnimated("Thank you as well. I will call the caregiver to help us pack the game! What do you "
                                 "think we should do next?".format(self.name))
                self.noAnswer = False
            else:  # NAO will proceed at the next step after 2 failed attempts.
                if self.times == 2:
                    self.sayAnimated("Even after two tries, I still didn't figured it out. I guess we will go to the"
                                     "next point")
                    self.times += 1
                else:
                    self.sayAnimated(random.choice(self.responses))
                    self.times += 1
            self.speechLock.acquire()


    def animation(self, gesture):

        # Display a gesture (replace <gestureID> with your gestureID)
        self.gestureLock = Semaphore(0)
        self.doGesture(gesture)
        self.gestureLock.acquire()
        time.sleep(1)

    def populate(self, path):
        with open(path) as f:
            lines = f.read().splitlines()
        return lines

# Run the application
sample = DialogFlowSampleApplication()
sample.main()
sample.stop()
