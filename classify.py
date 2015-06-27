import numpy as np
import caffe
import sys
import prepare_data

MODEL_FILE = 'acoustic_predict_hdf5.prototxt'
PRETRAINED = '_iter_10000.caffemodel'
FEAT_NUM = 69 + 39
INPUT_FILE = 'MLDS_HW1_RELEASE_v1/mfccfbank/train.normalized.cv.test.ark'
BATCH = 256
LABEL_FILE = 'MLDS_HW1_RELEASE_v1/label/train.lab'
MAP_FILE = 'MLDS_HW1_RELEASE_v1/phones/48_idx_chr.map'


def main(argv):

    if len(argv) < 3:
        print 'classify.py predict.prototxt _iter_10000.caffemodel'
        exit(-1)
    model_file = argv[1]
    pretrained = argv[2]

    spchid_phone_map, d_index_phone, d_phone_index, d_phone_alphabet  = prepare_data.read_map(LABEL_FILE, MAP_FILE)


    #input : iterable : (H x W x K)
    (spids, xs)  = read_data(INPUT_FILE, count=8192)
    ys = [int(spchid_phone_map[spid]) if spid in spchid_phone_map else -1 \
            for spid in spids]
    preds = classify(model_file, pretrained, xs, ys)

    preds_cnt = len(preds)
    correct_cnt = \
            sum([1 if prob.argmax() == y else 0 \
                    for (prob, y) in zip(preds, ys)])

    print 'predicted:', preds_cnt
    print 'correct:', correct_cnt
    print 'acc:', float(correct_cnt) / preds_cnt


def classify(model_file, pretrained, xs, ys):
    caffe.set_mode_gpu()
    net = caffe.Classifier(model_file, pretrained,raw_scale=1, image_dims=(1, FEAT_NUM))

    preds = []

    for i in xrange((len(xs) + BATCH - 1) / BATCH):
        xs_part = xs[i*BATCH: i*BATCH + BATCH]
        pred = net.predict(xs_part, oversample=False)

        # for (prob, y) in zip(pred, ys_part):
        #     print y, prob

        #print 'prediction shape:', pred[0].shape
        #print 'pred class:', pred[0].argmax()
        print 'y:', ys[i*BATCH: i*BATCH + BATCH]
        print 'pred:', pred
        preds.extend(pred)

    return preds


def read_data(in_file, count=-1):
    lines = []
    with open(in_file, 'r') as f:
        if count < 0:
            lines = f.readlines()
        else:
            for i in xrange(count):
                lines.append(f.readline())
    xs = []
    spids = []
    for l in lines:
        l = l.strip().split()
        x = [float(ft) for ft in l[1:]]
        spids.append(l[0])
        xs.append(np.array(x).reshape((1,FEAT_NUM,1)))

    return spids, xs



if __name__=='__main__':
    main(sys.argv)
