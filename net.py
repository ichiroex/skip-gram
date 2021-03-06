# -*- coding: utf-8 -*-
"""
Network Architecture of Neural Language Model
"""
from __future__ import print_function
import chainer
from chainer import cuda, Variable, Chain
import chainer.functions as F
import chainer.links as L
import numpy as np

class SkipGram(Chain):

    def __init__(self,
                 vocab_size,
                 embed_size):

        super(SkipGram, self).__init__(
            embed = L.EmbedID(vocab_size, embed_size),
            l1 = L.Linear(embed_size, vocab_size))

        self.vocab_size = vocab_size
        self.embed_size = embed_size

    def __call__(self, x, context):

        loss = None
        for c in context:
            e = self.embed(c)
            y = self.l1(e)
            loss_i = F.softmax_cross_entropy(y, x)
            loss = loss_i if loss is None else loss + loss_i
            
        return loss

    def get_embedding(self, x):
        return self.embed(x)

    def save_spec(self, filename):
        with open(filename, 'w') as fp:
            # パラメータを保存
            print(self.vocab_size, file=fp)
            print(self.embed_size, file=fp)

    @staticmethod
    def load_spec(filename):
        with open(filename) as fp:
            # specファイルからモデルのパラメータをロード
            vocab_size = int(next(fp))
            embed_size = int(next(fp))
            return SkipGram(vocab_size, embed_size)
