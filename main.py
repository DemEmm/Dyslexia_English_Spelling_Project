import csv
import pandas as pd
import os
import pyttsx3 as sx
from googletrans import Translator
import json
import time
from playsound import playsound


# --- UI ---

class User:
    def __init__(self,Username,Userlevel,scv_path,json_path):
        self.name = Username
        self.level = Userlevel
        self.csv_path = scv_path
        self.json_path = json_path

    def User_level_up(self):
        self.level += 1
        data = {
            "Name": self.name,
            "Level": self.level,
            "csv_path": self.csv_path,
            "json_path": self.json_path
        }

        # Save dictionary as JSON file
        with open(self.json_path, "w") as file:
            json.dump(data, file, indent=4)  # indent=4 makes it pretty formatted

def invitation():
    """"This function ask for the user. If user exists get the file path. if it doesn't generate a new file for him and
    a new path in order to have a lerning history"""

    username = input("give me your user name:")

    Prototype_path = "./Files/Prototype.csv"
    usre_file_path_csv = f"Users/{username}.csv"
    usre_file_path_json = f"Users/{username}.json"
    if not os.path.exists(usre_file_path_csv):
        #Creates the Columns mistakes and in the prototype file

        df = pd.read_csv(Prototype_path)
        df = df[df["word"].str.len() > 2] #remove all words with spesific length
        df['mistakes'] = 5
        df['eval'] = df["count"] / df['count'].sum() #calculates word value
        df.to_csv(usre_file_path_csv) #save file

        data = {
            "Name": f"{username}",
            "Level": 1,
            "csv_path": usre_file_path_csv,
            "json_path": usre_file_path_json
        }

        # Save dictionary as JSON file
        with open(usre_file_path_json, "w") as file:
            json.dump(data, file, indent=4)  # indent=4 makes it pretty formatted

        My_user = User(username, 1, usre_file_path_csv, usre_file_path_json)
        print("this User doesn't exist and Created")
    else:
        with open(usre_file_path_json, "r") as file:
            data = json.load(file)
            My_user = User(data["Name"], data["Level"],usre_file_path_csv,usre_file_path_json)
        print("User exist")

    return My_user

def generate_word(df):
    """get a df and choose the word in order to lern.
    retunrs word"""
    df_magic_word = df["word"].sample(n=1, weights=df["eval"]) #.samples gets random row with Specifies sampling weight per item. Higher weight increases sampling probability.
    my_magic_word = df_magic_word.iloc[0]
    my_magic_word_pos = df_magic_word.index[0]

        # if len(my_magic_word) > 2:
        #     break
    return my_magic_word,my_magic_word_pos

def speeker(my_magic_word):
    eng.say(my_magic_word)
    eng.runAndWait()

def Translate_prosidure(my_magic_word,translator):
    """"Say the magic word"""
    try:
        translated_text = translator.translate(my_magic_word, src='en', dest='el')
        print(f"Translated: {translated_text.text}")
    except Exception as e:
        print(f"Translation error: {e}")

def word_checker(my_magic_word,my_magic_word_pos,df):
    my_magic_word_answer = input("give me the wright word: \n")

    if my_magic_word == my_magic_word_answer:
        df.loc[my_magic_word_pos,"mistakes"] -= 1
        df['eval'] = df["count"] * df['mistakes'] / df['count'].sum()
        print(df.loc[my_magic_word_pos,"mistakes"])
        print(df.loc[my_magic_word_pos, "eval"])
        playsound("Speech On.wav")
    else:
        while my_magic_word != my_magic_word_answer:
            speeker(my_magic_word)
            print(f"{my_magic_word}")
            df.loc[my_magic_word_pos,"mistakes"] += 1
            df['eval'] = df["count"] * df['mistakes'] / df['count'].sum()
            print(df.loc[my_magic_word_pos, "mistakes"])
            print(df.loc[my_magic_word_pos, "eval"])
            my_magic_word_answer = input("give me the wright word: \n")

    print(df)

if __name__ == "__main__":
    playsound("Speech On.wav")
    My_user = invitation()

    df = pd.read_csv(My_user.csv_path)


    df = df.iloc[:5*My_user.level,:]

    """
    A1	~500–1,000	    ~750
    A2	~1,000–2,000	~1500
    B1	~2,000–4,000	~3000
    B2	~4,000–8000	    ~6000
    C1	~8000–10,000	~9000
    C2	~10,000–20,000+	~15000
    """

    translator = Translator()  # Generate Translator engin
    eng = sx.init()  # set up speeker engine
    eng.setProperty('rate', 90)  # set up the speed of speaker at 120 rate

    my_magic_word_answer = ""

    while my_magic_word_answer != "exit":

        my_magic_word,my_magic_word_pos = generate_word(df) #generate magic word
        print(f"My magic words position: {my_magic_word_pos}")
        start = time.time()
        speeker(my_magic_word)
        mtime = time.time()-start
        print(f"this is my time : {mtime}")
        # Translate_prosidure(my_magic_word,translator)

        word_checker(my_magic_word,my_magic_word_pos,df)
        if df["mistakes"].sum() < 5 :
            My_user.User_level_up()
            df = pd.read_csv(My_user.csv_path)
            df = df.iloc[:5 * My_user.level, :]


    print("end")
