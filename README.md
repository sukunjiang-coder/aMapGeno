# aMapGeno

**aMapGeno** is a Java/Scala-based framework for **local ancestry inference directly from unphased genotype data**.  
It is designed for single-individual analysis using haplotype-based reference panels and supports both modern and ancient genomic analysis scenarios.

In addition to local ancestry inference, aMapGeno provides an **optional ancestry-guided phasing module (aMapGenoPhase)**, which performs high-accuracy phasing specifically on hetero-ancestry regions.

The software is distributed as executable **JAR** files and can be run on any platform with a Java runtime.

---
## Key Features

- **Direct analysis of unphased genotype data**
- **Supports modern and ancient analysis modes**
- **Explicit handling of ancestry components not present in reference panels (`other`)**
- **Robust to reference haplotypes obtained from statistical or pedigree-based phasing**
- **Optional ancestry-guided phasing for hetero-ancestry regions**

---

## Installation

No installation is required.

Download the packaged JAR file and ensure Java is available on your system.

```bash
java -version
```

Any stable Java version (JDK 8 or later) is sufficient.

---

## Running aMapGeno (Local Ancestry Inference)

Basic usage:

```bash
java -jar aMapGeno.jar -config config.xml
```

### Command-line options

Required:

- `-config <path>`  
  Path to the configuration file (XML).

Optional:

- `-mode <modern|ancient>`  
  Analysis mode (default: `modern`).

- `-jump <int>`  
  Maximum jump times for boundary transitions (default: `2`).

- `-smallSeqS <int>`  
  Fixed small-sequence multiplier (default: `10`).

- `-smallSeqD <int>`  
  Flexible small-sequence multiplier (default: `15`).

---

## Memory Recommendation

aMapGeno is a Java-based application.
For chromosome-scale or genome-wide datasets, explicit memory allocation is strongly recommended.

Example:

```bash
java -Xmx64g -jar aMapGeno.jar -config config.xml
```

---

## Input Files

aMapGeno requires **three types of input files**:

1. **Configuration file**
2. **Sample genotype file (one individual, unphased)**
3. **Reference haplotype files (multiple populations)**

All file paths and parameters are specified in the configuration file.

---

### 1. Configuration File

All inputs are defined in a single XML configuration file.

Key fields include:

- **positionCount**  
This parameter does **not** affect ancestry inference results and usually does not need to be modified.

- **populations**  
  Definitions of one sample file and multiple reference files.
  Each population entry contains:
  - `id`: population identifier
  - `type`: `sample` or `reference`
  - `ordinal`: numeric code used in output
  - `fileName`: genotype or haplotype data file

- **outputDir**  
  Base output path used as a prefix for generated result files.

- **minWinSize**  
  Minimum window size for scanning.

- **winStep**  
  Step size for increasing window length.

- **maxWinSize**  
  Maximum window size for scanning.

See an example configuration file at `test/runData/config.xml` in the repository.


---

### 2. Sample Genotype File

- Contains **one individual only**
- Data are **unphased genotypes**
- File format is identical to reference files

---

### 3. Reference Haplotype Files

- Multiple reference files, each representing one population
- Each file may contain multiple individuals
- Data **must be haplotypes**
- Haplotypes may be obtained from:
  - Statistical phasing
  - Pedigree-based phasing

Minor phasing errors in reference haplotypes are tolerated.

**Note on sample–reference consistency**  
Sample and reference files must be aligned to the same variant set.
This includes consistent genomic coordinates, variant ordering, and allele representation.


---

## Genotype Data Format

Sample and reference files share the same tab-delimited format.

Example:

```
rsID    position    S1_A   S1_B
rs10458597  554484  A   A
rs2185539   556738  C   C
rs11240767  718814  C   C
rs12564807  724325  A   G
```

- Each individual is represented by two columns (`_A` and `_B`)
- Alleles are encoded as `A / T / C / G`
- Sample data are unphased; reference data must be phased

---

## Output Files

Output files preserve variant positions and replace nucleotide alleles with inferred ancestry labels.

Example output:

```
rsID    position    S1_A   S1_B
rs10458597  554484  1   1
rs2185539   556738  1   1
rs11240767  718814  1   1
rs12564807  724325  1   o
```

- Numeric values correspond to reference populations defined by `ordinal` in the configuration file
- `o` (other) denotes ancestry not represented in the reference panel

---

## Optional: aMapGenoPhase (Ancestry-guided Phasing)

aMapGenoPhase is an **optional downstream module** for ancestry-guided phasing. It performs phasing specifically on **hetero-ancestry regions** identified by aMapGeno.

**No additional input files or parameters are required.** The input configuration and genotype/haplotype files are identical to those used by aMapGeno.

The only requirement is that **aMapGeno must be executed first**, as the inferred local ancestry results are implicitly used by aMapGenoPhase.

### Usage

```bash
java -jar aMapGenoPhase.jar -config config.xml
```

No additional command-line options are required.

### Example Output (aMapGenoPhase)

```
ID        POS        NA19924   SegmentID   FinalScore
.         36621906   A/G       0           .
.         36621935   T/T       0           .
.         36622787   C/C       0           .
.         36622815   T/C       0           .
.         36623013   T/T       0           .
.         36634200   A|T       1           15
.         36634291   G|A       1           15
.         36634987   A|A       1           .
.         36635766   T|C       1           15
.         36635938   T|T       1           .
.         36636000   C|C       1           .
.         36636116   G|A       1           15
```

**Column description**

- **Genotype column (e.g., `NA19924`)**  
  Alleles are represented using either `/` or `|`.  
  `/` indicates unphased genotypes, while `|` indicates phased haplotypes.  
  For phased records, the left and right alleles correspond to the ancestry
  assignments inferred by aMapGeno.

- **SegmentID**  
  Index of the hetero-ancestry segment subjected to phasing.  
  `0` indicates regions that were not phased.  
  Positive integers (`1`, `2`, ...) correspond to different hetero-ancestry segments.

- **FinalScore**  
  Quality score of the phasing result for the corresponding segment.  
  `.` indicates positions that were not phased or are homozygous.  
  Scores ≥ 30 indicate high-confidence phasing results.

### Notes

- aMapGenoPhase is not intended as a general-purpose phasing tool
- Phasing is guided by local ancestry information inferred by aMapGeno
- Accuracy is optimized for hetero-ancestry segments

---

## Platform Compatibility

- Linux
- macOS
- Windows

Any platform supporting Java can run aMapGeno.

---

## License

Copyright (c) 2026 Sukun Jiang.
All rights reserved.

---

## Citation

If you use aMapGeno in your research, please cite the corresponding manuscript (in preparation).
