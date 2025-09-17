import csv
import pandas as pd
import os
import pyttsx3 as sx
from googletrans import Translator
import json
import time
from playsound import playsound
  
"""
A1	~500–1,000	    ~750
A2	~1,000–2,000	~1500
B1	~2,000–4,000	~3000
B2	~4,000–8000	    ~6000
C1	~8000–10,000	~9000
C2	~10,000–20,000+	~15000
"""

def invitation():
    """"This function ask for the user. If user exists get the file path. if it doesn't generate a new file for him and
    a new path in order to have a lerning history also create a json with his progres level"""

    username = input("give me your user name:")

    Prototype_path = "./Files/Prototype.csv"
    usre_file_path_csv = f"Users/{username}.csv"
    usre_file_path_json = f"Users/{username}.json"

    if not os.path.exists(usre_file_path_csv):
        # Creates the Columns mistakes and in the prototype file

        df = pd.read_csv(Prototype_path)
        df = df[df["word"].str.len() > 2]  # remove all words with spesific length
        df['mistakes'] = 5.0
        df['eval'] = df["count"] / df['count'].sum()  # calculates word value
        df.to_csv(usre_file_path_csv)  # save file

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
            My_user = User(data["Name"], data["Level"], usre_file_path_csv, usre_file_path_json)
        print("User exist")

    return My_user

def speeker(my_magic_word):
    eng.say(my_magic_word)
    eng.runAndWait()

def Translate_prosidure(my_magic_word, translator):
    """"Say the magic word"""
    try:
        translated_text = translator.translate(my_magic_word, src='en', dest='el')
        print(f"Translated: {translated_text.text}")
    except Exception as e:
        print(f"Translation error: {e}")

def word_checker(my_magic_word, my_magic_word_pos, df):
    """Ask user for the wrigt answer in oreder to compear it with the wright word"""
    my_magic_word_answer = input("give me the wright word: \n")

    if my_magic_word == my_magic_word_answer:
        df.loc[my_magic_word_pos, "mistakes"] = df.loc[my_magic_word_pos, "mistakes"] * 0.7
        df['eval'] = df["count"] * df['mistakes'] / df['count'].sum()
        print(df.loc[my_magic_word_pos, "mistakes"])
        print(df.loc[my_magic_word_pos, "eval"])
        playsound("Speech On.wav")
    else:
        df.loc[my_magic_word_pos, "mistakes"] = df.loc[my_magic_word_pos, "mistakes"] * 1.5
        df['eval'] = df["count"] * df['mistakes'] / df['count'].sum()
        print(df.loc[my_magic_word_pos, "mistakes"])
        print(df.loc[my_magic_word_pos, "eval"])
        playsound("Speech Off.wav")
    print(df)
    return my_magic_word_answer


class Teacher:
    def __init__(self,student):
        self.student = student
        self.test_df = self.student.df.iloc[:3 * self.student.level, :]
        self.my_magic_word = ""
        self.my_magic_word_pos = 0
        self.my_magic_word_answer = ""
        self.generate_word()
        self.mode = "brute"
        
    def generate_word(self):
        """get a df and choose the word in order to lern.
        retunrs word"""
        
        df_magic_word = self.test_df["word"].sample(n=1, weights=self.test_df["eval"])  # .samples gets random row with Specifies sampling weight per item. Higher weight increases sampling probability.
        self.my_magic_word = df_magic_word.iloc[0]
        self.my_magic_word_pos = df_magic_word.index[0]
        
    def word_checker(self):
        """Ask user for the wrigt answer in oreder to compear it with the wright word"""
        
        self.my_magic_word_answer = input("give me the wright word: \n")
        
        if self.my_magic_word == self.my_magic_word_answer:
            self.test_df.loc[self.my_magic_word_pos, "mistakes"] = self.test_df.loc[self.my_magic_word_pos, "mistakes"] * 0.2
            self.test_df['eval'] = self.test_df["count"] * self.test_df['mistakes'] / self.test_df['count'].sum()
            print(self.test_df.loc[self.my_magic_word_pos, "mistakes"])
            print(self.test_df.loc[self.my_magic_word_pos, "eval"])
            playsound("Speech On.wav")
        else:
            self.test_df.loc[self.my_magic_word_pos, "mistakes"] = self.test_df.loc[self.my_magic_word_pos, "mistakes"] * 1.5
            self.test_df['eval'] = self.test_df["count"] * self.test_df['mistakes'] / self.test_df['count'].sum()
            print(self.test_df.loc[self.my_magic_word_pos, "mistakes"])
            print(self.test_df.loc[self.my_magic_word_pos, "eval"])
            playsound("Speech Off.wav")
        print(self.test_df)
        
    def level_checker(self):
        print(self.test_df["mistakes"].sum())
        print(len(self.test_df["mistakes"])*1.9)
        if self.test_df["mistakes"].sum() < len(self.test_df["mistakes"])*1.9:
            print("LEEEV")
            self.student.User_level_up()
            self.mode_create_df()
    def mode_create_df(self):
        match self.mode:
            case "brute":
                df = pd.read_csv(self.student.csv_path)
                print(df.iloc[0:len(self.test_df)])
                df.iloc[0:len(self.test_df)] = self.test_df
                df.to_csv(self.student.csv_path)  # afto prepi na alxi apo edo !!!!!!
                df = df.iloc[:3 * self.student.level, :]
                self.test_df = df
                print(self.test_df)
            case "window":
                print("NA")
                pass
class User:
    def __init__(self, Username, Userlevel, scv_path, json_path):
        self.name = Username
        self.level = Userlevel
        self.csv_path = scv_path
        self.json_path = json_path
        self.df = pd.read_csv(scv_path)

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


if __name__ == "__main__":
    playsound("Speech On.wav")
    
    My_user = invitation()
    My_teacher = Teacher(My_user)

    translator = Translator()  # Generate Translator engin
    eng = sx.init()  # set up speeker engine
    eng.setProperty('rate', 90)  # set up the speed of speaker at 120 rate

    #my_magic_word_answer = ""
    Program_ends = True

    while Program_ends:

        My_teacher.generate_word()  # generate magic word
        print(f"My magic words position: {My_teacher.my_magic_word_pos}")
        speeker(My_teacher.my_magic_word)
        #Translate_prosidure(my_magic_word, translator)

        My_teacher.word_checker()
        print(My_teacher.my_magic_word_answer)
        My_teacher.level_checker()
        
        
        
        match My_teacher.my_magic_word_answer:
            case "exit":
                Program_ends = False
            case "!":
                pass
                
