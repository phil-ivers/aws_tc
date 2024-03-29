import csv
import sys

with open(sys.argv[1], mode='r') as evalfile:
        reader = csv.reader(evalfile)
        ncols = len(next(reader)) + 1
        evalfile.seek(0)
        mapval = {'strongly agree': 5, 'agree': 4, 'neutral': 3, 'disagree': 2, 'strongly disagree': 1,
                  'extremely satisfied': 5, 'satisfied': 4, 'dissatisfied': 2, 'extremely dissatisfied': 1,
                  'very likely': 5, 'likely': 4, 'unlikely': 2, 'very unlikely': 1}
        ignore_vals = ["No thanks", "Yes, I'd like Amazon Web Services (AWS) to follow up with me", "Promoter", "Passive", "Detractor"]
        column_sum = [0] * ncols
        divisor = [0] * ncols
        question = [None] * ncols
        row_position = 0
        feedback_change = ''
        feedback_like = ''
        feedback_other = ''
        for row in reader:
            row_position = row_position + 1
            item_position = 0
            for item in row:
                item_position = item_position + 1
                consumed = 0
                if row_position == 2:
                    question[item_position] = item.replace("\n", " ")
                if mapval.get(item.lower()):
                    column_sum[item_position] = column_sum[item_position] + mapval.get(item.lower())
                    divisor[item_position] = divisor[item_position] + 1
                    consumed = 1
                if item and row_position > 2 and question[
                    item_position] == 'What would you recommend changing about this course?':
                    feedback_change = feedback_change + ' - ' + item + '\n'
                    consumed = 1
                if item and row_position > 2 and question[
                    item_position] == 'What did you like most about the course?':
                    feedback_like = feedback_like + ' - ' + item + '\n'
                    consumed = 1
                elif consumed == 0 and item and row_position > 2 and item not in ignore_vals:
                    feedback_other = feedback_other + ' - ' + item + '\n'

        item_position = 0

        instructor_sum = 0
        instructor_div = 0
        overall_sum = 0
        overall_div = 0

        for pos in range(ncols):
            val = divisor[pos]
            if val > 0:
                print('%.2f' % (float(column_sum[pos]) / float(val)), question[pos])
                overall_div = overall_div + val
                overall_sum = overall_sum + column_sum[pos]
                if 'instructor' in question[pos]:
                    instructor_div = instructor_div + val
                    instructor_sum = instructor_sum + column_sum[pos]

        print('')
        print('%.2f' % (float(instructor_sum) / float(instructor_div)), 'Instructor CSAT')
        print('%.2f' % (float(overall_sum) / float(overall_div)), 'Overall CSAT')
        print('')
        output = ''
        if feedback_change:
            output += 'Recommended Changes' + '\n'
            output += '-------------------' + '\n'
            output += feedback_change + '\n'
        if feedback_like:
            output += 'What was Liked' + '\n'
            output += '-------------------' + '\n'
            output += feedback_like + '\n'
        if feedback_other:
            output += 'Other feedback' + '\n'
            output += '-------------------' + '\n'
            output += feedback_other + '\n'
        print(output)
