'''
This code was inspired by the code at:
https://github.com/edent/Tate-Hack/blob/master/eigensave.py
'''


import argparse
import os
import sys
import cv2
import numpy as np
import json


def read_images(path, sz=None):
    img_meta = {}
    X,y = [], []
    count = 0
    for dirname, dirnames, filenames in os.walk(path):
        for subdirname in dirnames:
            subject_path = os.path.join(dirname, subdirname)
            for filename in os.listdir(subject_path):
                try:
                    print(subject_path,filename)
                    im = cv2.imread(os.path.join(subject_path, filename), cv2.IMREAD_GRAYSCALE)
                    # resize to given size (if given)
                    if (sz is not None):
                        im = cv2.resize(im, sz)
                    X.append(np.asarray(im, dtype=np.uint8))
                    y.append(count)
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    continue
                img_meta[str(count)] = {'subject':subdirname} 
            count = count+1
    return (img_meta, [X,y])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train faces')
    parser.add_argument('img_dir',
                        help='Directory with subject training images')
    parser.add_argument('--model_out', default='eigenModel.xml')
    parser.add_argument('--meta_out', default='imgmeta.json')

    args = parser.parse_args()
    (img_meta, [X,y]) = read_images(args.img_dir, (256,256))
    
    
    # Convert labels to 32bit integers. This is a workaround for 64bit machines,
    y = np.asarray(y, dtype=np.int32)

    # Create the Eigenfaces model.
    model = cv2.createEigenFaceRecognizer(num_components=40)
    # Learn the model. Remember our function returns Python lists,
    # so we use np.asarray to turn them into NumPy lists to make
    # the OpenCV wrapper happy:
    model.train(np.asarray(X), np.asarray(y))

    # Save the model for later use
    model.save(args.model_out)

    with open(args.meta_out, 'w') as outfile:
        json.dump(img_meta, outfile)
