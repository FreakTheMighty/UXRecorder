#!/usr/bin/env python
# ----------------------------------------------------------------------------
# Copyright 2015 Nervana Systems Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------------

"""
AllCNN style convnet on CIFAR10 data.

Reference:
    Striving for Simplicity: the All Convolutional Net `[Springenberg2015]`_
..  _[Springenber2015]: http://arxiv.org/pdf/1412.6806.pdf
"""

from neon.initializers import GlorotUniform
from neon.optimizers import GradientDescentMomentum, Schedule
from neon.layers import Conv, Dropout, Activation, Pooling, GeneralizedCost, SumSquared
from neon.transforms import Rectlin, Softmax, CrossEntropyMulti, Misclassification
from neon.models import Model
from neon.data import DataIterator, load_cifar10
from neon.callbacks.callbacks import Callbacks
from neon.util.argparser import NeonArgparser
import glob

# parse the command line arguments
parser = NeonArgparser(__doc__)
args = parser.parse_args()

class ImageReader(NervanaObject):

    def __init__(self, input_glob, target_glob):
        self.batch_index = 0
        self.input_paths = glob.glob(input_glob)
        self.target_paths = glob.glob(target_glob)
        self.ndata = len(inputPaths)
        assert len(self.input_paths) == len(self.target_paths)
        assert self.ndata > self.be.bsz
        self.nbatches = self.ndata / (self.be.bsz)


    def reset(self):
        self.batch_index = 0

    def __iter__(self):
        self.batch_index = 0
        while self.batch_index < self.nbatches:
            start_index = self.be.bsz*self.batch_index;
            input_batch = self.input_paths[start_index:start_index+self.be.bsz]
            target_batch = self.target_paths[start_index:start_index+self.be.bsz]

            # Read paths

            self.batch_index += 1

            yield input_images, output_images



        

# hyperparameters
num_epochs = args.epochs

(X_train, y_train), (X_test, y_test), nclass = load_cifar10(path=args.data_dir)

# really 10 classes, pad to nearest power of 2 to match conv output
train_set = DataIterator(X_train, y_train, nclass=16, lshape=(3, 512, 512))
valid_set = DataIterator(X_test, y_test, nclass=16, lshape=(3, 512, 512))

init_uni = GlorotUniform()
opt_gdm = GradientDescentMomentum(learning_rate=0.5, momentum_coef=0.9, wdecay=.0001,
                                  schedule=Schedule(step_config=[200, 250, 300], change=0.1))

relu = Rectlin()
conv = dict(init=init_uni, batch_norm=True, activation=relu)
convp1 = dict(init=init_uni, batch_norm=True, activation=relu, padding=1)
convp1s2 = dict(init=init_uni, batch_norm=True, activation=relu, padding=1, strides=2)

layers = [Dropout(keep=.8),
          Conv((3, 3, 96), **conv),
          Conv((3, 3, 96), **convp1),
          Conv((3, 3, 96), **convp1s2),
          Dropout(keep=.5),
          Conv((3, 3, 192), **convp1),
          Conv((3, 3, 192), **convp1),
          Conv((3, 3, 192), **convp1s2),
          Dropout(keep=.5),
          Conv((3, 3, 192), **conv),
          Conv((1, 1, 192), **conv),
          Conv((1, 1, 16), init=init_uni, activation=relu),
          Pooling(6, op="avg"),
          Activation(Rectlin())]

cost = GeneralizedCost(costfunc=SumSquared())

mlp = Model(layers=layers)

# configure callbacks
callbacks = Callbacks(mlp, train_set, eval_set=valid_set, **args.callback_args)

mlp.fit(train_set, optimizer=opt_gdm, num_epochs=num_epochs, cost=cost, callbacks=callbacks)
print('Misclassification error = %.1f%%' % (mlp.eval(valid_set, metric=Misclassification())*100))
