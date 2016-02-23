import sys

MSI = 'MSI'
MESI = 'MESI'
MES = 'MES'
HELP = 'help'

ADDRESS_LENGTH = 16

EMPTY = '<empty>'

M = 'modified'
E = 'exclusive'
S = 'shared'
I = 'invalid'
NONE = None

READ = 'R'
READ_TEXT = 'read'
WRITE = 'W'
WRITE_TEXT = 'write'

NO_MESSAGE = 'No message'

MESSAGE = 'A {0} by P{1} to word {2} looked for tag {3} in cache block {4}, ' \
          'was found in state {5} in this cache.'
MESSAGE_LONG = MESSAGE[:-1] + ' and found in state(s) {6} in the cache(s) of P{7}.'

CPU = 'cpu'

V_FLAG = 'v'
P_FLAG = 'p'
H_FLAG = 'h'
I_FLAG = 'i'
O_FLAG = 'o'
COMMENT_FLAG = '#'


class CacheLine:
    def __init__(self, mes):
        if mes:
            self.state = NONE
        else:
            self.state = I

        self.tags = {}


class Cache:
    def __init__(self, cache_id, line_size, line_count, mode):
        self.cache_id = cache_id

        self.hits_in_M = 0
        self.hits_in_E = 0
        self.hits_in_S = 0
        self.miss_count = 0

        self.read_count = 0
        self.write_count = 0

        # MSI/MESI only
        self.invalidation_count = 0
        self.invalidation_broadcast_count = 0
        self.write_back_message_count = 0

        # MES only
        self.write_update_message_count = 0
        self.update_count = 0

        self.line_size = line_size
        self.line_count = line_count
        self.mode = mode

        self.caches = None

        self.storage = [CacheLine(mode == MES) for x in range(line_count)]

    def access(self, cpu, instruction, address):
        index, offset, tag = self.split_address(address)

        message_chunks = {}

        tag_check = self.tag_check(index, offset, tag)

        if cpu == self.cache_id:
            instruction_text = READ_TEXT if instruction == READ else WRITE_TEXT
            message_chunks = {CPU: self.cache_id,
                              0: instruction_text,
                              1: cpu,
                              2: address,
                              3: tag,
                              4: index,
                              5: None}

            if self.mode == MSI:
                if self.storage[index].state == M:
                    message_chunks[5] = M
                    if tag_check:
                        # read/write hit
                        self.msi_m_rw_hit(index, offset, tag)
                    else:
                        # eviction - write back
                        if instruction == READ:
                            self.msi_m_r_eviction(index, offset, tag)
                        elif instruction == WRITE:
                            self.msi_m_w_eviction(index, offset, tag)
                        message_chunks[5] = I

                elif self.storage[index].state == S:
                    message_chunks[5] = S
                    if tag_check and instruction == READ:
                        # read hit
                        self.msi_s_r_hit(index, offset, tag)
                    elif tag_check and instruction == WRITE:
                        # write hit
                        self.msi_s_w_hit(index, offset, tag)
                    else:
                        # eviction - silent drop
                        if instruction == READ:
                            self.msi_s_r_eviction(index, offset, tag)
                        elif instruction == WRITE:
                            self.msi_s_w_eviction(index, offset, tag)
                        message_chunks[5] = I

                elif self.storage[index].state == I:
                    message_chunks[5] = I
                    if instruction == READ:
                        self.msi_i_r(index, offset, tag)
                    elif instruction == WRITE:
                        self.msi_i_w(index, offset, tag)


            elif self.mode == MESI:
                if self.storage[index].state == M:
                    message_chunks[5] = M
                    if tag_check:
                        # r/w hit
                        self.mesi_m_rw_hit(index, offset, tag)
                    else:
                        # eviction - write back
                        if instruction == READ:
                            self.mesi_m_r_eviction(index, offset, tag)
                        elif instruction == WRITE:
                            self.mesi_m_w_eviction(index, offset, tag)
                        message_chunks[5] = I

                elif self.storage[index].state == E:
                    message_chunks[5] = E
                    if tag_check and instruction == READ:
                        # read hit
                        self.mesi_e_r_hit(index, offset, tag)
                    elif tag_check and instruction == WRITE:
                        # write hit
                        self.mesi_e_w_hit(index, offset, tag)
                    else:
                        # eviction - silent drop
                        if instruction == READ:
                            self.mesi_e_r_eviction(index, offset, tag)
                        elif instruction == WRITE:
                            self.mesi_e_w_eviction(index, offset, tag)
                        message_chunks[5] = I

                elif self.storage[index].state == S:
                    message_chunks[5] = S
                    if tag_check and instruction == READ:
                        # read hit
                        self.mesi_s_r_hit(index, offset, tag)
                    elif tag_check and instruction == WRITE:
                        # write hit
                        self.mesi_s_w_hit(index, offset, tag)
                    else:
                        # eviction - silent drop
                        if instruction == READ:
                            self.mesi_s_r_eviction(index, offset, tag)
                        elif instruction == WRITE:
                            self.mesi_s_w_eviction(index, offset, tag)
                        message_chunks[5] = I

                elif self.storage[index].state == I:
                    message_chunks[5] = I
                    if instruction == READ:
                        self.mesi_i_r(index, offset, tag)
                    elif instruction == WRITE:
                        self.mesi_i_w(index, offset, tag)


            elif self.mode == MES:
                if self.storage[index].state == M:
                    if tag_check:
                        message_chunks[5] = M
                        self.mes_m_rw_hit(index, offset, tag)
                    else:
                        if instruction == READ:
                            self.mes_m_r_miss(index, offset, tag)
                        elif instruction == WRITE:
                            self.mes_m_w_miss(index, offset, tag)
                        message_chunks[5] = NONE

                elif self.storage[index].state == E:
                    if tag_check:
                        message_chunks[5] = E
                        if instruction == READ:
                            self.mes_e_r_hit(index, offset, tag)
                        elif instruction == WRITE:
                            self.mes_e_w_hit(index, offset, tag)
                    else:
                        if instruction == READ:
                            self.mes_e_r_miss(index, offset, tag)
                        elif instruction == WRITE:
                            self.mes_e_w_miss(index, offset, tag)
                        message_chunks[5] = NONE

                elif self.storage[index].state == S:
                    if tag_check:
                        message_chunks[5] = S
                        if instruction == READ:
                            self.mes_s_r_hit(index, offset, tag)
                        elif instruction == WRITE:
                            self.mes_s_w_hit(index, offset, tag)
                    else:
                        if instruction == READ:
                            self.mes_s_r_miss(index, offset, tag)
                        elif instruction == WRITE:
                            self.mes_s_w_miss(index, offset, tag)
                        message_chunks[5] = NONE

                elif self.storage[index].state == NONE:
                    message_chunks[5] = NONE
                    if tag_check:
                        pass
                    else:
                        if instruction == READ:
                            self.mes_none_r_miss(index, offset, tag)
                        elif instruction == WRITE:
                            self.mes_none_w_miss(index, offset, tag)


        elif cpu != self.cache_id:
            message_chunks = {CPU: self.cache_id,
                              0: None}

            if self.mode == MSI:
                if tag_check:
                    if self.storage[index].state == M:
                        if instruction == READ:
                            self.msi_m_remote_r(index, offset, tag)
                        elif instruction == WRITE:
                            self.msi_m_remote_w(index, offset, tag)
                        message_chunks[0] = M

                    elif self.storage[index].state == S:
                        if instruction == READ:
                            self.msi_s_remote_r(index, offset, tag)
                        elif instruction == WRITE:
                            self.msi_s_remote_w(index, offset, tag)
                        message_chunks[0] = S


            elif self.mode == MESI:
                if tag_check:
                    if self.storage[index].state == M:
                        if instruction == READ:
                            self.mesi_m_remote_r(index, offset, tag)
                        elif instruction == WRITE:
                            self.mesi_m_remote_w(index, offset, tag)
                        message_chunks[0] = M

                    elif self.storage[index].state == E:
                        if instruction == READ:
                            self.mesi_e_remote_r(index, offset, tag)
                        elif instruction == WRITE:
                            self.mesi_e_remote_w(index, offset, tag)
                        message_chunks[0] = E

                    elif self.storage[index].state == S:
                        if instruction == READ:
                            self.mesi_s_remote_r(index, offset, tag)
                        elif instruction == WRITE:
                            self.mesi_s_remote_w(index, offset, tag)
                        message_chunks[0] = S


            elif self.mode == MES:
                if tag_check:
                    message_chunks[0] = self.storage[index].state

                    # on remote hit OR miss
                    if self.storage[index].state == M:
                        self.write_back_message_count += 1

                    # remote write requires us to update
                    if instruction == WRITE:
                        self.update_count += 1

                    if self.tag_check(index, offset, tag, cpu):
                        # remote cache hit
                        pass
                    else:
                        # remote cache miss
                        self.storage[index].state = S

                else:
                    message_chunks[0] = NONE

        return message_chunks

    def invalidate(self, index, offset, tag):
        if self.tag_check(index, offset, tag):
            self.invalidation_count += 1
            self.storage[index].state = I
            self.storage[index].tags = {}

    # MSI transitions
    # M
    def msi_m_rw_hit(self, index, offset, tag):
        self.hits_in_M += 1
    def msi_m_r_eviction(self, index, offset, tag):
        self.write_back_message_count += 1
        self.invalidate(index, offset, tag)
        self.msi_i_r(index, offset, tag)
    def msi_m_w_eviction(self, index, offset, tag):
        self.write_back_message_count += 1
        self.invalidate(index, offset, tag)
        self.msi_i_w(index, offset, tag)
    # S
    def msi_s_r_hit(self, index, offset, tag):
        self.hits_in_S += 1
    def msi_s_w_hit(self, index, offset, tag):
        self.hits_in_S += 1
        self.invalidation_broadcast_count += 1
        self.storage[index].state = M
    def msi_s_r_eviction(self, index, offset, tag):
        self.invalidate(index, offset, tag)
        self.msi_i_r(index, offset, tag)
    def msi_s_w_eviction(self, index, offset, tag):
        self.invalidate(index, offset, tag)
        self.msi_i_w(index, offset, tag)
    # I
    def msi_i_r(self, index, offset, tag):
        self.miss_count += 1
        self.storage[index].state = S
        self.storage[index].tags[offset] = tag
    def msi_i_w(self, index, offset, tag):
        self.miss_count += 1
        self.invalidation_broadcast_count += 1
        self.storage[index].state = M
        self.storage[index].tags[offset] = tag

    # M remote
    def msi_m_remote_r(self, index, offset, tag):
        self.write_back_message_count += 1
        self.storage[index].state = S
    def msi_m_remote_w(self, index, offset, tag):
        # no write-back message, as the remote CPU will now have a newer, modified entry
        self.invalidate(index, offset, tag)
    # S remote
    def msi_s_remote_r(self, index, offset, tag):
        pass
    def msi_s_remote_w(self, index, offset, tag):
        self.invalidate(index, offset, tag)

    # MESI transitions
    # M
    def mesi_m_rw_hit(self, index, offset, tag):
        self.hits_in_M += 1
    def mesi_m_r_eviction(self, index, offset, tag):
        self.write_back_message_count += 1
        self.invalidate(index, offset, tag)
        self.mesi_i_r(index, offset, tag)
    def mesi_m_w_eviction(self, index, offset, tag):
        self.write_back_message_count += 1
        self.invalidate(index, offset, tag)
        self.mesi_i_w(index, offset, tag)
    # E
    def mesi_e_r_hit(self, index, offset, tag):
        self.hits_in_E += 1
    def mesi_e_w_hit(self, index, offset, tag):
        self.hits_in_E += 1
        self.storage[index].state = M
    def mesi_e_r_eviction(self, index, offset, tag):
        self.invalidate(index, offset, tag)
        self.mesi_i_r(index, offset, tag)
    def mesi_e_w_eviction(self, index, offset, tag):
        self.invalidate(index, offset, tag)
        self.mesi_i_w(index, offset, tag)
    # S
    def mesi_s_r_hit(self, index, offset, tag):
        self.hits_in_S += 1
    def mesi_s_w_hit(self, index, offset, tag):
        self.hits_in_S += 1
        self.invalidation_broadcast_count += 1
        self.storage[index].state = M
    def mesi_s_r_eviction(self, index, offset, tag):
        self.invalidate(index, offset, tag)
        self.mesi_i_r(index, offset, tag)
    def mesi_s_w_eviction(self, index, offset, tag):
        self.invalidate(index, offset, tag)
        self.mesi_i_w(index, offset, tag)
    # I
    def mesi_i_r(self, index, offset, tag):
        self.miss_count += 1
        if self.only_copy(index, offset, tag):
            self.storage[index].state = E
        else:
            self.storage[index].state = S
        self.storage[index].tags[offset] = tag
    def mesi_i_w(self, index, offset, tag):
        self.miss_count += 1
        self.invalidation_broadcast_count += 1
        self.storage[index].state = M
        self.storage[index].tags[offset] = tag

    # M remote
    def mesi_m_remote_r(self, index, offset, tag):
        self.write_back_message_count += 1
        self.storage[index].state = S
    def mesi_m_remote_w(self, index, offset, tag):
        # no write-back message, as the remote CPU will now have a newer, modified entry
        self.invalidate(index, offset, tag)
    # E remote
    def mesi_e_remote_r(self, index, offset, tag):
        self.storage[index].state = S
    def mesi_e_remote_w(self, index, offset, tag):
        self.invalidate(index, offset, tag)
    # S remote
    def mesi_s_remote_r(self, index, offset, tag):
        pass
    def mesi_s_remote_w(self, index, offset, tag):
        self.invalidate(index, offset, tag)

    # MES transitions
    # M
    def mes_m_rw_hit(self, index, offset, tag):
        self.hits_in_M += 1
    def mes_m_r_miss(self, index, offset, tag):
        self.write_back_message_count += 1
        self.mes_none_r_miss(index, offset, tag)
    def mes_m_w_miss(self, index, offset, tag):
        self.write_back_message_count += 1
        self.mes_none_w_miss(index, offset, tag)
    # E
    def mes_e_r_hit(self, index, offset, tag):
        self.hits_in_E += 1
    def mes_e_w_hit(self, index, offset, tag):
        self.hits_in_E += 1
        self.storage[index].state = M
    def mes_e_r_miss(self, index, offset, tag):
        self.mes_none_r_miss(index, offset, tag)
    def mes_e_w_miss(self, index, offset, tag):
        self.mes_none_w_miss(index, offset, tag)
    # S
    def mes_s_r_hit(self, index, offset, tag):
        self.hits_in_S += 1
    def mes_s_w_hit(self, index, offset, tag):
        self.hits_in_S += 1
        self.write_update_message_count += 1
    def mes_s_r_miss(self, index, offset, tag):
        self.mes_none_r_miss(index, offset, tag)
    def mes_s_w_miss(self, index, offset, tag):
        self.write_update_message_count += 1
        self.mes_none_w_miss(index, offset, tag)
    # none
    def mes_none_r_miss(self, index, offset, tag):
        self.miss_count += 1
        if self.only_copy(index, offset, tag):
            self.storage[index].state = E
        else:
            self.storage[index].state = S
        self.storage[index].tags[offset] = tag
    def mes_none_w_miss(self, index, offset, tag):
        self.miss_count += 1
        if self.only_copy(index, offset, tag):
            self.storage[index].state = M
        else:
            self.write_update_message_count += 1
            self.storage[index].state = S
        self.storage[index].tags[offset] = tag

    def print_text(self, text):
        print "Cache " + str(self.cache_id) + " " + text + ":"

    def print_contents(self):
        self.print_text('cache contents')
        print 'Index\t\tState\t\t\tData'
        for index, item in enumerate(self.storage):
            print_state = item.state if item.state else '-'
            print '{0}\t\t{1}\t\t{2}'.format(index, print_state.ljust(9), item.tags)
        print '\n\n'

    def print_miss_rate(self):
        self.print_text('hit rate')
        hit_total = self.hits_in_M + self.hits_in_E + self.hits_in_S
        total = self.miss_count + hit_total
        if total > 0:
            print '{0}%'.format((hit_total / float(total))*100)
            if hit_total:
                print '{0}% of hits in M'.format((self.hits_in_M / float(hit_total))*100)
                if self.mode != MSI:
                    print '{0}% of hits in E'.format((self.hits_in_E / float(hit_total))*100)
                print '{0}% of hits in S'.format((self.hits_in_S / float(hit_total))*100)
            print '\n'
        else:
            print 'No data\n'

    def print_invalidations(self):
        if self.mode != MES:
            self.print_text('number of invalidations')
            print '{0}\n'.format(self.invalidation_count)

    def print_others(self):
        if self.mode == MES:
            self.print_text('number of updates')
            print '{0}'.format(self.update_count)
            self.print_text('number of write-update messages')
            print '{0}'.format(self.write_update_message_count)
        else:
            self.print_text('number of invalidation broadcasts')
            print '{0}'.format(self.invalidation_broadcast_count)
        self.print_text('number of write-back messages')
        print '{0}\n'.format(self.write_back_message_count)

    def split_address(self, address):
        exp_line_size = get_bin_exponent(self.line_size)
        exp_line_count = get_bin_exponent(self.line_count)

        index = int(address[:exp_line_count], 2)
        offset = int(address[exp_line_count:(exp_line_size + exp_line_count)], 2)
        tag = address[(exp_line_size + exp_line_count):]

        return index, offset, tag

    def tag_check(self, index, offset, tag, cpu=-1):
        if cpu == -1:
            cpu = self.cache_id
        check = False
        if offset in self.caches[cpu].storage[index].tags and self.caches[cpu].storage[index].tags[offset] == tag:
            check = True
        return check

    def only_copy(self, index, offset, tag):
        only = True
        for cache in self.caches:
            if cache.cache_id != self.cache_id:
                if self.tag_check(index, offset, tag, cache.cache_id):
                    only = False
        return only


