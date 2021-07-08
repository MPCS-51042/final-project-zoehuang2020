import tkinter as tk
from tkinter import *
import pandas as pd
from tkinter import ttk
from tkinter import messagebox
from Plot_by_time import plot_by_time
from course_eval import difficulty, rating, scoring
from Degree_Requirement import core_course_selection, electives_course_selection, find_prerequisite

root = tk.Tk()
root.title("Booth Course Planner")
root.geometry("1200x1000")

my_notebook = ttk.Notebook(root)
my_notebook.pack(pady=15)

# read in all the data tables
df_degree_requirement = pd.read_excel('Degree Requirement.xlsx', sheet_name="Degree Requirement")
df_concentration_courses = pd.read_excel('Degree Requirement.xlsx', sheet_name="Concentrations")
df_concentration_requirement = pd.read_excel('Degree Requirement.xlsx', sheet_name="Concentration Requirement")
df_course_eval = pd.read_excel('course_evals.xlsx', sheet_name="Course Evaluations")
course_hour_ratings_summary = pd.DataFrame(
    df_course_eval.groupby(["Course"]).agg({'Q. 1 HRS /WK': "mean", "Q. 6 REC COURSE": 'mean'}).reset_index())

# Evaluate whether a course is "easy" or "hard" based on hours per week
difficulty_range = pd.DataFrame(course_hour_ratings_summary["Q. 1 HRS /WK"].quantile([0.25, 0.5, 0.75]))
easy_cut = list(difficulty_range["Q. 1 HRS /WK"])[0]
medium_cut = list(difficulty_range["Q. 1 HRS /WK"])[1]
hard_cut = list(difficulty_range["Q. 1 HRS /WK"])[2]
course_hour_ratings_summary["difficulty"] = difficulty(course_hour_ratings_summary['Q. 1 HRS /WK'], easy_cut,
                                                       medium_cut, hard_cut)
# Evaluate whether a course is "good" or "bad" based on student ratings
rating_range = pd.DataFrame(course_hour_ratings_summary["Q. 6 REC COURSE"].quantile([0.33, 0.66]))
bad_cut = list(rating_range["Q. 6 REC COURSE"])[0]
good_cut = list(rating_range["Q. 6 REC COURSE"])[1]
course_hour_ratings_summary["rating"] = rating(course_hour_ratings_summary['Q. 6 REC COURSE'], bad_cut, good_cut)

# Join degree required courses with rating
df_degree_requirement = df_degree_requirement.merge(course_hour_ratings_summary, left_on="Course Code",
                                                    right_on="Course", how="left")
df_degree_requirement["difficulty"] = df_degree_requirement["difficulty"].fillna("No Rating Available")
df_degree_requirement["rating"] = df_degree_requirement["rating"].fillna("No Rating Available")
df_degree_requirement["Score"] = scoring(df_degree_requirement["rating"], df_degree_requirement["difficulty"])

# build buttons for course recommendations
###############################################
# start with foundation courses
###############################################
foundation_frame = Frame(my_notebook, bg="pink")
difficulty_option_foundation = {"super hard": 0, "hard": 0, "easy": 0, "super easy": 0}

rating_option_foundation = {"Bad class,avoid!": 0, "OK class": 0, "Great class!": 0}


def foudation_recommendation():
    diff_variable = [diff for diff in difficulty_option_foundation if difficulty_option_foundation[diff].get() == "1"]
    rate_variable = [rate for rate in rating_option_foundation if rating_option_foundation[rate].get() == "1"]
    try:
        foundation_courses = core_course_selection(df_degree_requirement, "Foundation", 3, diff_variable,
                                                   rate_variable)
        tree = ttk.Treeview(foundation_frame)
        cols = list(foundation_courses.columns)
        tree["columns"] = list(foundation_courses.columns)
        for i in cols:
            tree.column(i, anchor="w")
            tree.heading(i, text=i, anchor='w')

        for index, row in foundation_courses.iterrows():
            tree.insert("", 0, text=index, values=list(row))
        tree.pack(fill='both')
    except:
        messagebox.showerror("Things don't always work out", "Can't find courses for you :(, try adding more "
                                                             "selections to difficulty and ratings")


# Create text widget and specify size.
foudation_text = Label(foundation_frame, text="Let us start with 3 foundation courses", bg="pink")
foudation_text.config(font=("Courier", 16))
foudation_text.pack()

# Create label
course_difficulty_text = Label(foundation_frame, text="Select the difficulty levels of your course", bg="pink")
course_difficulty_text.config(font=("Courier", 14))
course_difficulty_text.pack()

for selection in difficulty_option_foundation:
    difficulty_option_foundation[selection] = Variable()
    difficulty_selection = Checkbutton(foundation_frame, text=selection,
                                       variable=difficulty_option_foundation[selection])
    difficulty_selection.pack()

