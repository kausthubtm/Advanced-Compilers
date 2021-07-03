import json
import sys
from collections import OrderedDict

TERMINATORS = 'jmp', 'br', 'ret'

def form_blocks(body):
    cur_block = []

    for instr in body:
        if 'op' in instr:
            cur_block.append(instr)

            # check for terminator
            if instr['op'] in TERMINATORS:
                yield cur_block
                cur_block = []

        else:
            if cur_block:
                yield cur_block
            cur_block = [instr]

    if cur_block:
        yield cur_block

def block_map(blocks):
    out = OrderedDict()

    for block in blocks:
        if 'label' in block[0]:
            name = block[0]['label']
            block = block[1:]
        else:
            name = 'b{}'.format(len(out))

        out[name] = block

    return out

def get_cfg(name2block):
    out = {}
    for i, (name, block) in enumerate(name2block.items()):
        last = block[-1]
        if last['op'] in ('jmp', 'br'):
            succ = last['labels']
        elif last['op'] == 'ret':
            succ = []
        else:
            if i == len(name2block)-1:
                succ = []
            else :
                succ = [list(name2block.keys())[i+1]]
    
        out[name] = succ

    return out



def mycfg():
    prog = json.load(sys.stdin)
    for func in prog['functions']:
        name2block = block_map(form_blocks(func['instrs']))
        cfg = get_cfg(name2block)

        print('digraph {} {{'.format(func['name']))
        for name in name2block:
            print('   {};'.format(name))
        for name, succs in cfg.items():
            for succ in succs:
                print('   {}->{};'.format(name,succ))
        print('}')
        

if __name__ == '__main__':
    mycfg()