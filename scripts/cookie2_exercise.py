"""This file contains code for use with "Think Bayes",
by Allen B. Downey, available from greenteapress.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

from __future__ import print_function, division
from collections.abc import MutableMapping

from thinkbayes2 import Pmf


class Bowl(MutableMapping):
    def __init__(self, vanilla: int, chocolate: int) -> None:
        self.store = dict(
            vanilla=vanilla,
            chocolate=chocolate
        )

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        self.store[key] = value

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __repr__(self):
        return repr(self.store)

    def probabilities(self):
        pmf = Pmf(self.store)
        pmf.Normalize()
        return pmf

    def eat(self, cookie: str) -> None:
        if self.store[cookie] > 0:
            self.store[cookie] = self.store[cookie] - 1
        else:
            raise ValueError(f"No {cookie} cookies left.")


class Cookie(Pmf):
    """A map from string bowl ID to probablity."""

    def __init__(self, hypos):
        """Initialize self.

        hypos: sequence of string bowl IDs
        """
        self.cookies = hypos
        Pmf.__init__(self)
        for hypo in hypos.keys():
            self.Set(hypo, 1)
        self.Normalize()

    def Update(self, data):
        """Updates the PMF with new data.

        data: string cookie type
        """
        for hypo in self.Values():
            like = self.Likelihood(data, hypo)
            self.Mult(hypo, like)
            self.cookies[hypo].eat(data)
        self.Normalize()

    def Likelihood(self, data, hypo):
        """The likelihood of the data under the hypothesis.

        data: string cookie type
        hypo: string bowl ID
        """
        mixes = {bname: bcookies.probabilities()
                 for bname, bcookies
                 in self.cookies.items()}
        mix = mixes[hypo]
        like = mix[data]
        return like


def main():
    bowl_1 = Bowl(30, 10)
    bowl_2 = Bowl(20, 20)

    hypos = dict(bowl_1=bowl_1, bowl_2=bowl_2)

    pmf = Cookie(hypos)

    pmf.Update('vanilla')
    pmf.Update('vanilla')

    for hypo, prob in pmf.Items():
        print(hypo, prob)


if __name__ == '__main__':
    main()
