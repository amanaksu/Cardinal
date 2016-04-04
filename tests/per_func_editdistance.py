#-----------------------------------------------------------------------------
# Three-Pronged Approach to Exploring the Limits of Static Malware Analyses:  
# Callsite Parameter Cardinality (CPC) Counting: get_cpc_accuracy.py                 
#                                                                               
# Compares the dictionary computed by cpc-tool to the ones generated by
# cpc_extract and tells their accuracy
#                                                                               
# Luke Jones (luke.t.jones.814@gmail.com)                                       
#                                                                               
#-----------------------------------------------------------------------------
from __future__ import print_function
import sys
import editdistance


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Needs 2 file arguments.")
        sys.exit()

    wrong = list()
    test1 = dict()
    test2 = dict()
    with open(sys.argv[1], 'r') as g:
        for line in g:
            tokens = line.split(" ")
            if len(tokens) > 1:
                test1[tokens[0]] = tokens[1]
    g.close()

    test1_count = 0
    test2_count = 0
    dist_count = 0
    shared = ""
    in_2 = ""
    in_1 = ""
    with open(sys.argv[2], 'r') as f:
        for line in f:
            tokens = line.split(" ")
            if len(tokens) > 1:
                test2entry = tokens[1]
                try:
                    test1entry = test1[tokens[0]]
                    del test1[tokens[0]]
                    test1_count += len(test1entry)
                    test2_count += len(test2entry)
                    dist = editdistance.eval(test1entry, test2entry)
                    dist_count += dist
                    shared = shared + tokens[0] + " " + str(dist) + "\n"

                except KeyError:
                    test2_count += len(test2entry)
                    dist_count += len(test2entry)
    f.close()

    for k in test1:
        test1_count += len(test1[k])
        dist_count += len(test1[k])

    print(shared)
    print("test1 cpc length: %d" % test1_count)
    print("test2 cpc length: %d" % test2_count)
    print("total distance: %d" % dist_count)
    denom = (float(test1_count) + float(test2_count)) / 2
    print("similarity: %f" % (1-(float(dist_count)/denom)))