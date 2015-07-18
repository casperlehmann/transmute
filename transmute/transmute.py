#! -*-coding:utf8-*-
from __future__ import print_function
import copy

INDEVISIBLE_FORMS = [str, unicode, int, float]

left_form = {
    'key': 'abc123',
    'name': {'first': 'joe', 'last': 'stein'},
    'triples': {1: 3, 2: 6, 3: 9, 4: 12, 5: 15},
    'opposites': [('low','high'),('big','small')]
    }
right_form = {
    'uuid': 'abc123',
    'first_name': 'joe',
    'last_name': 'stein',
    'triple_tuples': [(1, 3), (2, 6), (3, 9), (4, 12), (5, 15)],
    'opposites': [{'first': 'low', 'second': 'high'}, {'first': 'big', 'second': 'small'}]
    }

class TranslationModeller(object):
    """Takes two structures and formalizes a translation model.

    Input tree and output tree must share contents, so that the methods below
    can recognize the structures, and how to translate between them."""

    debug = False

    def __init__(self, input_tree, output_tree, debug = False):
        if debug: self.debug = True
        self.left = input_tree
        self.l_structure = []
        self.right = output_tree
        self.r_structure = []

    def get_key_val(self, container, overview = None, navi = None, level = None):
        if overview is None: overview = []
        if navi is None: navi = []
        if level is None: level = 0

        if self.debug: print ('container', container)
        if type(container) in INDEVISIBLE_FORMS:
            overview.append(navi[:] + [[str, container]])
            overview.append(navi[:] + [
                ['final', list, len(container), type(v), len(v), i, v]])
        if isinstance(container, dict):
            container, overview, navi, level = self.get_dict(
                    container, overview, navi, level)
        elif isinstance(container, list):
            container, overview, navi, level = self.get_list(
                    container, overview, navi, level)
        elif isinstance(container, tuple):
            container, overview, navi, level = self.get_tuple(
                    container, overview, navi, level)
        return overview, navi

    def get_dict(self, container, overview, navi, level):
        cvals = container.values()
        if not False in [type(x) in INDEVISIBLE_FORMS for x in cvals]:
            if self.debug: self.printout(container, overview, navi, level, 0, 0, 'dict_0')
            overview.append(navi[:] + [[dict, container]])
        else:
            for k,v in container.items():
                if type(v) in INDEVISIBLE_FORMS:
                    if self.debug: self.printout(container, overview, navi, level, k, v, 'dict_1')
                    overview.append(navi[:] +\
                        [['final', dict, len(container), type(v), len(v), k, v]])
                    #print ('|||', [['final', dict, len(container), type(v), len(v), k, v]])                    
                else:
                    if self.debug: self.printout(container, overview, navi, level, k, v, 'dict_2')
                    level += 1
                    navi.append([dict, container.keys(), type(v), len(v), k])
                    overview, navi = self.get_key_val(v, overview, navi, level)
                    navi = navi[:-1]
                    level -= 1
        return container, overview, navi, level

    def get_list(self, container, overview, navi, level):
        if not False in [type(x) in INDEVISIBLE_FORMS for x in container]:
            if self.debug: self.printout(container, overview, navi, level, 0, 0, 'list_0')
            overview.append(navi[:] + [[list, container]])
        else:
            for i,v in enumerate(container):
                if type(v) in INDEVISIBLE_FORMS:
                    if self.debug: self.printout(container, overview, navi, level, i, v, 'list_1')
                    overview.append(navi[:] +\
                        [['final', list, len(container), type(v), len(v), i, v]])
                else:
                    if self.debug: self.printout(container, overview, navi, level, i, v, 'list_2')
                    level += 1
                    navi.append([list, len(container), type(v), len(v), i])
                    overview, navi = self.get_key_val(v, overview, navi, level)
                    navi = navi[:-1]
                    level -= 1
        return container, overview, navi, level

    def get_tuple(self, container, overview, navi, level):
        if not False in [type(x) in INDEVISIBLE_FORMS for x in container]:
            if self.debug: self.printout(container, overview, navi, level, 0, 0, 'tuple_0')
            overview.append(navi[:] + [[tuple, container]])
        else:
            for i,v in enumerate(container):
                if type(v) in INDEVISIBLE_FORMS:
                    overview.append(navi[:] +\
                        [['final', list, len(container), type(v), len(v), i, v]]) #!! list -> tuple
                    if self.debug: self.printout(container, overview, navi, level, i, v, 'tuple_1')
                else:
                    if self.debug: self.printout(container, overview, navi, level, i, v, 'tuple_2')
                    level += 1
                    navi.append([list, len(container), type(v), len(v), i]) #!! list -> tuple
                    overview, navi = self.get_key_val(v, overview, navi, level)
                    navi = navi[:-1]
                    level -= 1
        return container, overview, navi, level

    @staticmethod
    def printout(container, overview, navi, level, key, val, msg):
        level += 1
        print()
        print('____________________________', msg)
        print (container)
        print (key, '\t\t', val)    
        #print ('navi ', navi)
        print ('lvl  ', level)
        print('navi:')
        for i,x in enumerate(navi):
            for y in x:
                print (level*'|' + (1+i)*4*' ', y)
        print('overview:')
        for i,x in enumerate(overview):
            for y in x:
                print (level*'#' + (1+i)*4*' ', y)
        print ()

