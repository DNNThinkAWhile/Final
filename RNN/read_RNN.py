import os

def read_RNN(output, n):
    org_tmp = []
    write_tmp = []
    score_index = []
    output_tmp = []
    print "Preprocessing input datas..."
    with open ("result/result", 'r') as result:
        lines = result.readlines()
        org_tmp = lines
        for index, line in enumerate(lines):
            header_value = (index+1)/n
            write_tmp.append(str(header_value)+" "+line.upper())
        result.close()
    with open ("result/rnn_input", 'w') as rnnfile:
        for content in write_tmp:
            rnnfile.write(content)
        rnnfile.close()
    cmd = "./simple-examples/simple-examples/rnnlm-0.2b/rnnlm -rnnlm simple-examples/simple-examples/rnnlm-0.2b/model100000 -test result/rnn_input -nbest -debug 0 > result/rnn_scores"
    print cmd
    os.system(cmd)
    print "Calculating scores ..."
    with open ("result/rnn_scores", 'r') as rnnfile:
        lines = rnnfile.readlines()
        tmp_index = 0
        tmp_value = -2000
        for index, line in enumerate(lines):
            if index % n == 0:
                tmp_index = index
                tmp_value = float(line)
            else:
                tmp_value = float(line) if float(line) < tmp_value else tmp_value
                tmp_index = index if float(line) < tmp_value else tmp_index
            if index % n == n - 1:
                score_index.append(tmp_index)
        rnnfile.close()
    for index in score_index:
        output_tmp.append(org_tmp[index])
    print "Selecting best sentace..."
    with open ("result/"+output, 'w') as outputfile:
        for content in output_tmp:
            outputfile.write(content)
        outputfile.close()

def main():
    read_RNN("file", 1)

if __name__ == "__main__":
    main()
