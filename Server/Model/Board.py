import random

class BoardCell:
    def __init__(self, row) -> None:
        self.State = dict(
            visit = False,
            value = (row+1)*200
        )


    def setState(self, keyValue):
        for key, value in keyValue.items():
            self.State[key] = value

            

class Board:
    def __init__(self, categories, scoresPerCategory, category_columns, questions) -> None:
        self.State = dict(
            categories = categories,
            scoresPerCategory = scoresPerCategory,
            category_columns = category_columns,
            cells = [[] for row in range(scoresPerCategory)],
            questions = [[] for row in range(scoresPerCategory)],
        )

        for col in range(categories):
            random_questions = random.sample(questions[col], scoresPerCategory)
            for row in range(scoresPerCategory):
                self.State['cells'][row].append(BoardCell(row))
                self.State['questions'][row].append(random_questions[row])


    def setState(self, keyValue):
        for key, value in keyValue.items():
            self.State[key] = value

    def setVisit(self, visit):
        for row in range(len(visit)):
            for col in range(len(visit[0])):
                self.State['cells'][row][col].setState(dict(
                    visit = visit[row][col],
                ))

    def getVisit(self):
        visit = []
        for row in range(self.State['scoresPerCategory']):
            visit.append([])
            for col in range(self.State['categories']):
                visit[-1].append(self.State['cells'][row][col].State['visit'])

        return visit

    
    def roundFinish(self, round):
        for row in range(self.State['scoresPerCategory']):
            for col in range(self.State['categories']):
                if self.State['cells'][row][col].State['visit'] == False:
                    return False

        return True

    
    def nextRound(self, round):
        if self.roundFinish():
            return round+1
        else:
            return round

