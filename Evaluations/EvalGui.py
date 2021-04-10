import sys
import statistics

if sys.version_info > (3, 0):
    import tkinter as tk
    from tkinter import filedialog
else:
    import Tkinter as tk
    import tkFileDialog as filedialog

import csv


class Feedback():

    def __init__(self):
        self.responses = []
        self.isNumeric = False

    def getQuestionId(self):
        return self.question_id

    def setQuestionId(self, question_id):
        self.question_id = question_id

    def getQuestion(self):
        return self.question

    def setQuestion(self, question):
        self.question = question

    def getResponses(self):
        return self.responses

    def addResponse(self, response):
        if isinstance(response, int):
            self.responses.append(response)
            self.isNumeric = True
        if isinstance(response, str) and len(response) > 0:
            self.responses.append(response)

    def responses_as_str(self):
        output = ''
        for r in self.responses:
            output += ' - {}\n'.format(r)
        return output

    def isNumericFeedback(self):
        return self.isNumeric


def getOrCreate(d, key):
    if (d.get(key) is None):
        d[key] = Feedback()
    return d[key]


def process_file(filename, show_adv_details=False):
    try:
        with open(filename, mode='r') as evalfile:
            reader = csv.reader(evalfile)
            evalfile.seek(0)
            mapval = {'strongly agree': 5, 'agree': 4, 'neutral': 3, 'disagree': 2, 'strongly disagree': 1,
                      'extremely satisfied': 5, 'satisfied': 4, 'dissatisfied': 2, 'extremely dissatisfied': 1,
                      'very likely': 5, 'likely': 4, 'unlikely': 2, 'very unlikely': 1}
            ignore_vals = ["No thanks", "Yes, I'd like Amazon Web Services (AWS) to follow up with me", "Promoter",
                           "Passive", "Detractor"]
            adv_title = 'Avg\tMin\tMax\tStd Dev\tQuestion\n'
            adv_output = '{average:.2f}\t{min:.2f}\t{max:.2f}\t{std_dev:.2f}\t{question}\n'
            std_title = 'Avg\tQuestion\n'
            std_output = '{average:.2f}\t{question}\n'
            feedback_output = '\n\n{title}\n-------------------\n{feedback}'
            feedback = {}
            total_rows = 0
            for row_position, row in enumerate(reader):
                for i, item in enumerate(row):
                    feedbackObj = getOrCreate(feedback, str(i))
                    if row_position == 0:
                        feedbackObj.setQuestionId(item)
                    elif row_position == 1:
                        feedbackObj.setQuestion(item.replace("\n", " "))
                    elif row_position > 1:
                        numeric_value = mapval.get(item.lower())
                        if numeric_value is None:
                            feedbackObj.addResponse(item)
                        else:
                            feedbackObj.addResponse(numeric_value)
                total_rows = row_position
            output = 'Number of responses: ' + str(total_rows-1) + '\n\n' + (std_title if not show_adv_details else adv_title)
            textarea_output = ''
            instructor_csat = {"count": 0, "sum": 0}
            overall_csat = {"count": 0, "sum": 0}
            for f in feedback.values():
                if len(f.getResponses()) == 0:
                    continue
                elif f.isNumericFeedback():
                    responses = f.getResponses()
                    output += (std_output if not show_adv_details else adv_output).format(
                                                    average=statistics.mean(responses),
                                                    std_dev=statistics.stdev(responses),
                                                    min=min(responses),
                                                    max=max(responses),
                                                    question=f.getQuestion())
                    if f.getQuestion().find("instructor") > 0:
                        instructor_csat["count"] += 1
                        instructor_csat["sum"] += statistics.mean(responses)
                    overall_csat["count"] += 1
                    overall_csat["sum"] += statistics.mean(responses)
                elif f.getQuestionId().find("TEXT") > 0:
                    textarea_output += feedback_output.format(title=f.getQuestion(), feedback=f.responses_as_str())
            output += '\n'
            output += '%.2f' % (float(instructor_csat.get("sum")) / float(instructor_csat.get("count"))) + '\t' + 'Instructor CSAT' + '\n'
            output += '%.2f' % (float(overall_csat.get("sum")) / float(overall_csat.get("count"))) + '\t' + 'Overall CSAT' + '\n'
            output += textarea_output
            results.delete("1.0", tk.END)
            results.insert(tk.END, output)
    except:
        results.insert(tk.END, "There is a problem with that file.")


def get_file_name(show_adv_details=False):
    browse_file = filedialog.askopenfilename(
        title="Select file",
        filetypes=(
            ("csv file", "*.csv"),
            ("text file", "*.txt"),
            ("all files", "*.*")))
    process_file(browse_file, show_adv_details)


def copy_text():
    r.clipboard_clear()
    r.clipboard_append(results.get("1.0", tk.END))


# set-up window
global r, output
r = tk.Tk()
showAdvDetails = tk.BooleanVar()
r.title('AWS T&C CSAT Evaluation v1.1')
r.geometry("1200x850")

fileOpenPath = tk.Button(r,
                         text='Choose a raw evaluation file',
                         command=lambda: get_file_name(showAdvDetails.get()))
fileOpenPath.grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)

advdetails = tk.Checkbutton(r, text="Show Adv Details", variable=showAdvDetails).grid(row=1, sticky=tk.W)

results = tk.Text(r, width=140, height=45)
results.grid(column=0, row=2, padx=5, pady=5, sticky=tk.W)
results.config(wrap=tk.WORD)

copy = tk.Button(r, text='Copy all to clipboard', command=lambda: copy_text())
copy.grid(column=0, row=3, padx=5, pady=5, sticky=tk.W)

r.mainloop()