class Simulator:
    def __init__(self, parameters):
        self.tfile = parameters[0]
        self.mode = parameters[1]
        self.cache_size = parameters[3]
        self.line_size = parameters[2]
        self.line_count = self.cache_size / self.line_size

        self.caches = [Cache(cache_id, self.line_size, self.line_count, self.mode) for cache_id in range(4)]
        for cache in self.caches:
            cache.caches = self.caches

        self.line_by_line = False

        self.read_count = 0
        self.write_count = 0

        self.hit_total = 0
        self.miss_total = 0

        self.invalidation_message_count = 0
        self.data_message_count = 0

        self.private_accesses = 0
        self.shared_accesses = 0

    def run(self):
        for line in self.tfile:
            chunks = line.strip().split(' ')
            if chunks[0] == V_FLAG:
                # toggle verbose
                self.line_by_line = not self.line_by_line
            elif chunks[0] == P_FLAG:
                # print contents
                for cache in self.caches:
                    cache.print_contents()
            elif chunks[0] == H_FLAG:
                # print hit-rate
                for cache in self.caches:
                    cache.print_miss_rate()
            elif chunks[0] == I_FLAG:
                # print invalidations
                for cache in self.caches:
                    cache.print_invalidations()
            elif chunks[0] == O_FLAG:
                # print other stats
                for cache in self.caches:
                    cache.print_others()
            elif chunks[0] == COMMENT_FLAG:
                # a comment
                pass
            else:
                processor = int(chunks[0][1])
                instruction = chunks[1]
                address = ('{0:0'+str(ADDRESS_LENGTH)+'b}').format(int(chunks[2]))

                if instruction == READ:
                    self.read_count += 1
                elif instruction == WRITE:
                    self.write_count += 1

                message_chunks = []
                for cache in self.caches:
                    message_chunks.append(cache.access(processor, instruction, address))
                if self.line_by_line:
                    message_chunks[processor][6] = []
                    message_chunks[processor][7] = []
                    for chunk in message_chunks:
                        if chunk[CPU] != processor and chunk[0]:
                            message_chunks[processor][6].append(chunk[0])
                            message_chunks[processor][7].append(chunk[CPU])
                    if not message_chunks[processor][6]:
                        message = MESSAGE.format(*[v for k, v in message_chunks[processor].items()])
                    else:
                        message = MESSAGE_LONG.format(*[v for k, v in message_chunks[processor].items()])
                    print message + '\n'

        for cache in self.caches:
            self.hit_total += cache.hits_in_M + cache.hits_in_E + cache.hits_in_S
            self.miss_total += cache.miss_count

            self.invalidation_message_count += cache.invalidation_broadcast_count
            self.data_message_count += cache.write_back_message_count + cache.write_update_message_count

            self.private_accesses += cache.hits_in_M + cache.hits_in_E
            self.shared_accesses += cache.hits_in_S
        print "Run complete.\nTotal reads: {0}\nTotal writes: {1}\nOverall hit rate: {2:.2f}%".\
            format(self.read_count, self.write_count, 100 * self.hit_total / float(self.hit_total + self.miss_total))
        if self.mode != MES:
            print "Total invalidation messages: {0}".format(self.invalidation_message_count)
        print "Total data messages: {0}".format(self.data_message_count)
        divisor_private = float(self.private_accesses + self.shared_accesses)
        divisor_shared = float(self.private_accesses + self.shared_accesses)
        if divisor_private != 0:
            print "Private data accesses: {0:.2f}%".format(100 * self.private_accesses / divisor_private)
        else:
            print "Private data accesses: N/A"
        if divisor_shared != 0:
            print "Shared data accesses: {0:.2f}%".format(100 * self.shared_accesses / divisor_shared)
        else:
            print "Shared data accesses: N/A"


