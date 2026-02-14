#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
to_hap.py – Convert VCF (or VCF.GZ) to a two-column-per-sample haplotype table.

Supported options:
  -i / --input   : input VCF[.gz] file (required)
  -o / --output  : output *.hap file (optional; defaults to input basename + .hap)

Usage examples:
1. Auto-name the output file:
   python3 to_hap.py -i sample.vcf.gz

2. Specify the output file explicitly:
   python3 to_hap.py -i sample.vcf -o my_result.hap

The script preserves all original genotype likelihoods and allelic encoding, simply expanding each sample into two columns (_A and _B) for downstream population-genetic analyses.
"""

#!/usr/bin/env python3
import os, sys, gzip, argparse

def open_vcf(path):
    return gzip.open(path, 'rt') if path.endswith('.gz') else open(path, 'r')

def main():
    parser = argparse.ArgumentParser(
        description='Convert VCF(.gz) to two-column-per-sample haplotype table.')
    parser.add_argument('-i', '--input', required=True,
                        help='Input VCF[.gz] file path')
    parser.add_argument('-o', '--output',
                        help='Output .hap file path (default: replace .vcf/.gz with .hap)')
    args = parser.parse_args()

    vcf_path = args.input
    if not os.path.isfile(vcf_path):
        sys.exit(f'[Error] Input file not found: {vcf_path}')

    if args.output:
        out_path = args.output
    else:
        if vcf_path.endswith('.gz'):
            out_path = vcf_path[:-3] + '.hap'
        elif vcf_path.endswith('.vcf'):
            out_path = vcf_path + '.hap'
        else:
            out_path = vcf_path + '.hap'

    out_dir = os.path.dirname(out_path) or '.'
    if not os.access(out_dir, os.W_OK):
        sys.exit(f'[Error] Output directory is not writable: {out_dir}')

    try:
        with open_vcf(vcf_path) as fin, open(out_path, 'w', newline='') as fout:
            samples = None
            for line in fin:
                if line.startswith('##'):
                    continue
                if line.startswith('#CHROM'):
                    samples = line.rstrip('\n').split('\t')[9:]
                    header = ['ID', 'POS'] + [s + suff for s in samples for suff in ('_A', '_B')]
                    fout.write('\t'.join(header) + '\n')
                    continue
                if samples is None:
                    continue

                parts = line.rstrip('\n').split('\t')
                chrom, pos = parts[0], parts[1]
                var_id = '.' if parts[2] == '.' or parts[2] == '' else parts[2]
                ref, alt = parts[3], parts[4]

                alt_list = alt.split(',')
                if len(ref) != 1 or any(len(a) != 1 for a in alt_list):
                    alleles = ['.'] * (1 + len(alt_list))
                else:
                    alleles = [ref] + alt_list

                out_row = [var_id, pos]
                for gt_field in parts[9:]:
                    gt = gt_field.split(':')[0]
                    if gt in './.':
                        a1 = a2 = '.'
                    else:
                        sep = '|' if '|' in gt else '/'
                        a1, a2 = gt.split(sep)
                        a1 = alleles[int(a1)] if a1 != '.' else '.'
                        a2 = alleles[int(a2)] if a2 != '.' else '.'
                    out_row += [a1, a2]
                fout.write('\t'.join(out_row) + '\n')
    except Exception as e:
        sys.exit(f'[Error] Processing failed: {e}')

    print(f'[Done] Haplotype table written to: {out_path}')

if __name__ == '__main__':
    main()