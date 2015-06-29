import os
import use_dict 
import csv

def read_RNN(inpu,output):
    org_tmp = []
    write_tmp = []
    score_index = []
    output_tmp = []
    index_end = []
    output_tmp = []
    print "Preprocessing input datas..."
    with open (inpu, 'r') as result:
        lines = result.readlines()
        header_value = 1
        for index, line in enumerate(lines):
            if line.isspace():
                index_end.append(index - header_value)
                header_value += 1
                continue
            write_tmp.append(str(header_value)+" "+line.upper())
            org_tmp.append(line)
        result.close()
    with open ("rnn_input", 'w') as rnnfile:
        for content in write_tmp:
            rnnfile.write(content)
        rnnfile.close()
    cmd = "./simple-examples/simple-examples/rnnlm-0.2b/rnnlm -rnnlm simple-examples/simple-examples/rnnlm-0.2b/model100000 -test rnn_input -nbest -debug 0 > rnn_scores"
    print cmd
    os.system(cmd)
    print "Calculating scores ..."
    with open ("rnn_scores", 'r') as rnnfile:
        lines = rnnfile.readlines()
        tmp_index = 0
        tmp_value = -2000
        for index, line in enumerate(lines):
            if index - 1 in index_end:
                tmp_index = index
                tmp_value = float(line)
            elif float(line) > tmp_value:
                tmp_value = float(line)
                tmp_index = index
            if index in index_end:
                score_index.append(tmp_index)
        rnnfile.close()
    for index in score_index:
        output_tmp.append(org_tmp[index].lower())
    print "Selecting best sentace..."
    with open ("rnn_result", 'w') as rnn_result_file:
        for content in output_tmp:
            rnn_result_file.write(content)
        rnn_result_file.close()
    my_dict = use_dict.make_dict()
    speech_id = open ('final_speechID.txt', 'r').readlines()
    with open (output, 'w') as outputfile:
        writer = csv.writer(outputfile)
        writer.writerow(['id','sequence'])
        for i in range(len(output_tmp)):
            writer.writerow([speech_id[i].strip('\n'), use_dict.use_dict(my_dict, output_tmp[i])])
        #outputfile.close()

def main():
    read_RNN("../gb","kaggle.csv")

if __name__ == "__main__":
    main()
