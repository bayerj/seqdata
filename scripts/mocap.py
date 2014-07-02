"""Create a data set of motion capture data.

Usage:
    mocap.py rtrbm --n-train=<nt> --n-val=<nv> --n-test=<ne> --target=<file>

Options:
    --target=<file>         Data set will be saved into that file.
    --n-train=<nt>          Number of time steps to put into the 'train' group.
    --n-val=<nv>            Number of time steps to put into the 'val' group.
    --n-test=<ne>           Number of time steps to put into the 'test' group.
"""


import sys

import docopt
import h5py
from scipy.io import loadmat


def add_group(fp, handle, seqs):
    grp = fp.create_group(handle)
    for i, seq in enumerate(seqs):
        grp.create_dataset(str(i), data=seq)


def load_data():
    try:
        f = loadmat('MOCAP.mat')
    except IOError:
        print ("Could not open `MOCAP.mat.` Download it as part of the "
               "recurrent temporal rbm code from "
               "`https://www.cs.toronto.edu/~ilya/pubs/`, where you can find "
               "it in the `data/` folder.")
    return f['batchdata'][-int(f['seqlengths'][0, -1].flatten()[0]):]


def main(args):
    AX = load_data()
    split_train_val = int(args['--n-train'])
    split_val_test = split_train_val + int(args['--n-val'])
    stop = split_val_test + int(args['--n-test'])

    if stop > AX.shape[0]:
        raise ValueError("Not enough time steps for desired train/val/test "
                         "split. Maximum: %i." % AX.shape[0])

    X = AX[:split_train_val]
    VX = AX[split_train_val:split_val_test]
    TX = AX[split_val_test:stop]

    with h5py.File(args['--target'], 'w') as fp:
        add_group(fp, 'train', [X])
        add_group(fp, 'val', [VX])
        add_group(fp, 'test', [TX])


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    main(args)
