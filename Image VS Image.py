from tkinter import *
from PIL import ImageTk, Image  # This does get used, it just has to be (exec)'ed into necessity
import os


# This is what runs the program and the top bar image and title
root = Tk()
root.title("Image Selection")
root.iconbitmap("image.ico")

# This opens the images folder in the DIR and lists the files ending in .jpg and makes a list empty for post processing
image_list = [f.name for f in os.scandir("images") if f.name.endswith('.jpg')]
image_list_dir = []

# Processing, the names get their (hard coded) file directory put in front of the names, now its the image and path
for images in image_list:
    images = "images/" + images
    image_list_dir.append(images)

# Okay, this one is tricky. This makes a list of commands (more processing)
# This will make a list of code that tells ImageTk to open the images that have their folder paths added
command_list = []
for i in range(len(image_list_dir)):
    command_list.append("i" + str(i + 1) + " = ImageTk.PhotoImage(Image.open('" + str(image_list_dir[i]) + "'))\n")

# The code has added a \n to the end so when they are made a string the list will make new lines instead of new items
code = "".join(command_list)

# This makes the paragraph of text a code instead of a string.
# Dynamically loading images based off their presence in a folder
exec(code)

# Okay it gets fun here too. Even though the images are now loaded easily enough they still have to be called after
# They will all be called i# and called as needed in a future label
image_list_last = []
for i in range(1, (len(image_list) + 1)):
    string = "i" + str(i)
    image_list_last.append(string)

# image_list was used in the beginning for pre-processing, but I want to use it again now, so I just update it to be
# what is was originally mean to hold, a list of images to call
image_list = image_list_last

# This takes the list of images (strings) and makes them variables through some steps
# First is to make a list again but as one string to remove '' from the list
lines = ""
for i in range(len(image_list)):
    line = "i" + str(i + 1) + ","
    lines = lines + line

# Then to clean it up we remove the last comma, and make a string called image_list = [ ... ]
# This is the same as the previous image list but without the ''
lines = lines[:-1]
lines = "image_list = [" + lines + "]"

# new_interp_list is a holder, interp will be the variable that holds the actual code (which is image_list=[...])
new_interp_list = "interp = " + lines

# This is how the mess ends, The new exec code makes the final part. The folder is read, files are logged, opened, and
# identified in a list that can be called using i#
exec(new_interp_list)

i = 0  # This is so we start at the first image in image_list[i]
loop_length = (len(image_list) / 2)  # First round of 2 pics at a time should be half the amount

# This makes the two image items exist and placed them for the first time
my_Label_1 = Label(root, image=image_list[i])
my_Label_2 = Label(root, image=image_list[i + 1])
my_Label_1.grid(row=0, column=0)
my_Label_2.grid(row=0, column=1)


def funct_A():
    # Global Variables, so they work between functions
    global i
    global my_Label_1
    global my_Label_2
    global loop_length
    global button_1
    global button_2

    # Forget the images up there and get ready for new ones
    my_Label_1.grid_forget()
    my_Label_2.grid_forget()

    # If A(i) is picked, remove image B(i + 1)
    image_list.remove(image_list[i + 1])

    # With one picture removed, adding 1 to i moves us for the next 2 images in line, otherwise "A" stays too
    i = i + 1

    # Time to chek how many other pictures there are
    if len(image_list) > 1:
        # This means there is still list to go through
        loop_length = int(loop_length)  # This gets rid of the decimal an odd list makes
        if i == loop_length:
            # this would happen when you are on the last item in your list
            i = 0  # This would restart the list
            loop_length = (len(image_list) / 2)  # and this would figure out how long the reduced restarted list is

        # This puts the new images up
        my_Label_1 = Label(image=image_list[i], pady=10)
        my_Label_2 = Label(image=image_list[i + 1], pady=10)
        my_Label_1.grid(row=0, column=0)
        my_Label_2.grid(row=0, column=1)
    else:
        # This would happen where there is one image left so it displays it
        my_Label_1 = Label(image=image_list[0], pady=10)
        my_Label_1.grid(row=0, column=0)
        # This will turn the buttons off where there is only one image left
        button_1 = Button(text="A", command=funct_A, state=DISABLED, pady=20, padx=20).grid(row=1, column=0)
        button_2 = Button(text="B", command=funct_B, state=DISABLED, pady=20, padx=20).grid(row=1, column=1)


def funct_B():
    global i
    global my_Label_1
    global my_Label_2
    global loop_length
    global button_1
    global button_2
    my_Label_1.grid_forget()
    my_Label_2.grid_forget()
    image_list.remove(image_list[i])
    i = i + 1
    if len(image_list) > 1:
        loop_length = int(loop_length)
        if i == loop_length:
            i = 0
            loop_length = (len(image_list) / 2)
        elif len(image_list) == 1:
            my_Label_1 = Label(image=image_list[0], pady=10)
        my_Label_1 = Label(image=image_list[i], pady=10)
        my_Label_2 = Label(image=image_list[i + 1], pady=10)
        my_Label_1.grid(row=0, column=0)
        my_Label_2.grid(row=0, column=1)
    else:
        my_Label_1 = Label(image=image_list[0], pady=10)
        my_Label_1.grid(row=0, column=0)
        button_1 = Button(text="A", command=funct_A, state=DISABLED, pady=20, padx=20).grid(row=1, column=0)
        button_2 = Button(text="B", command=funct_B, state=DISABLED, pady=20, padx=20).grid(row=1, column=1)


# This makes the buttons that select A or B using the symmetrical functions fucnt_A and funct_B
button_1 = Button(text="A", command=funct_A, pady=20, padx=20).grid(row=1, column=0)
button_2 = Button(text="B", command=funct_B, pady=20, padx=20).grid(row=1, column=1)


root.mainloop()
