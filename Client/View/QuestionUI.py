from tkinter import Canvas, CENTER, Button, Toplevel
from tkinter import Tk, Text


class QuestionUI:
    def __init__(self, master, width: float, height: float, bg, question_window_state, question, answer) -> None:
        self.State = dict(
            question = question,
            question_window_state = question_window_state,
            answer = answer,
        )

        # Question Area
        questionArea_attr = dict(
            master = master,
            height = height*0.6,
            width = width,
            bg = '#563567'
        )

        self.questionArea = Canvas(**questionArea_attr)
        self.questionText = self.questionArea.create_text(questionArea_attr['width']/2, questionArea_attr['height']/2, font=('Helvetica 20 bold'), justify=CENTER)

        self.questionArea.pack()

        # Answer Area
        answerArea_attr = dict(
            master = master,
            height = height*0.4,
            width = width,
            bg = '#786853'
        )
        self.answerArea = Canvas(**answerArea_attr)
        
        # Text Box
        answerBox_attr = dict(
            master = self.answerArea,
            bg = '#129593',
            font=('Helvetica', 20, 'bold'),
            wrap = 'word',
        )
        self.answerBox = Text(**answerBox_attr)
        self.answerBox.place(height=int(answerArea_attr['height']), width=int(answerArea_attr['width']))

        self.answerArea.pack()
        self.updateState()

    def setState(self, keyValue):
        for key, value in keyValue.items():
            self.State[key] = value
        
        self.updateState()

    def updateState(self):
        self.questionArea.itemconfig(self.questionText, text = self.State['question'])
        self.answerBox.config(state=self.State['question_window_state'])
        self.answerBox.delete("1.0", "end")
        self.answerBox.insert('end', self.State['answer'])


    def submit(self):
        self.setState(dict(
            submit_button_state = 'disabled',
        ))

        self.State['questionAnswer']['answer'] = self.answerBox.get(1.0, 'end-1c')