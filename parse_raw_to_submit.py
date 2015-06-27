import sys
import prepare_data

LABEL_FILE = 'MLDS_HW1_RELEASE_v1/label/train.lab'
MAP_FILE = 'MLDS_HW1_RELEASE_v1/phones/48_idx_chr.map'
SPID_FILE = 'MLDS_HW1_RELEASE_v1/mfccfbank/test.normalized.ark'
map_48_39_file = 'MLDS_HW1_RELEASE_v1/phones/48_39.map'

def main(argv):
    if len(argv) < 3:
        print 'python parse_raw_to_submit.py raw_.txt submit.csv'
        exit(-1)

    spchid_phone_map, d_index_phone, d_phone_index, d_phone_alphabet  = prepare_data.read_map(LABEL_FILE, MAP_FILE)
    sol_48_39_map = create_48_39_map(map_48_39_file)
    
    INPUT_FILE = argv[1]
    OUTPUT_FILE = argv[2]
    
    with open(INPUT_FILE, 'r') as f:
        lines = f.readlines()
    phone = []
    spid = []
    for l in lines:
        if(l.startswith('[')):
            index = l.strip('[]\n').split(',')
            phone = phone + [sol_48_39_map[d_index_phone[ele.strip()]] for ele in index]
    for i in range(1,len(phone)-3):
        if (phone[i] != phone[i-1]) and (phone[i] != phone[i+1]) and (phone[i] == phone[i+2]) :
                phone[i+1] = phone[i]
        else: 
            if (phone[i] != phone[i-1]) and (phone[i] != phone[i+1]) and (phone[i-1] == phone[i-2]):
                phone[i] = phone[i-1]
                
    with open(SPID_FILE, 'r') as f:
        lines = f.readlines()
    for l in lines:
        spid.append((l.strip().split())[0])

    with open(OUTPUT_FILE, 'w') as f:
        print >> f, 'Id,Prediction'
        for i in range(len(spid)):
            str = spid[i]+','+phone[i]
            print >> f , str
    
def create_48_39_map(map_48_39_file):
	d = dict()
	with open(map_48_39_file, 'r') as f:
		for line in f:
			toks = line.strip().split('\t')
			d[toks[0]] = toks[1]
	return d
    
if __name__ == '__main__':
	main(sys.argv)
