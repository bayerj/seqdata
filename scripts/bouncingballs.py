"""Create a data set of bouncing balls.

Usage:
    bouncingballs.py --time-steps=<t> --n-balls=<b> --res=<r> --target=<file> --n-train=<nt> --n-val=<nv> --n-test=<ne>

Options:
    --time-steps=<t>        Number of time steps each video has.
    --n-balls=<b>           Number of balls to have in the video.
    --res=<r>               Videos will have a <r> x <r> resolution.
    --target=<file>         Data set will be saved into that file.
    --n-train=<nt>          Number of sequences to put into the 'train' group.
    --n-val=<nv>            Number of sequences to put into the 'val' group.
    --n-test=<ne>           Number of sequences to put into the 'test' group.
"""


import sys

import docopt
import h5py


try:
    import bouncing_balls as bb
except ImportError:
    print ("Ilya Sutskever's bouncing balls module was not found on the "
           "PYTHONPATH. Download it as part of the recurrent temporal rbm code "
           "from `https://www.cs.toronto.edu/~ilya/pubs/`, where you can find "
           "it in the `data/` folder.")


def create_seqs(n_seqs, time_steps, n_balls, resolution):
    seqs = []
    for i in range(n_seqs):
        x = bb.bounce_n(time_steps, n_balls)
        xx = bb.matricize(x, resolution)
        seqs.append(xx)
    return seqs


def add_group(fp, handle, seqs):
    grp = fp.create_group(handle)
    for i, seq in enumerate(seqs):
        grp.create_dataset(str(i), data=seq)


def main(args):
    print args
    train_seqs = create_seqs(
        int(args['--n-train']), int(args['--time-steps']),
        int(args['--n-balls']), int(args['--res']))
    val_seqs = create_seqs(
        int(args['--n-val']), int(args['--time-steps']),
        int(args['--n-balls']), int(args['--res']))
    test_seqs = create_seqs(
        int(args['--n-test']), int(args['--time-steps']),
        int(args['--n-balls']), int(args['--res']))
    with h5py.File(args['--target'], 'w') as fp:
        add_group(fp, 'train', train_seqs)
        add_group(fp, 'val', val_seqs)
        add_group(fp, 'test', test_seqs)


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    main(args)
