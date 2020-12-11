class MDUser(object):
    def __init__(self):
        self.md_name = ""
        self.md_username = ""
        self.md_password = ""
        self.best_score = ""
        self.history_score_list = ""

    def __init__(self, md_name, md_username, md_password, best_score, history_score):
        self.md_name = md_name
        self.md_username = md_username
        self.md_password = md_password
        self.best_score = best_score
        self.history_score_list = history_score

