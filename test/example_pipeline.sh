#!/bin/bash
set -e

###############################################################################
# Example pipeline for running aMapGeno
#
# This script demonstrates:
#   (1) Converting VCF files into aMapGeno input format
#   (2) Running aMapGeno with default parameters
#   (3) Visualizing local ancestry results using AncestryView (optional)
#
# Requirements:
#   - Python 3
#   - Java (>= 8)
#   - aMapGeno.jar
#   - AncestryView (for visualization only)
#   - aMapGenoPhase.jar (for phasing)
###############################################################################


############################
# Step 1: Prepare reference data
############################
# Convert reference population VCF files into aMapGeno haplotype format.
# Each reference file may contain multiple individuals and must represent
# haplotypes (e.g., derived from statistical or pedigree-based phasing).

python to_hap.py -i vcfData/ref1.vcf.gz -o runData/ref1.txt
python to_hap.py -i vcfData/ref2.vcf.gz -o runData/ref2.txt
python to_hap.py -i vcfData/ref3.vcf.gz -o runData/ref3.txt


############################
# Step 2: Prepare sample data
############################
# Convert a single sample VCF file into aMapGeno input format.
# The sample genotype must be UNPHASED.

sampleName=sample1
python to_hap.py -i vcfData/${sampleName}.vcf.gz -o runData/aswSample.txt


############################
# Step 3: Run aMapGeno
############################
# Execute aMapGeno using the provided configuration file.
# Default parameters will be used unless specified in config.xml.

cd runData
java -jar ../../aMapGeno.jar -config config.xml


############################
# Step 4: Visualize results (optional)
############################
# Generate a local ancestry plot using AncestryView.
# This step is OPTIONAL and not part of the core aMapGeno workflow.

java -cp ../../AncestryView/loca-v-2.13_1.4.0.jar \
  -Xmx2048m \
  -XX:-UseGCOverheadLimit \
  com.micinfotech.locav.PlotC \
  -no-water-mark \
  -frame hg19 \
  -pcn POS \
  -colour 1:00DD00:YRI,2:FF0000:CEU,3:0000EE:CHS,o:FFFF00:other \
  -chrinfo chr22:out_final.loca:1:50807702:::${sampleName}_result.png \
  -person s1

echo "Pipeline completed successfully."


############################
# Step 5: Run aMapGenoPhase
############################
java -jar ../../aMapGenoPhase.jar -config config.xml

