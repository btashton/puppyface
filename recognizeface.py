import argparse
import json
import cv2


def recognize(model, image, threshold):
    emodel = cv2.createEigenFaceRecognizer(threshold=threshold)
    emodel.load(model)
    simg = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    simg = cv2.resize(simg, (256,256))

    [p_label, p_confidence] = emodel.predict(simg)
    return (p_label, p_confidence)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Match face.')
    parser.add_argument('-m', '--model', default='eigenModel.xml',
                        help='EignenFace model')
    parser.add_argument('-i', '--image', required=True,
                        help='Image to process')
    parser.add_argument('-t', '--threshold', type=float, required=True,
                        help='Matching threshold, 100.0 is very close')
    parser.add_argument('--meta', default='imgmeta.json',
                        help='File mapping subject to p_label')
    parser.add_argument('--result_out', default='result.json',
                        help='JSON file holding results')

    args = parser.parse_args()
    (p_label, p_confidence) = recognize(args.model, args.image, args.threshold)
    
    subject = None
    if args.meta is not None:
        with open(args.meta,'r') as metafile:
            img_meta = json.load(metafile)
            subject = img_meta[str(p_label)]['subject']
    result = dict(p_label=p_label, p_confidence=p_confidence, subject=subject)
    with open(args.result_out,'w') as resultfile:
        json.dump(result, resultfile)
    print(result)