class Transmute(object):
    """Translates data between two forms.

    Initialize with two structures to create translation models, allowing to
    translate data between the two parallel representations.
    """
    debug = False
    def __init__(self, left, right, debug = False):
        if debug: self.debug = True
        self.left_right = TranslationModeller(left_form, right_form, debug)
        self.l_overview, navi = self.left_right.get_key_val(left_form)
        self.right_left = TranslationModeller(right_form, left_form, debug)
        self.r_overview, navi = self.right_left.get_key_val(right_form)

    def translate(self):
        if isinstance(self.left, dict):
            pass

    def follow_roadmap(self, road, output):
        next_level = output
        for step in road[:-1]:
            if self.debug: print (road)
            #print ('== step:')
            #print (step)
            container_type, container_info, child_type, child_info, index = step
            if container_type is dict:
                next_level = self.open_dict_container(next_level, container_type,
                            container_info, child_type, child_info, index)
            elif container_type is list or container_type is tuple:
                next_level = self.open_list_container(next_level, container_type,
                            container_info, child_type, child_info, index, output)
                if container_type is tuple:
                    next_level = tuple(next_level)
        print ('{1--<', 'next_level', type(next_level))
        return next_level

    def finalize(self, items = None, next_level = None):
        if len(items) == 2:
            if items[0] is dict:
                print ('items', type(items))
                print (items)
                print ('next_level', type(next_level))
                print (next_level)
                print()
                for k,v in items[1].items():
                    next_level[k] = v
            elif items[0] is list:
                for x in items[1]:
                    next_level.append(x)
            elif items[0] is tuple:
                next_level.append(items[1])
            elif items[0] is str:
                next_level = items[1]
                #for i, x in enumerate(items): print (i, '+', x)
        else:
            if items[3] is dict:
                for k,v in items[-1].items():
                    next_level[k] = v
            elif items[3] is list:
                for x in items[-1]:
                    next_level.append(x)
            elif items[3] is tuple:
                next_level.append(items[-1])
            elif items[3] is str:
                next_level[items[-2]] = items[-1]

    def recreate(self, overview, output = None):
        #for x in overview: print (':', x)
        if output is None: output = {}
        print ('----------------------')
        for x in overview:
            print (x)
        print ('----------------------')
        print (output)
        print ('----------------------')
        for road in overview:
            next_level = self.follow_roadmap(road = road, output = output)
            self.finalize(items = road[-1], next_level = next_level)
        return output

    def test_it(self, l_tree, r_tree):
        #print(input_tree)
        l_recreated = self.recreate(self.l_overview)
        if l_recreated == l_tree: 
            print (True)
        else: 
            print (False, l_recreated)
        print(4 * '========')
        
        r_recreated = self.recreate(self.r_overview)
        if r_recreated == r_tree: 
            print (True)
        else: 
            print (False)
            print ('|', r_tree)
            print ('|', r_recreated)
        print(4 * '========')
        print(4 * '========')
        print()

    def open_dict_container(self, next_level, container_type, container_info, child_type, child_info, index):
        for i,x in enumerate([next_level, container_type, container_info, child_type, child_info, index]):
            print (i, x)
        if child_type is dict:
            print (1)
            child_key = index
            if not child_key in next_level.keys():
                next_level[child_key] = child_type()
            next_level = next_level[child_key]
        elif child_type is list:
            print (2)
            container_keys = container_info
            child_len = child_info
            child_index = index
            if len(next_level) == 0:
                for key in container_keys:
                    if not key in next_level:
                        next_level[key] = None #child_type() 
                        # This is wrong. We only know single child type here. Cannot extrapolate.
                        # Throw this up in the beginning of the method so that sub trees are created once and only once.
                        if key == child_type:
                            next_level[child_index] = child_type()
            if not child_index in next_level:
                next_level[child_index] = child_type()
            next_level = next_level[child_index]
        elif child_type is str or child_type is unicode:
            print (3)
            # This shouldn't happen.
            # We want to treat immutable items in finalize().
            print('___', child_type, index, next_level[index])
            #print(step)
            next_level[index] = ''
        else:
            print('___________fail 1')
        for i,x in enumerate([next_level, container_type, container_info, child_type, child_info, index]):
            print (i, x)
        print ('{2--<', 'next_level', type(next_level))
        return next_level

    def open_list_container(self, next_level, container_type, container_info, child_type, child_info, index, output = None):
        self.printout_list(next_level, container_type, container_info, child_type, child_info, index, output, 'Open List')
        if child_type is list:
            container_len = container_info
            child_index = index
            for x in range(container_len-len(next_level)):
                next_level.append(None)
            next_level[child_index] = child_type()
            next_level = next_level[child_index]
        elif child_type is str or child_type is unicode:
            print ('| Container: list, Child: str')
        elif child_type is tuple:
            container_len = container_info
        elif child_type is dict:
            print ()
            for x in range(container_info-len(next_level)):
                next_level.append(None)
            for x in [next_level, container_type, container_info, child_type, child_info, index, output]:
                print (x)
            print()
            print ( container_info )
            print()
            #1/0
        else:
            print('___________fail 2', child_type)
        return next_level

    def printout_list(self, next_level, container_type, container_info, child_type, child_info, index, output, msg):
        if not self.debug: return
        print()
        print('____________________________', msg)
        print('next_level:    ',     next_level)
        print('container_type:', container_type)
        print('container_info:', container_info)
        print('child_type:    ', child_type)
        print('child_info:    ', child_info)
        print('index:         ', index)
        print('output:        ', output)
        print ()


#modeller = TranslationModeller(left_form, right_form, False)
#for x in modeller.get_key_val(left_form, [], [], 0):
#    print (x)

print ('left\n', left_form)
print ('right\n', right_form)
print()

example = Transmute(left_form, right_form, False)
example.test_it(left_form, right_form)

#print (left_form)
