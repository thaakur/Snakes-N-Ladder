# Snakes and Ladders

# Import modules for later use.
from tkinter import *
import random 

# Define a new class, StarterApp, that will display the initial GUI with instructions to start the game.
class StarterApp(Tk):
    def __init__(self): # Initialize the GUI
        Tk.__init__(self)
        self.title('Snakes and Ladders') # Title the GUI
        self.grid() # Create grid
        self.createWidgets() # Create the widgets
    
    # Create the widgets
    def createWidgets(self):
        # Title Label
        label = Label(self,fg = 'dark green', font='Helvetica 60 bold', text='Snakes and Ladders')
        label.grid(row=0,column=0,columnspan=4,sticky=N+E+W+S)
        
        # Instructions Label; obtaining and cleaning data from textfile
        instructionList = []
        instructions = open('SnakesandLaddersInstructions.txt').readlines() # Opening text file
        for line in instructions:
            # Get rid of newline character
            line = line.strip('\n')
            instructionList.append(line)
        for i in range(0,len(instructionList)): # Reads in the instructions and adds as a label to GUI 
           instructionLabel = Label(self, fg='black', font='Helvetica 16', text=instructionList[i])
           instructionLabel.grid(row=4+i,column=2,columnspan=2,sticky=W)
        
        # Insert Snakes and Ladder Picture 
        pic = PhotoImage(file='starter.gif') # Get starter image
        imageLabel = Label(self, image=pic,borderwidth=0) # Create the label for image
        imageLabel.pic = pic # Set the image to the label
        imageLabel.grid(row=3,column=0,rowspan=8,sticky=N+E+W+S) # Position the image in GUI
        
        # Create Start New Game Button      
        startGameButton = Button(self, text='Start New Game',command=self.onStartGameButtonClick)
        startGameButton.grid(row=12,column=0,sticky=N+S)
        
        # Create Quit Game Button
        quitButton = Button(self, text='Quit',command=self.onQuitButtonClick)
        quitButton.grid(row=13,column=0,sticky=N+S)

    # Define instance method that destroys the starter GUI and invokes the gameBoard GUI for a new game
    def onStartGameButtonClick(self):
        self.destroy() # Destroy starter (current) GUI
        self.m_app = gameBoard() # Launch gameBoard GUI
        self.m_app.mainloop()
        
    # Define instance method that destroys the GUI when the quit button is clicked    
    def onQuitButtonClick(self):
        self.destroy()

