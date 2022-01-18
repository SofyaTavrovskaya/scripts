from elftools.elf.elffile import ELFFile
import struct
import sys


def parse_binary():
    path = sys.argv[1]
    with open(path, 'rb') as in_file:
        elffile = ELFFile(in_file)
        go_buildinfo = elffile.get_section_by_name('.go.buildinfo').data()

        go_vers_addr_in_data_section = go_buildinfo[16:][:4]
        go_mod_addr_in_data_section = go_buildinfo[16:][8:12]

        # convert address into little_endian
        addr_go_vers_in_data_section = int(struct.unpack('<I', go_vers_addr_in_data_section)[0])
        addr_go_mod_in_data_section = int(struct.unpack('<I', go_mod_addr_in_data_section)[0])

        data_section = elffile.get_section_by_name('.data')
        data = data_section.data()
        rodata_section = elffile.get_section_by_name('.rodata')
        rodata = rodata_section.data()
        data_with_go_version_var = data[addr_go_vers_in_data_section-data_section.header['sh_addr']:
                                        addr_go_vers_in_data_section + 16 - data_section.header['sh_addr']]
        go_version_var = int(struct.unpack('<I', data_with_go_version_var[:4])[0])
        go_version_var_size = int(struct.unpack('<I', data_with_go_version_var[8:12])[0])

        go_version = rodata[go_version_var - rodata_section.header['sh_addr']:
                            go_version_var + go_version_var_size - rodata_section.header['sh_addr']].decode()
        data_with_go_mod_var = data[addr_go_mod_in_data_section - data_section.header['sh_addr']:
                                    addr_go_mod_in_data_section + 16 - data_section.header['sh_addr']]
        go_mod_var = int(struct.unpack('<I', data_with_go_mod_var[:4])[0])
        go_mod_var_size = int(struct.unpack('<I', data_with_go_mod_var[8:12])[0])
        go_mode = rodata[go_mod_var - rodata_section.header['sh_addr']:
                         go_mod_var + go_mod_var_size - rodata_section.header['sh_addr']]

        if len(go_mode) >= 33 and go_mode[len(go_mode)-17:len(go_mode)-16] == b'\n':
            go_mode = go_mode[16:len(go_mode)-16].decode()
        else:
            go_mode = ""
        print(go_version)
        print(go_mode)


if __name__ == '__main__':
    sys.exit(parse_binary())

