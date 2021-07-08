import pandas as pd
import re
from re import search

pd.options.mode.chained_assignment = None


def core_course_selection(data, course_type, number_of_courses, difficulty=["easy"], ratings=["good"]):
    sub_data = data.loc[(data["Type"] == course_type) &
                        (data["rating"].isin(ratings)) &
                        (data["difficulty"].isin(difficulty))]
    unique_Area = set(data["Area"])
    # if multiple courses satisfy the same area, pick the best one
    output = pd.DataFrame()
    for i in unique_Area:
        course_selected = pd.DataFrame(sub_data[sub_data["Area"] == i].sort_values(by="Score", ascending=False)).head(1)
        output = output.append(course_selected)
    if len(output) < number_of_courses:
        raise ValueError("Can't find courses for you :(, try adding more selections to difficulty and ratings")
    output = output.sort_values(by="Score").head(number_of_courses)
    output["Units"] = 100
    columns_need = ["Course Code", "Course Name", "Type", "Area", 'Q. 1 HRS /WK', 'Q. 6 REC COURSE',
                    'difficulty', 'rating', 'Score', "Units"]
    output_cleaned = output[columns_need]
    output_cleaned["Course Code"] = output_cleaned["Course Code"].apply(str)
    return output_cleaned


def electives_course_selection(course_data, degree_requirement, concentration, difficulty=["easy"], ratings=["good"]):
    required_units = degree_requirement[degree_requirement["Concentration"].isin(concentration)]
    sub_data = pd.DataFrame(
        course_data.loc[course_data["Concentration"].isin(concentration) &
                        (course_data["rating"].isin(ratings)) &
                        (course_data["difficulty"].isin(difficulty))])
    sub_data = sub_data.sort_values(by="Score", ascending=False)
    concentration_course = pd.DataFrame()
    concentration_unit = 0
    for j in concentration:
        total_unit = 0
        concentration_threshold = int(required_units["Required Units"][required_units["Concentration"] == j])
        sub_data_concentration = pd.DataFrame(
            sub_data[sub_data["Concentration"] == j]).reset_index()
        for i in range(len(sub_data_concentration)):
            if total_unit < concentration_threshold:
                new_unit = int(sub_data_concentration["Units"][i])
                concentration_course = concentration_course.append(sub_data_concentration.iloc[i])
                total_unit += new_unit
            if len(concentration_course) > 11:
                raise ValueError("This schedule will not work :( try change concentration selection")
        concentration_unit += total_unit
    concentration_course["Type"] = "Concentration"
    concentration_course_list = set(concentration_course["Course"])
    sub_data_electives = pd.DataFrame(
        course_data[~course_data["Course"].isin(concentration_course_list)]). \
        sort_values(by="Score", ascending=False)
    # drop duplicates based on course code and only keep the first one
    sub_data_electives_clean = sub_data_electives.drop_duplicates(subset='Course Code', keep="first")
    cumulus_unit = sub_data_electives_clean["Units"].cumsum()
    electives_needed = 2100 - 900 - concentration_unit
    elective_courses = pd.DataFrame(sub_data_electives_clean[cumulus_unit < electives_needed])
    elective_courses["Type"] = "Electives"
    concentration_course = concentration_course.append(elective_courses)

    # print out only columns we need
    concentration_course = concentration_course.rename(columns={'Concentration': 'Area'})
    columns_need = ["Course Code", "Course Name", "Type", "Area", 'Q. 1 HRS /WK', 'Q. 6 REC COURSE',
                    'difficulty', 'rating', 'Score', "Units", 'Prerequisites', 'Prerequisites Courses']

    concentration_course_cleaned = concentration_course[columns_need]
    concentration_course_cleaned["Course Code"] = concentration_course_cleaned["Course Code"].apply(int).apply(str)
    return concentration_course_cleaned


def find_course_code(prereq_desc):
    prereq_desc_list = prereq_desc.split(",")
    output = []
    for i in prereq_desc_list:
        converted_words = re.findall("[0-9][0-9][0-9][0-9][0-9]", i)
        if len(converted_words)>1:
            output.append(converted_words)
        elif len(converted_words) == 1:
            output.append(converted_words[0])
    return output


def find_prerequisite(column):
    output = []
    equiv_dic = {"30000": ["30000", "30116", "30117", "30120", "30130", "30131"],
                 "33001": ["33001", "33002", "33101", "30100", "30200"],
                 "41000": ["41000", "41100", "41901", "41912", "41913"]}
    for i in column:
        i = str(i)
        if search("equiv", i):
            original_course = find_course_code(i)
            equiv_course = [equiv_dic[j] for j in original_course if j in equiv_dic.keys()]
            non_equic_couse = [j for j in original_course if j not in equiv_dic.keys()]
            if len(non_equic_couse) > 0:
                equiv_course.append(non_equic_couse)
            output.append(equiv_course)
        else:
            output.append(find_course_code(i))
    return output
