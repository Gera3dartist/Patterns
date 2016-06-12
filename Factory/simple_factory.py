__author__ = 'agerasym'

class AbstractProduct(object): pass


class Product1(AbstractProduct): pass


class Product2(AbstractProduct): pass


class ProductFactory(object):
    @staticmethod
    def create_product(product_type):
        if product_type == 'product1':
            return Product1()
        elif product_type == 'product2':
            return Product2()
        else:
            raise RuntimeError('Invalid Product')

