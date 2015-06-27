import os

def read_RNN(inpu,output, n):
    org_tmp = []
    write_tmp = []
    score_index = []
    output_tmp = []
    index_end = []
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
                print "index = ",tmp_index
                print "value = ",tmp_value
                score_index.append(tmp_index)
        rnnfile.close()
    for index in score_index:
        output_tmp.append(write_tmp[index][2:])
    print "Selecting best sentace..."
    with open (output, 'w') as outputfile:
        for content in output_tmp:
            outputfile.write(content)
        outputfile.close()

def main():
    n = 50
    read_RNN("gb","file", 50)

if __name__ == "__main__":
    main()
