# Atlantic Giant Pumpkin Diversity Panel - BIGapp Workshop Demo

## Overview
This simulated dataset represents a **GWAS diversity panel** of 200 Atlantic Giant pumpkin 
(*Cucurbita maxima*) accessions collected from breeding programs across the United States.

This dataset is designed to teach realistic GWAS concepts including:
- Population structure driven by geography
- A QTL peak with linkage disequilibrium (LD) structure
- The importance of LD pruning to identify independent signals

## Reference Genome

This dataset uses chromosome coordinates based on the **HZAU telomere-to-telomere assembly**:

| Parameter | Value |
|-----------|-------|
| Assembly | *C. maxima* HZAU (T2T, gap-free) |
| Total size | 345.14 Mb |
| Chromosomes | 20 |
| Scaffold N50 | 19.03 Mb |
| Reference | Zeng et al. (2024) Plant Communications |
| DOI | 10.1016/j.xplc.2024.100935 |

## Population Structure Model

The panel contains accessions from three geographic regions with distinct genetic backgrounds:

| Region | States | N | Mean Fruit Weight | Breeding Focus |
|--------|--------|---|-------------------|----------------|
| Eastern | NY, PA, OH, RI, CT, MA, NJ | 70 | ~1,065 lbs | Traditional giant pumpkin competitions |
| Midwest | WI, IA, IL, IN, MI, MN, NE, MO | 70 | ~965 lbs | Show & processing types |
| Western | CA, OR, WA, CO, AZ | 60 | ~895 lbs | Diverse newer breeding programs |

### How Structure Was Simulated
1. Three ancestral populations with different allele frequencies
2. Each sample has **admixture proportions** (Eastern_Ancestry, Midwest_Ancestry, Western_Ancestry columns)
3. Geography predicts ancestry, but with variation (gene flow between regions)
4. This creates **overlapping clusters** in PCA, not discrete groups

## Files

| File | Description | Size |
|------|-------------|------|
| `atlantic_giant_pumpkin_diversity.vcf` | Genotype data (GT:DP:AD format) | ~3 MB |
| `atlantic_giant_pumpkin_diversity_phenotypes.csv` | Sample metadata + phenotype | ~20 KB |
| `atlantic_giant_pumpkin_diversity_snp_info.csv` | SNP details + QTL annotations | ~75 KB |

## SNP Information

### Distribution
- **1,200 total SNPs** across 20 chromosomes (~60 per chromosome)
- **1,000 high-quality SNPs**: MAF > 0.05, missing < 10%
- **100 low-MAF SNPs**: MAF < 0.05 (for QC filtering demo)
- **100 high-missing SNPs**: >50% missing (for QC filtering demo)

**Note:** Poor-quality SNPs are randomly distributed across ALL chromosomes 
(~5 low-MAF and ~5 high-missing per chromosome). After filtering, each 
chromosome retains ~45-53 good-quality SNPs.

## QTL Region with LD Structure

### The Key Teaching Point
This dataset simulates a **realistic QTL peak** where multiple SNPs appear significant 
due to linkage disequilibrium, not because they are all causal.

### QTL Details (Chromosome 4)

| SNP | Position | Role | r² with Causal | Notes |
|-----|----------|------|----------------|-------|
| **SNP_0240** | 18,967,397 bp | **CAUSAL** | 1.00 | The TRUE QTL - only this SNP affects phenotype |
| SNP_0239 | 18,487,979 bp | Tag (LD) | 0.98 | ~479 kb from causal, significant due to LD |
| SNP_0238 | 18,109,217 bp | Tag (LD) | 0.90 | ~858 kb from causal, significant due to LD |

**Total QTL region span: ~858 kb**

### What This Teaches
1. **GWAS shows 3 significant SNPs** - but they're NOT 3 independent QTLs
2. **After LD filtering** - only 1 signal remains (the QTL region)
3. **Fine-mapping is needed** - to distinguish causal from tag SNPs
4. The causal SNP adds **150 lbs per alt allele** to fruit weight

