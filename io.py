'''
(\/)
(oO)
c(")("
Author: Jack
'''


class IO():

    # returns the currently pressed button
    def current_input():
        pass

    # displays the array on screen
    def display(input_array, style_dic, clear_screen=True):
        for l in input_array:
            line = ''
            for e in l:
                line += style_dic[e]
            print(line, end =)
        