# Define a new class gameBoard that will create the GUI with the game board, game pieces, move the game pieces
# accordingly and check if the game is over.
class gameBoard(Tk):
    def __init__(self): # Initialize GUI
        Tk.__init__(self)
        self.GIF_width = 590  # Set width of GIF
        self.GIF_height = 708 # Set height of GIF
        self.numRows = 12 # Set the number of rows
        self.numCols = 10 # Set the number of columns
        self.cellHeight = 53 # Set the max and min grid cell height 
        self.cellWidth = 53 # Set the max and min grid cell width
        self.minsize(width=self.GIF_width, height=self.GIF_height) # Set the minimum size of the GUI so it won't change
        self.maxsize(width=self.GIF_width, height=self.GIF_height) # Set the maximum size of the GUI so it won't change
        self.title('Snakes and Ladders') # Set the title
        self.grid() # Create a grid
        self.createWidgets() # Create the widgets
        self.isUserTurn = True # Create Boolean to check which player's turn it is
        self.isPaused = False # Create boolean to check if the game has been paused before
        self.isGameOver = False # Create Boolean to check if the game is over
        self.dict = {(5,0):(2,0),(2,3):(1,3),(4,3):(7,2),(8,6):(3,6),(0,8):(3,7),(5,7):(8,7)} # Create a dictionary
                                                                # where the keys are beginning positions of the snakes
                                                                # and ladders and the values are the ending positions
    
    # Create the widgets
    def createWidgets(self):
        # Create grid of blank widgets behind the background image
        for i in range(self.numRows):
            for j in range(self.numCols):
                # For each row and column, create a blank widget
                self.blank = Canvas(self, width=self.cellWidth, height=self.cellHeight)
                self.blank.grid(row=i, column=j)
        
        # Create background image
        pic = PhotoImage(file='SnakesAndLadders.gif') # Get game board image
        imageLabel = Label(self, image=pic) # Create the label for the image
        imageLabel.pic = pic # Set the label to the image
        imageLabel.place(x=0, y=0, relwidth=1, relheight=1) # Position the image in GUI

        # Create Roll Dice Button with command
        self.rollButton = Button(self,text= 'Roll the dice!', command = self.diceRollClick)
        self.rollButton.grid(row=11,column=1,columnspan=3) # Position button
        
        # Create Start Game Button with command
        self.startButton = Button(self,text = 'Start New Game',command = self.onStartButtonClick)
        self.startButton.grid(row=10,column=7,columnspan=2,sticky=N+E+W+S) # Position button
        
        # Create Quit Button with command
        self.quitButton = Button(self, text = 'Quit',command = self.onQuitButtonClick)
        self.quitButton.grid(row=11,column=7,columnspan=2,sticky=N+E+W+S) # Position button
        
        # Create Status Label
        self.status = StringVar() # Set to StringVar() so we can change the status later.
        self.statusLabel = Label(self,font='Verdana 16',textvariable=self.status) # Create label
        self.statusText = 'It\'s your turn!' # Set beginning status
        self.status.set(self.statusText)
        self.statusLabel.grid(row=10,columnspan=6,sticky=N+E+W+S) # Position label
        
        # Create Pause Key
        self.bind('p',self.pKey) # Bind the 'p' keyboard key with a command
        
        # Create Computer Game Piece
        computerPic = PhotoImage(file = 'computer.gif') # Get computer's game piece image
        self.comImage = Label(self, image = computerPic) # Create the label for the image
        self.comImage.pic = computerPic # Set the label to the image
        self.comRow = IntVar() # Make IntVar() to keep track of position and change after rolling dice.
        self.comRow = 9 # This is the beginning starter position; Same as user--we want pieces to overlap.
        self.comCol = IntVar() # Make IntVar() to keep track of position and change after rolling dice.
        self.comCol = 0 # This is the beginning starter position; Same as user--we want pieces to overlap.
        self.comImage.grid(row=self.comRow,column=self.comCol) # Position the image in GUI
        
        # Create User Game Piece
        userPic = PhotoImage(file = 'player.gif') # Get user's game piece image
        self.userImage = Label(self, image = userPic) # Create the label for the image
        self.userImage.pic = userPic # Set the label to the image
        self.userRow = IntVar() # Make IntVar() to keep track of position and change after rolling dice.
        self.userRow = 9 # This is the beginning starter position; Same as user--we want pieces to overlap.
        self.userCol = IntVar() # Make IntVar() to keep track of position and change after rolling dice.
        self.userCol = 0 # This is the beginning starter position; Same as user--we want pieces to overlap.
        self.userImage.grid(row=self.userRow,column=self.userCol) # Position the image in GUI
        
    # Define an instance method that gives a number on a dice for which the game piece will move to.
    def diceRolling(self):
        return random.randint(1,6)
        
     # Define instance method. This will update the status of the rolled dice and which player's turn, also moving
     # the game pieces according to the rolled dice.
    def diceRoll(self,x,y,player):
        deltaX = self.diceRolling() # Get how many spaces the piece should advance; Call instance method defined above
        if player == self.userImage: # Check which player it is.
            self.statusText = 'Your dice rolled: ' + str(deltaX) + '. It\'s Computer\'s turn!' # If it is the user, set
                                                    # status telling user of result and that computer is next
        else:
            self.statusText = 'Computer\'s dice rolled: ' + str(deltaX) + '. It\'s your turn!' # If it is the computer,
                                                    # set status telling user of computer's result and that user is next
        self.status.set(self.statusText) # Update status
        if x == 0 and (y - deltaX) <= 0: # If game piece is on the final row and is at or passes the final square make
                                                                        # the game piece stay at the final square
            y = 0
            player.grid(row=x,column=y)
        else: # If not, then follow code below:
            if x%2 != 0: # Check if the row is odd
                # If the row is odd, and the spaces to advance does not exceed columns, move pieces to the right.
                if (y + deltaX) < self.numCols:
                    y += deltaX # Define new column position
                    player.grid(row=x,column=y) # Reposition player piece
                # If the spaces to advance exceeds columns, move piece up in row and move piece left (since will be an
                # even row) according to the remaining pieces after the piece moved in the row below
                else:
                    remain = self.numCols-y-1 # Find remaining column for new column position
                    x = x - 1 # Move up in row
                    y = self.numCols - (deltaX - remain) # Define new column position
                    player.grid(row=x,column=y) # Reposition player piece
            else: # If the row is even:
                if (y - deltaX) >= 0: # If the spaces to advance does not exceed columns, move pieces to the left.
                    y = y - deltaX # Define new column position
                    player.grid(row=x,column=y) # Reposition player piece
                # If the spaces to advance exceeds columns, move piece up in row and move piece right (since will be an
                # odd row) according to the remaining pieces after piece moved in the row below
                else: 
                    x -= 1 # Move up in row
                    y = deltaX - y - 1 # Define new column position/ Find remaining column for new column position
                    player.grid(row=x,column=y) # Reposition player
            if self.isUserTurn: # Check which player the game piece is moved
                self.userRow = x # If it is the users, then update the user's row and column
                self.userCol = y
            else:
                self.comRow = x # If it is the computer's, then update the computer's row and column
                self.comCol = y
        self.handleGameOver(x,y,player) # Check if the position of the player is where the game wins after each turn

    # Define the instance method that links the rollButton with moving the game pieces.
    def diceRollClick(self):
        if self.isUserTurn: # Check if it is the user's turn
            self.diceRoll(self.userRow, self.userCol, self.userImage) # Move game piece by calling on previous method
            self.checkIf(self.userRow,self.userCol,self.userImage) # Check if the game piece is at a snake or ladder
                                                                    # and move accordingly
            if not self.isGameOver: # Check if the game is over and if the GUI has been destroyed before trying to
                                    # change the button's text
                self.rollButton.configure(text='See Computer\'s Move') # Change the button for computer's turn
            self.isUserTurn = False # No longer user's turn. It is Computer's turn
        else: # If it is computer's turn
            self.diceRoll(self.comRow,self.comCol, self.comImage) # Move the game piece by calling on previous method
            self.checkIf(self.comRow,self.comCol,self.comImage) # Check if the game piece is at a snake or ladder
                                                                    # and move accordingly
            if not self.isGameOver: # Check if the game is over and if the GUI has been destroyed before trying to
                                    # change the button's text
                self.rollButton.configure(text='Roll the dice!') # Change the button for computer's turn
            self.isUserTurn = True # No longer Computer's turn. It is user's turn
    
    # Define an instance method that checks if the game piece is at a snake or ladder and if so, moves it accordingly.;
    # To be invoked in diceRollClick
    def checkIf(self,row,col,imageLabel):
        pos = (row,col) # New syntax to see if it is in the key of dictionary
        if pos in self.dict:
            value = self.dict[pos] # Get value that pertains to key
            newRow = value[0] # Get row from tuple
            newCol = value[1] # Get column from tuple
            imageLabel.grid(row=newRow,column=newCol)
            if imageLabel == self.userImage:
                self.userRow = newRow
                self.userCol = newCol
            else:
                self.comRow = newRow
                self.comCol = newCol
                
    # Define instance method that checks if the game is over; to be invoked by diceRoll
    def handleGameOver(self,row,column,player):
        if row == 0 and column == 0: # Check if the game piece is at the final square
            self.isGameOver = True # Change boolean to indicate the game is over
            self.destroy() # Destroy gameBoard (current) GUI
            if player == self.userImage: # Check if it is the user who won
                self.m_app = CongratsGUI('user') # Launch GUI that congratulates user
            else: # If the computer won
                self.m_app = CongratsGUI('computer') # Launch GUI that tells user he/she lost
            self.m_app.mainloop()
    
    # Define instance method that destroys the gameBoard GUI and invokes the starter GUI for a new game
    def onStartButtonClick(self):
        self.destroy() # Destroy gameBoard (current) GUI
        self.m_app = StarterApp() # Launch starter GUI
        self.m_app.mainloop()
        
    # Define instance method that destroys the GUI when the quit button is clicked
    def onQuitButtonClick(self):
        self.destroy()
    
    # Define instance method that pauses the game when the p button is clicked
    def pKey(self,event):
        if not self.isGameOver: # Check if the game is over
            if not self.isPaused: # If game is not over and the game is not currently paused, then disable all buttons
                self.quitButton.configure(state='disabled')
                self.rollButton.configure(state='disabled')
                self.startButton.configure(state='disabled')
                self.isPaused = True # Change the boolean so that the game is paused
            else: # If the game is not over and the game is currently paused, then enable all buttons
                self.quitButton.configure(state='normal')
                self.rollButton.configure(state='normal')
                self.startButton.configure(state='normal')
                self.isPaused = False # Change the boolean so that the game is not paused