## Expected Workshop Results

### 1. Principal Component Analysis (PCA)

**Color by Region:**
- Three overlapping clusters visible
- Eastern samples cluster together (but overlap with Midwest)
- Western samples form a separate cluster

**Color by State:**
- Geographic gradient becomes apparent

### 2. Genome-Wide Association Study (GWAS)

**Without kinship/structure correction:**
- Inflated test statistics across genome
- False positive signals

**With kinship correction:**
- Clear peak on Chromosome 4 with **3 significant SNPs**
- All 3 are within ~858 kb of each other

**After LD pruning/clumping:**
- Only **1 independent signal** remains
- This is your candidate QTL region
- The SNP info file tells you which one is truly causal

### 3. Quality Control Filtering

With species ploidy 2, minimum depth 10, MAF 0.05, and 50 percent SNP and sample missingness thresholds:

- Genotype cells below depth 10 are set to missing before missingness is evaluated.
- 100 low-MAF SNPs and 100 high-missingness SNPs are removed.
- 1,000 SNPs and all 200 samples are retained.
- The retained matrix contains 9,447 missing genotype cells.

## Phenotype/Passport Data Columns

| Column | Description |
|--------|-------------|
| Sample_ID | Unique identifier (AGP_001 to AGP_200) |
| State | US state of origin |
| Region | Geographic region (Eastern/Midwest/Western) |
| Breeding_Program | Source breeding program |
| Sequencing_Year | Year sample was sequenced |
| Sequencing_Lane | Sequencing lane ID |
| Plate | 96-well plate number |
| Well | Well position (A1-H12) |
| Eastern_Ancestry | Proportion ancestry from Eastern gene pool |
| Midwest_Ancestry | Proportion ancestry from Midwest gene pool |
| Western_Ancestry | Proportion ancestry from Western gene pool |
| Fruit_Weight_lbs | Fruit weight in pounds (quantitative trait) |

## SNP Info Columns

| Column | Description |
|--------|-------------|
| CHROM | Chromosome |
| POS | Physical position (bp) |
| ID | SNP identifier |
| REF/ALT | Reference and alternate alleles |
| quality_category | good, low_maf, or high_missing |
| is_QTL | TRUE for QTL region SNPs |
| QTL_role | "causal", "tag_LD", or "none" |
| Freq_Eastern/Midwest/Western | Allele frequency in each ancestral population |

## Workshop Teaching Points

### Why Diversity Panels for GWAS?
- Historical recombination breaks up LD, which can improve resolution
- Many alleles segregate, which allows more QTLs to be detected
- BUT: population structure requires careful handling

### Key GWAS Concepts Demonstrated
1. Population structure causes spurious associations
2. Kinship matrices capture cryptic relatedness
3. Mixed models control false positives
4. **Multiple significant SNPs may represent ONE QTL due to LD**
5. LD pruning identifies independent signals
6. Fine-mapping needed to find causal variants

### Suggested Workshop Flow
1. Load data into BIGapp
2. Run PCA and show population structure by Region or State
3. Run GWAS without correction and inspect inflated results
4. Run GWAS with kinship and inspect the Chr04 peak with 3 SNPs
5. Discuss LD filtering and why 3 SNPs can represent 1 QTL
6. Check the SNP info file to reveal the causal variant

## References

**Simulated data** for BIGapp workshop demonstration.

**Reference Genome:**
Zeng Q, Wei M, Li S, et al. (2024). Complete genome assembly provides insights into 
the centromere architecture of pumpkin (*Cucurbita maxima*). Plant Communications 5(9):100935.
https://doi.org/10.1016/j.xplc.2024.100935

**BIGapp:** 
Sandercock A.M., Peel M.D., Taniguti C.H., et al. (2025). BIGapp: A User-Friendly Genomic 
Tool Kit Identified Quantitative Trait Loci for Creeping Rootedness in Alfalfa. The Plant Genome. 
DOI: 10.1002/tpg2.70067
