def difficulty(score, easy_cut, medium_cut, hard_cut):
    output = []
    for i in score:
        if i <= easy_cut:
            output.append("super easy")
        elif i <= medium_cut:
            output.append("easy")
        elif i <= hard_cut:
            output.append("hard")
        else:
            output.append("super hard")

    return output


def rating(score, bad_cut, good_cut):
    output = []
    for i in score:
        if i <= bad_cut:
            output.append("Bad class,avoid!")
        elif i <= good_cut:
            output.append("OK class")
        else:
            output.append("Great class!")

    return output


def scoring(rating, difficulty):
    difficulty_score = {"No Rating Available": 0, "super hard": 1, "hard": 2, "easy": 3, "super easy": 4}
    rating_score = {"No Rating Available": 0, "Bad class,avoid!": 1, "OK class": 2, "Great class!": 3}
    ratings_values = [rating_score[i] for i in rating]
    difficulty_values = [difficulty_score[i] for i in difficulty]
    output = [int(ratings_values[i]) + int(difficulty_values[i]) for i in range(len(ratings_values))]
    return output
