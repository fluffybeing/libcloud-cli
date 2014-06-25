# -*- coding:utf-8 -*-
import libcloud

__all__ = [
    'versions',
]

versions = {
    libcloud.__version__: '0.14',  # FIXME: it's just for test
}
