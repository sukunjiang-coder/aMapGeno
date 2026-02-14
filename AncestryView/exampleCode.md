## Example: Visualizing Local Ancestry Results Using AncestryView

This example demonstrates how to generate a local ancestry plot from
aMapGeno output using **AncestryView**.

> **Note**  
> AncestryView is a third-party visualization tool and is **not part of**
> the core aMapGeno software.  
> This step is provided for visualization only and does **not** affect
> aMapGeno inference or analysis results.

---

### Command Example

```bash
java -cp /path/to/AncestryView/loca-v-2.13_1.4.0.jar \
  -Xmx2048m \
  -XX:-UseGCOverheadLimit \
  com.micinfotech.locav.PlotC \
  -no-water-mark \
  -frame hg19 \
  -pcn POS \
  -colour \
    1:00DD00:YRI,\
    2:FF0000:CEU,\
    3:0000EE:CHS,\
    o:FFFF00:other\
  -chrinfo chr10:input_file.loca:start_pos:end_pos:::output_plot.png \
  -person sample1,sample2,sample3,sample4
```

### Parameter explanation

- `-frame hg19`  
  Reference genome build used only for plotting in AncestryView.
  This option is hard-coded to `hg19` in the current AncestryView implementation
  (no `hg38` support available).
  It does not influence aMapGeno inference or output data.


- `-pcn POS`  
  Column name representing genomic positions in the `.loca` file.


- `-colour`  
  Color scheme for ancestry labels in the plot.  
  Format: `label:HEX_COLOR:description`


- `-chrinfo`  
  Genomic region and input/output specification.  
  Format:  
  `chromosome:input_file:start:end:::output_image`


- `-person`  
  Comma-separated list of sample IDs to visualize.