course_ratings_text = Label(foundation_frame, text="Select the ratings of your course", bg="pink")
course_ratings_text.config(font=("Courier", 14))
course_ratings_text.pack()

for selection in rating_option_foundation:
    rating_option_foundation[selection] = Variable()
    rating_selection = Checkbutton(foundation_frame, text=selection, variable=rating_option_foundation[selection])
    rating_selection.pack()

foundation_button = Button(foundation_frame, text="Click here and I will populate a foundation course "
                                                  "recommendation for you",
                           command=foudation_recommendation, bg="pink")
foundation_button.pack(pady=20)

foundation_frame.pack()
my_notebook.add(foundation_frame, text="Foundation Course Planer")
###############################################
# build recommendation for  6 function courses
###############################################
function_frame = Frame(my_notebook, bg="green")
difficulty_option_function = {"super hard": 0, "hard": 0, "easy": 0, "super easy": 0}

rating_option_function = {"Bad class,avoid!": 0, "OK class": 0, "Great class!": 0}


def function_recommendation():
    diff_variable = [diff for diff in difficulty_option_function if difficulty_option_function[diff].get() == "1"]
    rate_variable = [rate for rate in rating_option_function if rating_option_function[rate].get() == "1"]
    try:
        function_courses = core_course_selection(df_degree_requirement,
                                                 "Functions, Management, and the Business Environment",
                                                 6, diff_variable,
                                                 rate_variable)
        tree = ttk.Treeview(function_frame)
        cols = list(function_courses.columns)
        tree["columns"] = list(function_courses.columns)
        for i in cols:
            tree.column(i, anchor="w")
            tree.heading(i, text=i, anchor='w')

        for index, row in function_courses.iterrows():
            tree.insert("", 0, text=index, values=list(row))
        tree.pack(fill='both')
    except:
        messagebox.showerror("Things don't always work out", "Can't find courses for you :(, try adding more "
                                                             "selections to difficulty and ratings")


# Create text widget and specify size.
function_text = Label(function_frame, text="Let us move on with 6 function courses", bg="green")
function_text.config(font=("Courier", 16))
function_text.pack()

# Create label
course_difficulty_text = Label(function_frame, text="Select the difficulty levels of your course", bg="green")
course_difficulty_text.config(font=("Courier", 14))
course_difficulty_text.pack()
for selection in difficulty_option_function:
    difficulty_option_function[selection] = Variable()
    difficulty_selection = Checkbutton(function_frame, text=selection, variable=difficulty_option_function[selection])
    difficulty_selection.pack()

course_ratings_text = Label(function_frame, text="Select the ratings of your course", bg="green")
course_ratings_text.config(font=("Courier", 14))
course_ratings_text.pack()

for selection in rating_option_function:
    rating_option_function[selection] = Variable()
    rating_selection = Checkbutton(function_frame, text=selection, variable=rating_option_function[selection])
    rating_selection.pack()

function_button = Button(function_frame, text="Click here and I will populate a function course "
                                              "recommendation for you",
                         command=function_recommendation, bg="green")
function_button.pack(pady=20)
function_frame.pack()
my_notebook.add(function_frame, text="Function Course Planer")
###############################################
# build recommendation for  Concentrations
###############################################
# Electives for concentrations
df_concentration_courses = df_concentration_courses.merge(course_hour_ratings_summary, left_on="Course Code",
                                                          right_on="Course", how="left")
df_concentration_courses["difficulty"] = df_concentration_courses["difficulty"].fillna("No Rating Available")
df_concentration_courses["rating"] = df_concentration_courses["rating"].fillna("No Rating Available")
df_concentration_courses["Score"] = scoring(df_concentration_courses["rating"], df_concentration_courses["difficulty"])

concentration_frame = Frame(my_notebook, bg="yellow")
difficulty_option_con = {"super hard": 0, "hard": 0, "easy": 0, "super easy": 0}

rating_option_con = {"Bad class,avoid!": 0, "OK class": 0, "Great class!": 0}

concentration_option = {"Accounting": 0, "Analytic Finance": 0, "Behavioral Science": 0, "Business Analytics": 0,
                        "Econometrics and Statistics": 0, "Economics": 0, "Entrepreneurship": 0, "Finance": 0,
                        "General Management": 0, "International Business": 0, "Marketing Management": 0,
                        "Operations Management": 0, "Strategic Management": 0}


