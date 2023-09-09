#! /usr/bin/env python3

import argparse
import sys

PRINT_TREE = False

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

    print('loading tokens')

    with open(file_input, 'rb') as f_in:
        while True:
            token = f_in.read(1)
            if len(token) == 0:
                break

            token = ord(token)
            t0, t1 = (token & 0xff), ((token & 0xff00) >> 8)

            for token in (t0, t1):
                if token not in tokens:
                    tokens[token] = 0

                tokens[token] += 1
        
    print('sorting')

    tokens = list(tokens.items())
    tokens.sort(key=lambda t: -t[1])

    print('loading bt')

    bt = Binary_tree()
    for idx, (token, count) in enumerate(tokens):
        print(f'{idx} / {len(tokens)}')
        item = Binary_tree_item(count, token)
        bt.insert(item)
        if PRINT_TREE:
            print(bt)
    
    print('generating translator')

    trans = bt.generate_translator()

    print('writing back')

    size_original = 0
    size_compressed = 0

    out_buf = ''
    with open(file_input, 'rb') as f_in:
        with open(file_output, 'w') as f_out:
            while True:
                print(size_original)
                token = f_in.read(1)
                if len(token) == 0:
                    break
                size_original += len(token)

                token = ord(token)
                t0, t1 = (token & 0xff), ((token & 0xff00) >> 8)

                t0 = trans[t0]
                t1 = trans[t1]

                out_buf += t0 + t1

                while len(out_buf) > 8:
                    token = out_buf[:8]
                    out_buf = out_buf[8:]

                    token = int(token, base=2)
                    token = chr(token)

                    size_compressed += len(token)
                    f_out.write(token)

    print('done')

    return size_original, size_compressed

if __name__ == '__main__':
    # TODO use argparse
    size_original, size_compressed = compress_file(sys.argv[1], sys.argv[2])
    compressed = size_original - size_compressed
    print(f'compressed {compressed}')

    # ./minq_compressor.py minq_compressor.py compressed
