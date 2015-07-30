#############################################
# Universidad Tecnica Particular de Loja    #
#############################################
# Professor:                                #
# Rodrigo Barba        lrbarba@utpl.edu.ec  #
#############################################
# Students:                                 #
# Marcelo Bravo        mdbravo4@utpl.edu.ec #
# Galo Celly           gscelly@utpl.edu.ec  #
# Nicholas Earley      nearley@utpl.edu.ec  #
#############################################
#library to sanitize data converting all the doubles in tuple to integers
__author__ = 'utpl'

def double_tuple_2_int(t):
    l = []
    print t
    for d in t:
        l.append(int(d))
    return tuple(l)
