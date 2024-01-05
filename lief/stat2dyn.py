#!/usr/bin/env python3
import sys
import argparse
import lief
import logging
from lief.ELF import ARCH, E_TYPE, SEGMENT_TYPES, SECTION_TYPES
from lief_common import *

INTERPRETER_DEFAULT = '/lib/ld-linux.so.2'

INTERPRETER_MAP = {
        ARCH.x86_64: '/lib/ld-linux-x86-64.so.2',
        ARCH.i386: INTERPRETER_DEFAULT,
}

def main(argv):
    parser = argparse_default(argparse.ArgumentParser(
            prog=argv[0],
            description='Convert static binaries to dynamic ones for LD_PRELOAD'))
    parser.add_argument('-f', dest='force', action='store_true', help='Force conversion even if the executable is detected')
    parser.add_argument('--interp', help='Specify alternate interpreter path')
    parser.add_argument('--libc', help='Specify alternate libc path')
    parser.add_argument('--libdl', help='Specify alternate libdl path (Specify empty string to omit libdl)')
    parser.add_argument('input', help='Specify input file path')
    parser.add_argument('output', nargs='?', help='Specify output file path. Omit to replace input file.')

    args = parser.parse_args(args=argv[1:])
    executable = lief.ELF.parse(args.input)
    arch = executable.header.machine_type
    if args.interp is None:
        if arch not in INTERPRETER_MAP:
           logging.warning(f'Architecture not recognized! Defaulting to interpreter "{INTERPRETER_DEFAULT}"')
        args.interp = INTERPRETER_MAP.get(arch, INTERPRETER_DEFAULT)

    if args.libc is None:
        args.libc = 'libc.so.6'

    if args.libdl is None:
        args.libdl = 'libdl.so.2'

    if args.output is None:
        args.output = args.input

    if executable.has_interpreter and not args.force:
        logging.error('ELF executable has an interpreter, so not a static binary.')
        logging.error('Use "-f" to do the conversion anyways')
        return 1

    dynsegment = lief.ELF.Segment()
    dynsegment.type = SEGMENT_TYPES.DYNAMIC
    executable.add(dynsegment)

    dynstr = lief.ELF.Section('.dynstr', SECTION_TYPES.STRTAB)
    dynstr.content = memoryview(f'\x00{args.libc}\x00{args.libdl}\x00'.encode())
    executable.add(dynstr)

    dynamic = lief.ELF.Section('.dynamic', SECTION_TYPES.DYNAMIC)
    executable.add(dynamic)

    dynsym = lief.ELF.Section('.dynsym', SECTION_TYPES.DYNSYM)
    executable.add(dynsym)

    executable.interpreter = args.interp
    dynsym = lief.ELF.Symbol()
    dynsym.name = args.libc
    executable.add_dynamic_symbol(dynsym)
    libc_entry = executable.add_library(args.libc)
    libc_entry.value = 1
    print(libc_entry)
    if args.libdl != '':
        dynsym = lief.ELF.Symbol()
        dynsym.name = args.libdl
        executable.add_dynamic_symbol(dynsym)
        libdl_entry = executable.add_library(args.libdl)
        libdl_entry.value = 2 + len(args.libc.encode())
        print(libdl_entry)
    executable.header.file_type = E_TYPE.DYNAMIC
    executable.write(args.input + '.2')
    return 0

if __name__ == '__main__':
    lief.logging.enable()
    logging.error('=====================================')
    logging.error('==== This program does not work! ====')
    logging.error('=====================================')
    sys.exit(main(sys.argv))
