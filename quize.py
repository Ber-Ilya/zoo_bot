class Quize:
    def __init__(self, **kwargs):
        self.questions = kwargs

    def get_questions(self):
        questions = [q['text']for q in self.questions['questions']]
        return questions


    def get_answers(self):
        answers = [q['options'] for q in self.questions['questions']]
        return answers


    def get_results(self):
        results_category = [r for r in self.questions['results'].values()]
        return results_category

