This repository contains the scripts used to analyse the data to study the alleles of the *TtBtr1* genes.


The splotter.py script takes as input the stacked results of FastIBS fastibsmapper (one sample per line) and plots a heatmap based on the *k*-mers coverage.


The reduction_factor.py script was used to compute the reduction factor to apply to the pairwise comparisons of the *k*-mer sets for the phylogeny based on the sets' intersections. 
The reduction factor is needed for differences in sequencing coverage between different samples. 


The three scripts 1_valley_detector.py, 2_tolerant_filtering.py and 3_list_to_matrix.py are needed to process the FastIBS fastibsmapper output files to obtain the local phylogeny.
The first script identifies all the valleys (drop of *k*-mers coverage), the second filters the valleys to distinguish valleys originating from sequencing errors and from real polymorphisms (same as "mac > 2" in a vcf file).
The third scripts convert the list of valleys in a presence/absence matrix to be used as an input for the phylogeny.
