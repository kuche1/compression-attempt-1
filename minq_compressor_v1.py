#! /usr/bin/env python3

import argparse
import sys

TOKEN_LEN = 2
DEPTH_PREF = ' '

class Binary_tree:
    def __init__(s):
        s.left = None
        s.right = None
        s.item = None
    
    def __repr__(s, pref=''):
        ret = ''

        if s.item != None:
            ret += f'{pref} item: {s.item}\n'

        if s.left != None:
            ret += s.left.__repr__(pref=pref+'0')
        
        if s.right != None:
            ret += s.right.__repr__(pref=pref+'1')

        assert ret != ''

        return ret
    
    def generate_translator(s, code=''):
        trans = {}

        if s.item != None:
            trans[s.item.data] = code

        else:
            trans = s.left.generate_translator(code+'0')

            if s.right != None:
                trans.update( s.right.generate_translator(code+'1') )

        return trans
    
    def get_total_value(s):
        if s.item != None:
            return s.item.value
        
        total = 0
        if s.right != None:
            total += s.right.get_total_value()
        if s.left != None:
            total += s.left.get_total_value()
        return total
    
    def insert(s, item):
        if s.left == s.right == s.item == None:
            s.item = item
            return

        if s.item != None:
            assert s.left == s.right == None
            s.left = Binary_tree()
            s.left.insert(s.item)
            s.item = None
            s.insert(item)
            return
        
        if s.right == None:
            # only 1 item - left
            s.right = Binary_tree()
            s.right.insert(item)
            if s.right.item.value > s.left.item.value:
                s.right, s.left = s.left, s.right
            return

        # we've got something in both left and right

        # if s.left.item != None:
        #     # we've got (1 item in left)
        #     if item.value > s.left.item.value:
        #         o_l_i = s.left.item
        #         s.left.item = item
        #         s.right.insert(o_l_i)
        #     else:
        #         s.right.insert(item)
        #     return
        
        # else:
        #     # we've got (more than 1 item in left)
        #     ...
        #     assert False, 'not implemented'
    
        left_total = s.left.get_total_value()
        right_total = s.right.get_total_value()
        if right_total + item.value > left_total:
            s.left.insert(item)
        else:
            s.right.insert(item)

        # assert False, 'unreachable'

class Binary_tree_item:
    def __init__(s, value, data):
        s.value = value
        s.data = data
    def __repr__(s):
        return f'{s.value=} {s.data=}'

def compress_file(file_input, file_output):
    tokens = {}

    with open(file_input, 'rb') as f_in:
        while True:
            token = f_in.read(TOKEN_LEN)
            if len(token) == 0:
                break
            assert len(token) == TOKEN_LEN, f'not implemented; currently file len needs to be dividable by {TOKEN_LEN}'

            if token not in tokens:
                tokens[token] = 0

            tokens[token] += 1

    tokens = list(tokens.items())
    tokens.sort(key=lambda t: -t[1])

    bt = Binary_tree()
    for token, count in tokens:
        item = Binary_tree_item(count, token)
        bt.insert(item)
        print(bt)
    
    trans = bt.generate_translator()

    size_original = 0
    size_compressed = 0

    with open(file_input, 'rb') as f_in:
        with open(file_output, 'w') as f_out:
            while True:
                token = f_in.read(TOKEN_LEN)
                if len(token) == 0:
                    break
                assert len(token) == TOKEN_LEN
                size_original += len(token)

                token = trans[token]
                size_compressed += len(token)
                f_out.write(token)
    
    return size_original, size_compressed

if __name__ == '__main__':
    # TODO use argparse
    size_original, size_compressed = compress_file(sys.argv[1], sys.argv[2])
    compressed = size_original - size_compressed
    print(f'compressed {compressed}')

    # ./minq_compressor.py minq_compressor.py compressed