# Define a new class, CongratsGUI, that will display the final GUI telling the user if the user won or lost once the
# game is over.
class CongratsGUI(Tk):
    def __init__(self,winner): # Initialize GUI - Takes argument winner
        Tk.__init__(self)
        self.title('Snakes and Ladders') # Title the GUI
        self.grid() # Create grid
        self.createWidgets(winner) # Create the widgets: Takes argument winner that will be utilized in creating the GUI
    
    # Define an instance method that will create the image and text label
    def makeimageLabel(self,image,words):
        for i in range(0,2): # Loop through twice to place the same image twice but in different rows and columns
            pic = PhotoImage(file=image) # Get the image
            picLabel = Label(self, image=pic,borderwidth=0) # Create Label for image
            picLabel.pic = pic # Set the image to the label
            picLabel.grid(row=0,column=2*i,rowspan=3,sticky=N+E+W+S) # Position the image
        # Create text label
        self.congratsLabel = Label(font='Verdana 18 bold',text=words)
        self.congratsLabel.grid(row=0,column=1,sticky=N+S)
        
   # Create the widgets 
    def createWidgets(self,winner):
        # Create Start New Game Button      
        startGameButton = Button(self, text='Start New Game',command=self.onStartGameButtonClick)
        startGameButton.grid(row=1,column=1,sticky=N+S)
        
        # Create Quit Game Button
        quitButton = Button(self, text='Quit',command=self.onQuitButtonClick)
        quitButton.grid(row=2,column=1,sticky=N+S)
        
        # Check if the winner is the user
        if winner == 'user':
            self.makeimageLabel('congrats.gif','Congratulations, you won!') # If so, create the congratulations GUI
        else: # If the winner is the computer
            self.makeimageLabel('sorry.gif','Sorry, you lost!') # Create the sorry GUI
            
    # Define instance method that destroys the current GUI and invokes the starter GUI for a new game
    def onStartGameButtonClick(self):
        self.destroy() # Destroy congratsGUI (current) GUI
        self.m_app = StarterApp() # Launch starter GUI
        self.m_app.mainloop()
            
    # Define instance method that destroys the GUI when the quit button is clicked    
    def onQuitButtonClick(self):
        self.destroy() # Destroy congratsGUI (current) GUI
    
# Run the GAME!
app = StarterApp()
app.mainloop()
