# generated by datamodel-codegen:
#   filename:  class_schema.json
#   timestamp: 2024-03-08T00:13:43+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from models.helper_models import Field


class AnnoqData(BaseModel):
    x_1000Gp3_AC: Optional[Field] = None
    x_1000Gp3_AF: Optional[Field] = None
    x_1000Gp3_AFR_AC: Optional[Field] = None
    x_1000Gp3_AFR_AF: Optional[Field] = None
    x_1000Gp3_AMR_AC: Optional[Field] = None
    x_1000Gp3_AMR_AF: Optional[Field] = None
    x_1000Gp3_EAS_AC: Optional[Field] = None
    x_1000Gp3_EAS_AF: Optional[Field] = None
    x_1000Gp3_EUR_AC: Optional[Field] = None
    x_1000Gp3_EUR_AF: Optional[Field] = None
    x_1000Gp3_SAS_AC: Optional[Field] = None
    x_1000Gp3_SAS_AF: Optional[Field] = None
    ALSPAC_AC: Optional[Field] = None
    ALSPAC_AF: Optional[Field] = None
    ALSPAC_AN: Optional[Field] = None
    ANNOVAR_ensembl_Closest_gene: Optional[Field] = None
    ANNOVAR_ensembl_Effect: Optional[Field] = None
    ANNOVAR_ensembl_Exon_Rank: Optional[Field] = None
    ANNOVAR_ensembl_GO_biological_process_complete_list_id: Optional[Field] = None
    ANNOVAR_ensembl_GO_cellular_component_complete_list_id: Optional[Field] = None
    ANNOVAR_ensembl_GO_molecular_function_complete_list_id: Optional[Field] = None
    ANNOVAR_ensembl_Gene_ID: Optional[Field] = None
    ANNOVAR_ensembl_HGVSc: Optional[Field] = None
    ANNOVAR_ensembl_HGVSp: Optional[Field] = None
    ANNOVAR_ensembl_PANTHER_GO_SLIM_biological_process_list_id: Optional[Field] = None
    ANNOVAR_ensembl_PANTHER_GO_SLIM_cellular_component_list_id: Optional[Field] = None
    ANNOVAR_ensembl_PANTHER_GO_SLIM_molecular_function_list_id: Optional[Field] = None
    ANNOVAR_ensembl_PANTHER_GO_SLIM_protein_class_list_id: Optional[Field] = None
    ANNOVAR_ensembl_PANTHER_pathway_list_id: Optional[Field] = None
    ANNOVAR_ensembl_REACTOME_pathway_list_id: Optional[Field] = None
    ANNOVAR_ensembl_Transcript_ID: Optional[Field] = None
    ANNOVAR_ensembl_summary: Optional[Field] = None
    ANNOVAR_refseq_Closest_gene: Optional[Field] = None
    ANNOVAR_refseq_Effect: Optional[Field] = None
    ANNOVAR_refseq_Exon_Rank: Optional[Field] = None
    ANNOVAR_refseq_GO_biological_process_complete_list_id: Optional[Field] = None
    ANNOVAR_refseq_GO_cellular_component_complete_list_id: Optional[Field] = None
    ANNOVAR_refseq_GO_molecular_function_complete_list_id: Optional[Field] = None
    ANNOVAR_refseq_Gene_ID: Optional[Field] = None
    ANNOVAR_refseq_HGVSc: Optional[Field] = None
    ANNOVAR_refseq_HGVSp: Optional[Field] = None
    ANNOVAR_refseq_PANTHER_GO_SLIM_biological_process_list_id: Optional[Field] = None
    ANNOVAR_refseq_PANTHER_GO_SLIM_cellular_component_list_id: Optional[Field] = None
    ANNOVAR_refseq_PANTHER_GO_SLIM_molecular_function_list_id: Optional[Field] = None
    ANNOVAR_refseq_PANTHER_GO_SLIM_protein_class_list_id: Optional[Field] = None
    ANNOVAR_refseq_PANTHER_pathway_list_id: Optional[Field] = None
    ANNOVAR_refseq_REACTOME_pathway_list_id: Optional[Field] = None
    ANNOVAR_refseq_Transcript_ID: Optional[Field] = None
    ANNOVAR_refseq_summary: Optional[Field] = None
    ANNOVAR_ucsc_Closest_gene: Optional[Field] = None
    ANNOVAR_ucsc_Effect: Optional[Field] = None
    ANNOVAR_ucsc_Exon_Rank: Optional[Field] = None
    ANNOVAR_ucsc_Gene_ID: Optional[Field] = None
    ANNOVAR_ucsc_HGVSc: Optional[Field] = None
    ANNOVAR_ucsc_HGVSp: Optional[Field] = None
    ANNOVAR_ucsc_Transcript_ID: Optional[Field] = None
    ANNOVAR_ucsc_summary: Optional[Field] = None
    APPRIS: Optional[Field] = None
    Aloft_Confidence: Optional[Field] = None
    Aloft_Fraction_transcripts_affected: Optional[Field] = None
    Aloft_pred: Optional[Field] = None
    Aloft_prob_Dominant: Optional[Field] = None
    Aloft_prob_Recessive: Optional[Field] = None
    Aloft_prob_Tolerant: Optional[Field] = None
    CADD_phred: Optional[Field] = None
    CADD_raw: Optional[Field] = None
    CADD_raw_rankscore: Optional[Field] = None
    COSMIC_CNT: Optional[Field] = None
    COSMIC_ID: Optional[Field] = None
    DEOGEN2_pred: Optional[Field] = None
    DEOGEN2_rankscore: Optional[Field] = None
    DEOGEN2_score: Optional[Field] = None
    ENCODE_Dnase_cells: Optional[Field] = None
    ENCODE_Dnase_score: Optional[Field] = None
    ENCODE_TFBS: Optional[Field] = None
    ENCODE_TFBS_cells: Optional[Field] = None
    ENCODE_TFBS_score: Optional[Field] = None
    ENCODE_annotated: Optional[Field] = None
    ESP6500_AA_AC: Optional[Field] = None
    ESP6500_AA_AF: Optional[Field] = None
    ESP6500_AC: Optional[Field] = None
    ESP6500_AF: Optional[Field] = None
    ESP6500_EA_AC: Optional[Field] = None
    ESP6500_EA_AF: Optional[Field] = None
    Ensembl_Regulatory_Build_ID: Optional[Field] = None
    Ensembl_Regulatory_Build_TFBS: Optional[Field] = None
    Ensembl_Regulatory_Build_TFBS_matrix: Optional[Field] = None
    Ensembl_Regulatory_Build_feature_type: Optional[Field] = None
    Ensembl_geneid: Optional[Field] = None
    Ensembl_proteinid: Optional[Field] = None
    Ensembl_transcriptid: Optional[Field] = None
    ExAC_AC: Optional[Field] = None
    ExAC_AF: Optional[Field] = None
    ExAC_AFR_AC: Optional[Field] = None
    ExAC_AFR_AF: Optional[Field] = None
    ExAC_AMR_AC: Optional[Field] = None
    ExAC_AMR_AF: Optional[Field] = None
    ExAC_Adj_AC: Optional[Field] = None
    ExAC_Adj_AF: Optional[Field] = None
    ExAC_EAS_AC: Optional[Field] = None
    ExAC_EAS_AF: Optional[Field] = None
    ExAC_FIN_AC: Optional[Field] = None
    ExAC_FIN_AF: Optional[Field] = None
    ExAC_NFE_AC: Optional[Field] = None
    ExAC_NFE_AF: Optional[Field] = None
    ExAC_SAS_AC: Optional[Field] = None
    ExAC_SAS_AF: Optional[Field] = None
    FANTOM5_CAGE_peak_permissive: Optional[Field] = None
    FANTOM5_CAGE_peak_robust: Optional[Field] = None
    FANTOM5_enhancer_differentially_expressed_tissue_cell: Optional[Field] = None
    FANTOM5_enhancer_expressed_tissue_cell: Optional[Field] = None
    FANTOM5_enhancer_permissive: Optional[Field] = None
    FANTOM5_enhancer_robust: Optional[Field] = None
    FANTOM5_enhancer_target: Optional[Field] = None
    FATHMM_converted_rankscore: Optional[Field] = None
    FATHMM_pred: Optional[Field] = None
    FATHMM_score: Optional[Field] = None
    GENCODE_basic: Optional[Field] = None
    GERP_NR: Optional[Field] = None
    GERP_RS: Optional[Field] = None
    GERP_RS_rankscore: Optional[Field] = None
    GRASP_PMID: Optional[Field] = None
    GRASP_ancestry: Optional[Field] = None
    GRASP_p_value: Optional[Field] = None
    GRASP_phenotype: Optional[Field] = None
    GRASP_platform: Optional[Field] = None
    GRASP_rs: Optional[Field] = None
    GTEx_V7_gene: Optional[Field] = None
    GTEx_V7_tissue: Optional[Field] = None
    GWAS_catalog_OR: Optional[Field] = None
    GWAS_catalog_pubmedid: Optional[Field] = None
    GWAS_catalog_rs: Optional[Field] = None
    GWAS_catalog_trait: Optional[Field] = None
    LRT_Omega: Optional[Field] = None
    LRT_converted_rankscore: Optional[Field] = None
    LRT_pred: Optional[Field] = None
    LRT_score: Optional[Field] = None
    M_CAP_pred: Optional[Field] = None
    M_CAP_rankscore: Optional[Field] = None
    M_CAP_score: Optional[Field] = None
    MPC_rankscore: Optional[Field] = None
    MPC_score: Optional[Field] = None
    MVP_rankscore: Optional[Field] = None
    MVP_score: Optional[Field] = None
    MetaLR_pred: Optional[Field] = None
    MetaLR_rankscore: Optional[Field] = None
    MetaLR_score: Optional[Field] = None
    MetaSVM_pred: Optional[Field] = None
    MetaSVM_rankscore: Optional[Field] = None
    MetaSVM_score: Optional[Field] = None
    Motif_breaking: Optional[Field] = None
    MutPred_AAchange: Optional[Field] = None
    MutPred_Top5features: Optional[Field] = None
    MutPred_protID: Optional[Field] = None
    MutPred_rankscore: Optional[Field] = None
    MutPred_score: Optional[Field] = None
    MutationAssessor_pred: Optional[Field] = None
    MutationAssessor_rankscore: Optional[Field] = None
    MutationAssessor_score: Optional[Field] = None
    MutationTaster_AAE: Optional[Field] = None
    MutationTaster_converted_rankscore: Optional[Field] = None
    MutationTaster_model: Optional[Field] = None
    MutationTaster_pred: Optional[Field] = None
    MutationTaster_score: Optional[Field] = None
    ORegAnno_PMID: Optional[Field] = None
    ORegAnno_type: Optional[Field] = None
    PROVEAN_converted_rankscore: Optional[Field] = None
    PROVEAN_pred: Optional[Field] = None
    PROVEAN_score: Optional[Field] = None
    PrimateAI_pred: Optional[Field] = None
    PrimateAI_rankscore: Optional[Field] = None
    PrimateAI_score: Optional[Field] = None
    RegulomeDB_motif: Optional[Field] = None
    RegulomeDB_score: Optional[Field] = None
    Reliability_index: Optional[Field] = None
    SIFT4G_converted_rankscore: Optional[Field] = None
    SIFT4G_pred: Optional[Field] = None
    SIFT4G_score: Optional[Field] = None
    SIFT_converted_rankscore: Optional[Field] = None
    SIFT_pred: Optional[Field] = None
    SIFT_score: Optional[Field] = None
    SnpEff_ensembl_CDS_position: Optional[Field] = None
    SnpEff_ensembl_Distance_to_feature: Optional[Field] = None
    SnpEff_ensembl_Effect: Optional[Field] = None
    SnpEff_ensembl_Effect_impact: Optional[Field] = None
    SnpEff_ensembl_Exon_or_intron_rank: Optional[Field] = None
    SnpEff_ensembl_GO_biological_process_complete_list_id: Optional[Field] = None
    SnpEff_ensembl_GO_cellular_component_complete_list_id: Optional[Field] = None
    SnpEff_ensembl_GO_molecular_function_complete_list_id: Optional[Field] = None
    SnpEff_ensembl_Gene_ID: Optional[Field] = None
    SnpEff_ensembl_Gene_name: Optional[Field] = None
    SnpEff_ensembl_HGVSc: Optional[Field] = None
    SnpEff_ensembl_HGVSp: Optional[Field] = None
    SnpEff_ensembl_LOF: Optional[Field] = None
    SnpEff_ensembl_PANTHER_GO_SLIM_biological_process_list_id: Optional[Field] = None
    SnpEff_ensembl_PANTHER_GO_SLIM_cellular_component_list_id: Optional[Field] = None
    SnpEff_ensembl_PANTHER_GO_SLIM_molecular_function_list_id: Optional[Field] = None
    SnpEff_ensembl_PANTHER_GO_SLIM_protein_class_list_id: Optional[Field] = None
    SnpEff_ensembl_PANTHER_pathway_list_id: Optional[Field] = None
    SnpEff_ensembl_Protein_position: Optional[Field] = None
    SnpEff_ensembl_REACTOME_pathway_list_id: Optional[Field] = None
    SnpEff_ensembl_Sequence_feature: Optional[Field] = None
    SnpEff_ensembl_Sequence_feature_impact: Optional[Field] = None
    SnpEff_ensembl_TF_ID: Optional[Field] = None
    SnpEff_ensembl_TF_binding_effect: Optional[Field] = None
    SnpEff_ensembl_TF_name: Optional[Field] = None
    SnpEff_ensembl_Transcript_ID: Optional[Field] = None
    SnpEff_ensembl_Transcript_biotype: Optional[Field] = None
    SnpEff_ensembl_Warnings: Optional[Field] = None
    SnpEff_ensembl_cDNA_position: Optional[Field] = None
    SnpEff_ensembl_summary: Optional[Field] = None
    SnpEff_refseq_CDS_position: Optional[Field] = None
    SnpEff_refseq_Distance_to_feature: Optional[Field] = None
    SnpEff_refseq_Effect: Optional[Field] = None
    SnpEff_refseq_Effect_impact: Optional[Field] = None
    SnpEff_refseq_Exon_or_intron_rank: Optional[Field] = None
    SnpEff_refseq_GO_biological_process_complete_list_id: Optional[Field] = None
    SnpEff_refseq_GO_cellular_component_complete_list_id: Optional[Field] = None
    SnpEff_refseq_GO_molecular_function_complete_list_id: Optional[Field] = None
    SnpEff_refseq_Gene_ID: Optional[Field] = None
    SnpEff_refseq_Gene_name: Optional[Field] = None
    SnpEff_refseq_HGVSc: Optional[Field] = None
    SnpEff_refseq_HGVSp: Optional[Field] = None
    SnpEff_refseq_LOF: Optional[Field] = None
    SnpEff_refseq_PANTHER_GO_SLIM_biological_process_list_id: Optional[Field] = None
    SnpEff_refseq_PANTHER_GO_SLIM_cellular_component_list_id: Optional[Field] = None
    SnpEff_refseq_PANTHER_GO_SLIM_molecular_function_list_id: Optional[Field] = None
    SnpEff_refseq_PANTHER_GO_SLIM_protein_class_list_id: Optional[Field] = None
    SnpEff_refseq_PANTHER_pathway_list_id: Optional[Field] = None
    SnpEff_refseq_Protein_position: Optional[Field] = None
    SnpEff_refseq_REACTOME_pathway_list_id: Optional[Field] = None
    SnpEff_refseq_Sequence_feature: Optional[Field] = None
    SnpEff_refseq_Sequence_feature_impact: Optional[Field] = None
    SnpEff_refseq_Transcript_ID: Optional[Field] = None
    SnpEff_refseq_Transcript_biotype: Optional[Field] = None
    SnpEff_refseq_Warnings: Optional[Field] = None
    SnpEff_refseq_cDNA_position: Optional[Field] = None
    SnpEff_refseq_summary: Optional[Field] = None
    TSL: Optional[Field] = None
    TWINSUK_AC: Optional[Field] = None
    TWINSUK_AF: Optional[Field] = None
    TWINSUK_AN: Optional[Field] = None
    TargetScan_context_score_percentile: Optional[Field] = None
    UK10K_AC: Optional[Field] = None
    UK10K_AF: Optional[Field] = None
    UK10K_AN: Optional[Field] = None
    UTR3_miRNA_target: Optional[Field] = None
    Uniprot_acc: Optional[Field] = None
    Uniprot_entry: Optional[Field] = None
    VEP_canonical: Optional[Field] = None
    VEP_ensembl_Amino_Acid_Change: Optional[Field] = None
    VEP_ensembl_CANONICAL: Optional[Field] = None
    VEP_ensembl_CCDS: Optional[Field] = None
    VEP_ensembl_CDS_position: Optional[Field] = None
    VEP_ensembl_Codon_Change_or_Distance: Optional[Field] = None
    VEP_ensembl_Consequence: Optional[Field] = None
    VEP_ensembl_Exon_or_Intron_Rank: Optional[Field] = None
    VEP_ensembl_GO_biological_process_complete_list_id: Optional[Field] = None
    VEP_ensembl_GO_cellular_component_complete_list_id: Optional[Field] = None
    VEP_ensembl_GO_molecular_function_complete_list_id: Optional[Field] = None
    VEP_ensembl_Gene_ID: Optional[Field] = None
    VEP_ensembl_Gene_Name: Optional[Field] = None
    VEP_ensembl_HGVSc: Optional[Field] = None
    VEP_ensembl_HGVSp: Optional[Field] = None
    VEP_ensembl_LoF: Optional[Field] = None
    VEP_ensembl_LoF_filter: Optional[Field] = None
    VEP_ensembl_LoF_flags: Optional[Field] = None
    VEP_ensembl_LoF_info: Optional[Field] = None
    VEP_ensembl_PANTHER_GO_SLIM_biological_process_list_id: Optional[Field] = None
    VEP_ensembl_PANTHER_GO_SLIM_cellular_component_list_id: Optional[Field] = None
    VEP_ensembl_PANTHER_GO_SLIM_molecular_function_list_id: Optional[Field] = None
    VEP_ensembl_PANTHER_GO_SLIM_protein_class_list_id: Optional[Field] = None
    VEP_ensembl_PANTHER_pathway_list_id: Optional[Field] = None
    VEP_ensembl_Protein_ID: Optional[Field] = None
    VEP_ensembl_Protein_position: Optional[Field] = None
    VEP_ensembl_REACTOME_pathway_list_id: Optional[Field] = None
    VEP_ensembl_STRAND: Optional[Field] = None
    VEP_ensembl_SWISSPROT: Optional[Field] = None
    VEP_ensembl_Transcript_ID: Optional[Field] = None
    VEP_ensembl_cDNA_position: Optional[Field] = None
    VEP_ensembl_summary: Optional[Field] = None
    VEP_refseq_Amino_Acid_Change: Optional[Field] = None
    VEP_refseq_CANONICAL: Optional[Field] = None
    VEP_refseq_CDS_position: Optional[Field] = None
    VEP_refseq_Codon_Change_or_Distance: Optional[Field] = None
    VEP_refseq_Consequence: Optional[Field] = None
    VEP_refseq_Exon_or_Intron_Rank: Optional[Field] = None
    VEP_refseq_GO_biological_process_complete_list_id: Optional[Field] = None
    VEP_refseq_GO_cellular_component_complete_list_id: Optional[Field] = None
    VEP_refseq_GO_molecular_function_complete_list_id: Optional[Field] = None
    VEP_refseq_Gene_ID: Optional[Field] = None
    VEP_refseq_Gene_Name: Optional[Field] = None
    VEP_refseq_HGVSc: Optional[Field] = None
    VEP_refseq_HGVSp: Optional[Field] = None
    VEP_refseq_LoF: Optional[Field] = None
    VEP_refseq_LoF_filter: Optional[Field] = None
    VEP_refseq_LoF_flags: Optional[Field] = None
    VEP_refseq_LoF_info: Optional[Field] = None
    VEP_refseq_PANTHER_GO_SLIM_biological_process_list_id: Optional[Field] = None
    VEP_refseq_PANTHER_GO_SLIM_cellular_component_list_id: Optional[Field] = None
    VEP_refseq_PANTHER_GO_SLIM_molecular_function_list_id: Optional[Field] = None
    VEP_refseq_PANTHER_GO_SLIM_protein_class_list_id: Optional[Field] = None
    VEP_refseq_PANTHER_pathway_list_id: Optional[Field] = None
    VEP_refseq_Protein_ID: Optional[Field] = None
    VEP_refseq_Protein_position: Optional[Field] = None
    VEP_refseq_REACTOME_pathway_list_id: Optional[Field] = None
    VEP_refseq_STRAND: Optional[Field] = None
    VEP_refseq_Transcript_ID: Optional[Field] = None
    VEP_refseq_cDNA_position: Optional[Field] = None
    VEP_refseq_summary: Optional[Field] = None
    aaalt: Optional[Field] = None
    aapos: Optional[Field] = None
    aaref: Optional[Field] = None
    alt: Optional[Field] = None
    cds_strand: Optional[Field] = None
    chr: Optional[Field] = None
    clinvar_MedGen_id: Optional[Field] = None
    clinvar_OMIM_id: Optional[Field] = None
    clinvar_Orphanet_id: Optional[Field] = None
    clinvar_clnsig: Optional[Field] = None
    clinvar_hgvs: Optional[Field] = None
    clinvar_id: Optional[Field] = None
    clinvar_review: Optional[Field] = None
    clinvar_trait: Optional[Field] = None
    clinvar_var_source: Optional[Field] = None
    codon_degeneracy: Optional[Field] = None
    codonpos: Optional[Field] = None
    enhancer_linked_GO_biological_process_complete_list_id: Optional[Field] = None
    enhancer_linked_GO_cellular_component_complete_list_id: Optional[Field] = None
    enhancer_linked_GO_molecular_function_complete_list_id: Optional[Field] = None
    enhancer_linked_PANTHER_GO_SLIM_biological_process_list_id: Optional[Field] = None
    enhancer_linked_PANTHER_GO_SLIM_cellular_component_list_id: Optional[Field] = None
    enhancer_linked_PANTHER_GO_SLIM_molecular_function_list_id: Optional[Field] = None
    enhancer_linked_REACTOME_pathway_list_id: Optional[Field] = None
    enhancer_linked_enhancer: Optional[Field] = None
    enhancer_linked_genes: Optional[Field] = None
    fathmm_MKL_coding_group: Optional[Field] = None
    fathmm_MKL_coding_pred: Optional[Field] = None
    fathmm_MKL_coding_rankscore: Optional[Field] = None
    fathmm_MKL_coding_score: Optional[Field] = None
    fathmm_MKL_non_coding_group: Optional[Field] = None
    fathmm_MKL_non_coding_pred: Optional[Field] = None
    fathmm_MKL_non_coding_rankscore: Optional[Field] = None
    fathmm_MKL_non_coding_score: Optional[Field] = None
    fathmm_XF_coding_or_noncoding: Optional[Field] = None
    fathmm_XF_pred: Optional[Field] = None
    fathmm_XF_rankscore: Optional[Field] = None
    fathmm_XF_score: Optional[Field] = None
    flanking_0_GO_biological_process_complete_list_id: Optional[Field] = None
    flanking_0_GO_cellular_component_complete_list_id: Optional[Field] = None
    flanking_0_GO_molecular_function_complete_list_id: Optional[Field] = None
    flanking_0_PANTHER_GO_SLIM_biological_process_list_id: Optional[Field] = None
    flanking_0_PANTHER_GO_SLIM_cellular_component_list_id: Optional[Field] = None
    flanking_0_PANTHER_GO_SLIM_molecular_function_list_id: Optional[Field] = None
    flanking_0_PANTHER_pathway_list_id: Optional[Field] = None
    flanking_0_REACTOME_pathway_list_id: Optional[Field] = None
    flanking_10000_GO_biological_process_complete_list_id: Optional[Field] = None
    flanking_10000_GO_cellular_component_complete_list_id: Optional[Field] = None
    flanking_10000_GO_molecular_function_complete_list_id: Optional[Field] = None
    flanking_10000_PANTHER_GO_SLIM_biological_process_list_id: Optional[Field] = None
    flanking_10000_PANTHER_GO_SLIM_cellular_component_list_id: Optional[Field] = None
    flanking_10000_PANTHER_GO_SLIM_molecular_function_list_id: Optional[Field] = None
    flanking_10000_PANTHER_pathway_list_id: Optional[Field] = None
    flanking_10000_REACTOME_pathway_list_id: Optional[Field] = None
    flanking_20000_GO_biological_process_complete_list_id: Optional[Field] = None
    flanking_20000_GO_cellular_component_complete_list_id: Optional[Field] = None
    flanking_20000_GO_molecular_function_complete_list_id: Optional[Field] = None
    flanking_20000_PANTHER_GO_SLIM_biological_process_list_id: Optional[Field] = None
    flanking_20000_PANTHER_GO_SLIM_cellular_component_list_id: Optional[Field] = None
    flanking_20000_PANTHER_GO_SLIM_molecular_function_list_id: Optional[Field] = None
    flanking_20000_PANTHER_GO_SLIM_protein_class_list_id: Optional[Field] = None
    flanking_20000_PANTHER_pathway_list_id: Optional[Field] = None
    flanking_20000_REACTOME_pathway_list_id: Optional[Field] = None
    funseq_noncoding_score: Optional[Field] = None
    genename: Optional[Field] = None
    gnomAD_exomes_AC: Optional[Field] = None
    gnomAD_exomes_AF: Optional[Field] = None
    gnomAD_exomes_AFR_AC: Optional[Field] = None
    gnomAD_exomes_AFR_AF: Optional[Field] = None
    gnomAD_exomes_AFR_AN: Optional[Field] = None
    gnomAD_exomes_AFR_nhomalt: Optional[Field] = None
    gnomAD_exomes_AMR_AC: Optional[Field] = None
    gnomAD_exomes_AMR_AF: Optional[Field] = None
    gnomAD_exomes_AMR_AN: Optional[Field] = None
    gnomAD_exomes_AMR_nhomalt: Optional[Field] = None
    gnomAD_exomes_AN: Optional[Field] = None
    gnomAD_exomes_ASJ_AC: Optional[Field] = None
    gnomAD_exomes_ASJ_AF: Optional[Field] = None
    gnomAD_exomes_ASJ_AN: Optional[Field] = None
    gnomAD_exomes_ASJ_nhomalt: Optional[Field] = None
    gnomAD_exomes_EAS_AC: Optional[Field] = None
    gnomAD_exomes_EAS_AF: Optional[Field] = None
    gnomAD_exomes_EAS_AN: Optional[Field] = None
    gnomAD_exomes_EAS_nhomalt: Optional[Field] = None
    gnomAD_exomes_FIN_AC: Optional[Field] = None
    gnomAD_exomes_FIN_AF: Optional[Field] = None
    gnomAD_exomes_FIN_AN: Optional[Field] = None
    gnomAD_exomes_FIN_nhomalt: Optional[Field] = None
    gnomAD_exomes_NFE_AC: Optional[Field] = None
    gnomAD_exomes_NFE_AF: Optional[Field] = None
    gnomAD_exomes_NFE_AN: Optional[Field] = None
    gnomAD_exomes_NFE_nhomalt: Optional[Field] = None
    gnomAD_exomes_POPMAX_AC: Optional[Field] = None
    gnomAD_exomes_POPMAX_AF: Optional[Field] = None
    gnomAD_exomes_POPMAX_AN: Optional[Field] = None
    gnomAD_exomes_POPMAX_nhomalt: Optional[Field] = None
    gnomAD_exomes_SAS_AC: Optional[Field] = None
    gnomAD_exomes_SAS_AF: Optional[Field] = None
    gnomAD_exomes_SAS_AN: Optional[Field] = None
    gnomAD_exomes_SAS_nhomalt: Optional[Field] = None
    gnomAD_exomes_controls_AC: Optional[Field] = None
    gnomAD_exomes_controls_AF: Optional[Field] = None
    gnomAD_exomes_controls_AFR_AC: Optional[Field] = None
    gnomAD_exomes_controls_AFR_AF: Optional[Field] = None
    gnomAD_exomes_controls_AFR_AN: Optional[Field] = None
    gnomAD_exomes_controls_AFR_nhomalt: Optional[Field] = None
    gnomAD_exomes_controls_AMR_AC: Optional[Field] = None
    gnomAD_exomes_controls_AMR_AF: Optional[Field] = None
    gnomAD_exomes_controls_AMR_AN: Optional[Field] = None
    gnomAD_exomes_controls_AMR_nhomalt: Optional[Field] = None
    gnomAD_exomes_controls_AN: Optional[Field] = None
    gnomAD_exomes_controls_ASJ_AC: Optional[Field] = None
    gnomAD_exomes_controls_ASJ_AF: Optional[Field] = None
    gnomAD_exomes_controls_ASJ_AN: Optional[Field] = None
    gnomAD_exomes_controls_ASJ_nhomalt: Optional[Field] = None
    gnomAD_exomes_controls_EAS_AC: Optional[Field] = None
    gnomAD_exomes_controls_EAS_AF: Optional[Field] = None
    gnomAD_exomes_controls_EAS_AN: Optional[Field] = None
    gnomAD_exomes_controls_EAS_nhomalt: Optional[Field] = None
    gnomAD_exomes_controls_FIN_AC: Optional[Field] = None
    gnomAD_exomes_controls_FIN_AF: Optional[Field] = None
    gnomAD_exomes_controls_FIN_AN: Optional[Field] = None
    gnomAD_exomes_controls_FIN_nhomalt: Optional[Field] = None
    gnomAD_exomes_controls_NFE_AC: Optional[Field] = None
    gnomAD_exomes_controls_NFE_AF: Optional[Field] = None
    gnomAD_exomes_controls_NFE_AN: Optional[Field] = None
    gnomAD_exomes_controls_NFE_nhomalt: Optional[Field] = None
    gnomAD_exomes_controls_POPMAX_AC: Optional[Field] = None
    gnomAD_exomes_controls_POPMAX_AF: Optional[Field] = None
    gnomAD_exomes_controls_POPMAX_AN: Optional[Field] = None
    gnomAD_exomes_controls_POPMAX_nhomalt: Optional[Field] = None
    gnomAD_exomes_controls_SAS_AC: Optional[Field] = None
    gnomAD_exomes_controls_SAS_AF: Optional[Field] = None
    gnomAD_exomes_controls_SAS_AN: Optional[Field] = None
    gnomAD_exomes_controls_SAS_nhomalt: Optional[Field] = None
    gnomAD_exomes_controls_nhomalt: Optional[Field] = None
    gnomAD_exomes_flag: Optional[Field] = None
    gnomAD_exomes_nhomalt: Optional[Field] = None
    gnomAD_genomes_AC: Optional[Field] = None
    gnomAD_genomes_AF: Optional[Field] = None
    gnomAD_genomes_AFR_AC: Optional[Field] = None
    gnomAD_genomes_AFR_AF: Optional[Field] = None
    gnomAD_genomes_AFR_AN: Optional[Field] = None
    gnomAD_genomes_AFR_nhomalt: Optional[Field] = None
    gnomAD_genomes_AMR_AC: Optional[Field] = None
    gnomAD_genomes_AMR_AF: Optional[Field] = None
    gnomAD_genomes_AMR_AN: Optional[Field] = None
    gnomAD_genomes_AMR_nhomalt: Optional[Field] = None
    gnomAD_genomes_AN: Optional[Field] = None
    gnomAD_genomes_ASJ_AC: Optional[Field] = None
    gnomAD_genomes_ASJ_AF: Optional[Field] = None
    gnomAD_genomes_ASJ_AN: Optional[Field] = None
    gnomAD_genomes_ASJ_nhomalt: Optional[Field] = None
    gnomAD_genomes_EAS_AC: Optional[Field] = None
    gnomAD_genomes_EAS_AF: Optional[Field] = None
    gnomAD_genomes_EAS_AN: Optional[Field] = None
    gnomAD_genomes_EAS_nhomalt: Optional[Field] = None
    gnomAD_genomes_FIN_AC: Optional[Field] = None
    gnomAD_genomes_FIN_AF: Optional[Field] = None
    gnomAD_genomes_FIN_AN: Optional[Field] = None
    gnomAD_genomes_FIN_nhomalt: Optional[Field] = None
    gnomAD_genomes_NFE_AC: Optional[Field] = None
    gnomAD_genomes_NFE_AF: Optional[Field] = None
    gnomAD_genomes_NFE_AN: Optional[Field] = None
    gnomAD_genomes_NFE_nhomalt: Optional[Field] = None
    gnomAD_genomes_POPMAX_AC: Optional[Field] = None
    gnomAD_genomes_POPMAX_AF: Optional[Field] = None
    gnomAD_genomes_POPMAX_AN: Optional[Field] = None
    gnomAD_genomes_POPMAX_nhomalt: Optional[Field] = None
    gnomAD_genomes_controls_AC: Optional[Field] = None
    gnomAD_genomes_controls_AF: Optional[Field] = None
    gnomAD_genomes_controls_AFR_AC: Optional[Field] = None
    gnomAD_genomes_controls_AFR_AF: Optional[Field] = None
    gnomAD_genomes_controls_AFR_AN: Optional[Field] = None
    gnomAD_genomes_controls_AFR_nhomalt: Optional[Field] = None
    gnomAD_genomes_controls_AMR_AC: Optional[Field] = None
    gnomAD_genomes_controls_AMR_AF: Optional[Field] = None
    gnomAD_genomes_controls_AMR_AN: Optional[Field] = None
    gnomAD_genomes_controls_AMR_nhomalt: Optional[Field] = None
    gnomAD_genomes_controls_AN: Optional[Field] = None
    gnomAD_genomes_controls_ASJ_AC: Optional[Field] = None
    gnomAD_genomes_controls_ASJ_AF: Optional[Field] = None
    gnomAD_genomes_controls_ASJ_AN: Optional[Field] = None
    gnomAD_genomes_controls_ASJ_nhomalt: Optional[Field] = None
    gnomAD_genomes_controls_EAS_AC: Optional[Field] = None
    gnomAD_genomes_controls_EAS_AF: Optional[Field] = None
    gnomAD_genomes_controls_EAS_AN: Optional[Field] = None
    gnomAD_genomes_controls_EAS_nhomalt: Optional[Field] = None
    gnomAD_genomes_controls_FIN_AC: Optional[Field] = None
    gnomAD_genomes_controls_FIN_AF: Optional[Field] = None
    gnomAD_genomes_controls_FIN_AN: Optional[Field] = None
    gnomAD_genomes_controls_FIN_nhomalt: Optional[Field] = None
    gnomAD_genomes_controls_NFE_AC: Optional[Field] = None
    gnomAD_genomes_controls_NFE_AF: Optional[Field] = None
    gnomAD_genomes_controls_NFE_AN: Optional[Field] = None
    gnomAD_genomes_controls_NFE_nhomalt: Optional[Field] = None
    gnomAD_genomes_controls_POPMAX_AC: Optional[Field] = None
    gnomAD_genomes_controls_POPMAX_AF: Optional[Field] = None
    gnomAD_genomes_controls_POPMAX_AN: Optional[Field] = None
    gnomAD_genomes_controls_POPMAX_nhomalt: Optional[Field] = None
    gnomAD_genomes_controls_nhomalt: Optional[Field] = None
    gnomAD_genomes_flag: Optional[Field] = None
    gnomAD_genomes_nhomalt: Optional[Field] = None
    network_hub: Optional[Field] = None
    pos: Optional[Field] = None
    ref: Optional[Field] = None
    refcodon: Optional[Field] = None
    rs_dbSNP151: Optional[Field] = None
    sensitive: Optional[Field] = None
    sno_miRNA_name: Optional[Field] = None
    sno_miRNA_type: Optional[Field] = None
    splicing_consensus_ada_score: Optional[Field] = None
    splicing_consensus_rf_score: Optional[Field] = None
    target_gene: Optional[Field] = None
    ultra_sensitive: Optional[Field] = None