def concentration_recommendation():
    diff_variable = [diff for diff in difficulty_option_con if difficulty_option_con[diff].get() == "1"]
    rate_variable = [rate for rate in rating_option_con if rating_option_con[rate].get() == "1"]
    concentration_variable = [con for con in concentration_option if concentration_option[con].get() == "1"]
    try:
        concentration_course = electives_course_selection(df_concentration_courses, df_concentration_requirement,
                                                          concentration=concentration_variable,
                                                          difficulty=diff_variable,
                                                          ratings=rate_variable)
        tree = ttk.Treeview(concentration_frame)
        cols = list(concentration_course.columns)
        tree["columns"] = list(concentration_course.columns)
        for i in cols:
            tree.column(i, anchor="w")
            tree.heading(i, text=i, anchor='w')

        for index, row in concentration_course.iterrows():
            tree.insert("", 0, text=index, values=list(row))
        tree.pack(fill='both')
    except:
        messagebox.showerror("Things don't always work out", "Can't find courses for you :(, try different selections")


# Create text widget and specify size.
function_text = Label(concentration_frame, text="Lastly, lets work on concentration courses!", bg="yellow")
function_text.config(font=("Courier", 16))
function_text.pack()

# Create label
course_difficulty_text = Label(concentration_frame, text="Select the difficulty levels of your course", bg="yellow")
course_difficulty_text.config(font=("Courier", 14))
course_difficulty_text.pack()
for selection in difficulty_option_con:
    difficulty_option_con[selection] = Variable()
    difficulty_selection = Checkbutton(concentration_frame, text=selection, variable=difficulty_option_con[selection])
    difficulty_selection.pack()

course_ratings_text = Label(concentration_frame, text="Select the ratings of your course", bg="yellow")
course_ratings_text.config(font=("Courier", 14))
course_ratings_text.pack()

for selection in rating_option_con:
    rating_option_con[selection] = Variable()
    rating_selection = Checkbutton(concentration_frame, text=selection, variable=rating_option_con[selection])
    rating_selection.pack()

concentration_text = Label(concentration_frame, text="Select the concentrations you like", bg="yellow")
concentration_text.config(font=("Courier", 14))
concentration_text.pack()

for selection in concentration_option:
    concentration_option[selection] = Variable()
    concentration_selection = Checkbutton(concentration_frame, text=selection, variable=concentration_option[selection])
    concentration_selection.pack()

concentration_button = Button(concentration_frame, text="Click here and I will populate a concentration course "
                                                        "recommendation for you", command=concentration_recommendation,
                              bg="yellow")
concentration_button.pack(pady=20)
concentration_frame.pack()
my_notebook.add(concentration_frame, text="Concentration Course Planer")
#################################
# Start Analysis Bid Points
#################################
graph_frame = Frame(my_notebook, width=500, height=800, bg="orange")
function_text = Label(graph_frame, text="Enter a Course Code below", bg="orange")
function_text.config(font=("Courier", 16))
function_text.pack()

course_history_file = pd.DataFrame()
xls = pd.ExcelFile('course price history.xls')
names = xls.sheet_names

# create a master course history file by appending all sheets together, also adding a sheet name column as source
df_course_history = pd.DataFrame()
for i in names:
    df = pd.read_excel(xls, sheet_name=i, skiprows=1)
    df["Source"] = i
    df_course_history = df_course_history.append(df)

# clean up data and create new columns for our analysis
df_course_history[["Quarter", "Year"]] = df_course_history["Source"].str.split(expand=True)
# add numbers in front of quarter name for easier sorting
df_course_history["Quarter"] = df_course_history["Quarter"].replace("Summer", "3-Summer")
df_course_history["Quarter"] = df_course_history["Quarter"].replace("Spring", "2-Spring")
df_course_history["Quarter"] = df_course_history["Quarter"].replace("Winter", "1-Winter")
df_course_history["Quarter"] = df_course_history["Quarter"].replace("Autumn", "4-Autumn")
df_course_history = df_course_history.sort_values(by=['Year', "Quarter"])
df_course_history["Source"] = df_course_history["Year"] + "_" + df_course_history["Quarter"]
df_course_history[["Course Code", "Section Code"]] = df_course_history["Course"].str.split("-", expand=True)
course_list = df_course_history["Course Code"].unique()
df_course_history['Phase 1 Price'] = df_course_history['Phase 1 Price'].fillna(0)
col_need = ["Course Code", 'Phase 1 Price', 'Instructor', "Source", "Year", "Quarter", "Section Code"]
df_course_clean = df_course_history.loc[:, col_need]

# Add button for user to enter course code
course_code_box = Entry(graph_frame)
course_code_box.pack(pady=20)


def submit():
    course_exist = set(df_course_clean["Course Code"])
    if course_code_box.get() not in course_exist:
        messagebox.showerror("Wrong Course Code", "This Course Code does not exist! Please look up and "
                                                  "enter the correct one")
    else:
        plot_by_time(df_course_clean, "Phase 1 Price", "Source", "Section Code", course_code_box.get())


my_button = Button(graph_frame, text="Click here and Visualize the Trend!", command=submit)
my_button.pack(pady=20)
graph_frame.pack()
my_notebook.add(graph_frame, text="Bidding Point Analysis")

root.mainloop()
