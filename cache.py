import math


def hex_to_bin(hex_value):
    match hex_value:
        case '0':
            return "0000"
        case '1':
            return "0001"
        case '2':
            return "0010"
        case '3':
            return "0011"
        case '4':
            return "0100"
        case '5':
            return "0101"
        case '6':
            return "0110"
        case '7':
            return "0111"
        case '8':
            return "1000"
        case '9':
            return "1001"
        case 'a':
            return "1010"
        case 'b':
            return "1011"
        case 'c':
            return "1100"
        case 'd':
            return "1101"
        case 'e':
            return "1110"
        case 'f':
            return "1111"


def decode_hex(address_hex: str):
    address_bin: str = ""
    for i in address_hex:
        address_bin += hex_to_bin(i)
    return address_bin


class Cache:
    def __init__(self, block_size, set_num, blocks_per_set, recent_use):
        self.size = block_size * set_num * blocks_per_set
        self.block_size = block_size
        self.set_num = set_num
        self.blocks_per_set = blocks_per_set
        self.cache = [[None] * blocks_per_set] * set_num
        self.offset_size = int(math.log2(self.block_size))
        self.set_field_size = int(math.log2(set_num))
        self.tag_size = int(32 - self.offset_size - self.set_field_size)
        self.recent_use = recent_use

    def replace(self, tag, set_field):

        for i in range(self.cache[set_field].__len__() - 1):
            self.cache[set_field][i] = self.cache[set_field][i + 1]

        self.cache[set_field][self.cache[set_field].__len__() - 1] = tag

    def update(self, tag, set_field):
        block = 0
        for b in range(self.cache[set_field].__len__()):
            if self.cache[set_field][b] == tag:
                block = b

        for i in range(block, self.cache[set_field].__len__() - 1):
            self.cache[set_field][i] = self.cache[set_field][i + 1]

        self.cache[set_field][self.cache[set_field].__len__() - 1] = tag

    def check(self, address_hex):
        address_bin = decode_hex(address_hex)

        tag_bin = address_bin[:self.tag_size]
        set_field_bin = address_bin[self.tag_size + 1:(self.tag_size + self.set_field_size)]
        offset_bin = address_bin[-self.offset_size:]

        tag = int(tag_bin, 2)
        if set_field_bin != "":
            set_field = int(set_field_bin, 2)
        else:
            set_field = 0
        offset = int(offset_bin, 2)

        for i in self.cache[set_field]:
            if i == tag:
                if self.recent_use:
                    self.update(i, set_field)
                return True

        self.replace(tag, set_field)
        return False