def check_args(args):
    # parameters: input file, mode, line size
    if len(args) == 2 and args[1] == HELP:
        print_usage()
    elif len(args) < 4 or len(args) > 5:
        print "Invalid number of arguments"
        print_usage()

    tfile = None
    try:
        tfile = open(args[1])
    except:
        print "Could not open file"
        print_usage()

    if args[2] == MSI or args[2] == MESI or args[2] == MES:
        pass
    else:
        print "Invalid mode"
        print_usage()

    if args[3] == '2' or args[3] == '4' or args[3] == '8' or args[3] == '16':
        pass
    else:
        print "Invalid line size"
        print_usage()

    cache_size = 2048
    if len(args) == 5:
        cache_size = int(args[4])

    return tfile, args[2], int(args[3]), cache_size


def print_usage():
    print "USAGE: python main.py [input file] [mode: MSI|MESI|MES] [line size: 2|4|8|16] [cache size (optional)]"
    sys.exit(0)


def get_bin_exponent(power_two_number):
    clean = True
    for digit in bin(power_two_number)[3:]:
        if digit == '1':
            clean = False

    if clean:
        return len(bin(power_two_number)[2:]) - 1
    else:
        print "Not a power two number!"
        return -1


if __name__ == '__main__':
    params = check_args(sys.argv)

    sim = Simulator(params)
    sim.run()
