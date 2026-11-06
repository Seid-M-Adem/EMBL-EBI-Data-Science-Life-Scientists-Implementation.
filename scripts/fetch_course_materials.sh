#!/usr/bin/env bash
# Fetch the official EMBL-EBI "Data science for life scientists" (2026 edition) materials
# and place them in the matching module folders of this repository.
#
# Usage:
#   scripts/fetch_course_materials.sh            # slides, notebooks, tutorial code (committed)
#   scripts/fetch_course_materials.sh --local    # + unlicensed repo, reference papers, live Colab versions (git-ignored)
#   scripts/fetch_course_materials.sh --data     # + project datasets into data/raw (~730 MB, git-ignored)
#   scripts/fetch_course_materials.sh --2025     # + 2025 course edition: slides, notebooks, data (~330 MB, git-ignored)
#   scripts/fetch_course_materials.sh --all      # everything
#
# Source: https://www.ebi.ac.uk/training/materials/data-science-for-life-scientists-materials-2026/
# Licence of EMBL-EBI materials: CC BY 4.0 — see COURSE_MATERIALS.md for attribution.
# Re-running is safe: files that already exist are skipped.
set -euo pipefail

cd "$(dirname "$0")/.."
FTP="https://ftp.ebi.ac.uk/pub/training/2026/Data_science_for_life_scientists_2026"
FTP25="https://ftp.ebi.ac.uk/pub/training/2025/Data_science_for_Life_Scientists_2025"
WITH_LOCAL=false
WITH_DATA=false
WITH_2025=false
for arg in "$@"; do
  case "$arg" in
    --local) WITH_LOCAL=true ;;
    --data)  WITH_DATA=true ;;
    --2025)  WITH_2025=true ;;
    --all)   WITH_LOCAL=true; WITH_DATA=true; WITH_2025=true ;;
    -h|--help) sed -n '2,14p' "$0"; exit 0 ;;
    *) echo "Unknown option: $arg (see --help)" >&2; exit 1 ;;
  esac
done

# get <remote path relative to FTP> <local destination file>
get() {
  local src="$FTP/$1" dest="$2"
  if [[ -s "$dest" ]]; then echo "  ✓ exists  $dest"; return; fi
  mkdir -p "$(dirname "$dest")"
  echo "  ↓ $dest"
  curl -fsSL --retry 5 --retry-delay 3 --retry-all-errors --connect-timeout 30 -o "$dest.part" "$src"
  mv "$dest.part" "$dest"
}

# drive_nb <Google Drive / Colab file id> <destination .ipynb>
# Downloads a shared Colab notebook and strips its outputs (they can embed third-party images) and its
# Colab metadata (it records who ran each cell: display name and Google user id).
drive_nb() {
  local id="$1" dest="$2"
  if [[ -s "$dest" ]]; then echo "  ✓ exists  $dest"; return; fi
  mkdir -p "$(dirname "$dest")"
  echo "  ↓ $dest  (Colab $id, outputs stripped)"
  curl -fsSL --retry 5 --retry-delay 3 --retry-all-errors --connect-timeout 30 -o "$dest.part" \
    "https://drive.google.com/uc?export=download&id=$id"
  python3 -I -c '
import json, sys
src, dest = sys.argv[1], sys.argv[2]
nb = json.load(open(src, encoding="utf-8"))
for c in nb["cells"]:
    c["metadata"] = {}  # Colab stores executionInfo (runner name, Google user id), outputId, etc.
    if c["cell_type"] == "code":
        c["outputs"], c["execution_count"] = [], None
for k in ("widgets", "colab", "accelerator", "gpuClass"):
    nb.get("metadata", {}).pop(k, None)
json.dump(nb, open(dest, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
open(dest, "a").write("\n")
' "$dest.part" "$dest"
  rm -f "$dest.part"
}

# get2025 <path relative to the 2025 FTP folder> <local destination file>
get2025() { FTP="$FTP25" get "$1" "$2"; }

# clone_snapshot <github owner/repo> <destination> <keep_git: true|false>
clone_snapshot() {
  local repo="$1" dest="$2" keep_git="$3"
  if [[ -d "$dest" ]]; then echo "  ✓ exists  $dest"; return; fi
  echo "  ↓ github.com/$repo → $dest"
  git clone --quiet --depth 1 "https://github.com/$repo.git" "$dest"
  local sha; sha="$(git -C "$dest" rev-parse HEAD)"
  if [[ "$keep_git" == false ]]; then
    rm -rf "$dest/.git"
    printf 'Snapshot of https://github.com/%s at commit %s (fetched %s)\n' \
      "$repo" "$sha" "$(date -u +%Y-%m-%d)" > "$dest/SNAPSHOT_SOURCE.txt"
  fi
}

M01="01_introduction_to_embl_ebi/course_materials"
M02a="02_accessing_and_handling_data/01_apis_and_data_collection/course_materials"
M02b="02_accessing_and_handling_data/02_handling_and_visualisation/course_materials"
M03a="03_foundations_of_machine_learning/01_intro_and_fundamentals/course_materials"
M03b="03_foundations_of_machine_learning/02_hyperparameters_and_performance/course_materials"
M04a="04_foundations_of_deep_learning/01_dnn_and_transformers/course_materials"
M04b="04_foundations_of_deep_learning/02_evaluation_and_visualisation/course_materials"
M04c="04_foundations_of_deep_learning/03_intro_to_llms/course_materials"
GE="05_group_projects/gene_expression/course_materials"
BI="05_group_projects/bioimaging/course_materials"

echo "==> Slides & notebooks (CC BY 4.0, committed)"
get "Day_1/OCathail_DataScience2026_IntrotoEBI.pdf"                       "$M01/Intro_to_EMBL-EBI.pdf"
get "Day_2/APIs_and_Python_data%20science_for_life_scientists_course.pdf" "$M02a/APIs_and_Python_for_data_collection.pdf"
get "Day_2/PyLab-teaching-slides.pdf"                                     "$M02b/PyLab_teaching_slides.pdf"
get "Day_1/Intro_to_AI_EBI.pdf"                                           "$M03a/Intro_to_ML.pdf"
get "Day_3/ML_Algorithms_public.pdf"                                      "$M03a/ML_fundamentals_and_algorithms.pdf"
get "Day_3/Data_hyperparameters_and_model_performance.pdf"                "$M03b/Data_hyperparameters_and_model_performance.pdf"
get "Day_4/Introduction_to_DNNs_Transformers.pdf"                         "$M04a/Introduction_to_DNNs_and_Transformers.pdf"
get "Day_4/session1A_dnn_pubmed_rct20k_tutorial.ipynb"                    "$M04a/session1A_dnn_pubmed_rct20k_tutorial.ipynb"
get "Day_4/session1B__finetune_a_pretrained_transformer.ipynb"            "$M04a/session1B_finetune_a_pretrained_transformer.ipynb"
get "Day_4/Deep_learning_model_evaluation_visualisation.pdf"              "$M04b/Deep_learning_model_evaluation_and_visualisation.pdf"
get "Day_4/session2_model_evaluation_visualisation.ipynb"                 "$M04b/session2_model_evaluation_visualisation.ipynb"
get "Day_5/Intro_to_LLMs_EBI_DAT26.pdf"                                   "$M04c/Intro_to_LLMs.pdf"
get "Gene_expression_project/Concepts_and_models.pdf"                     "$GE/Concepts_and_models.pdf"
get "Gene_expression_project/EBI_Data_download.pdf"                       "$GE/EBI_Data_download.pdf"
get "Gene_expression_project/Code/01_DataDownload.ipynb"                  "$GE/code/01_data_download.ipynb"
get "Gene_expression_project/Code/Gene_expression_2026_classification%20part%201.ipynb" "$GE/code/02_classification_part1.ipynb"
get "Gene_expression_project/Code/Gene_expression_2026_classification%20part%202.ipynb" "$GE/code/03_classification_part2.ipynb"
get "Gene_expression_project/Code/Gene_expression_2026_clustering.ipynb"  "$GE/code/04_clustering.ipynb"
get "Bioimaging_project/2026_06_15_EMBL-EBI_DataScienceForLifeScientists_Ollitrault.pdf" "$BI/Bioimaging_project_overview.pdf"
# 03.2 image-augmentation demo exists only on Colab (linked from the session page)
drive_nb 18Ew7O8HnyhlUAkK9lNfwV9By3qTltlM6 "$M03b/image_augmentation_colab.ipynb"

echo "==> Tutorial code (open licences, committed)"
clone_snapshot "SandyRogers/python-data-tutorials" "$M02a/python-data-tutorials" false  # Apache-2.0
clone_snapshot "mevol/DataScience_EBI"             "$M03b/DataScience_EBI"        false  # MIT (also used by structural biology project)

if $WITH_LOCAL; then
  echo "==> Local-only resources (no redistribution licence — git-ignored)"
  clone_snapshot "ewald-lab/2026_DataScienceForLifeScientists_Training" "$BI/local/ewald-lab-training" true
  for f in 1-s2.0-S1746809422004554-main.pdf 1908.06278v1.pdf 43588_2025_Article_916.pdf \
           TCBB.2023.3328029.pdf danaee.pdf fgene-10-00166.pdf s12864-017-4226-0.pdf; do
    get "Gene_expression_project/References/$f" "$GE/local/references/$f"
  done
  # Live Colab versions of the 04.x notebooks. Trainers kept editing these after the FTP snapshot,
  # which stays the canonical committed copy. NB: the course page swaps the 1A/1B links; ids below are correct.
  drive_nb 1WDO6TtHylzrw3HpLMzIqQsQ5WNPVzDc- "$M04a/local/colab/session1A_dnn_pubmed_rct20k_tutorial.ipynb"
  drive_nb 1TInWLPKvYTG9icYRuHp2LKp2muX7HqhX "$M04a/local/colab/session1B_finetune_a_pretrained_transformer.ipynb"
  drive_nb 1ldJZHM8150Lc3Y3z9r6gCLGiYMW_1fEX "$M04b/local/colab/session2_model_evaluation_visualisation.ipynb"
fi

if $WITH_DATA; then
  echo "==> Project datasets (git-ignored)"
  for f in gene_expresion_prostate_cancer.RDS genes_cancer_prostata_bibliografia.txt labels.tsv \
           pan_cancer_dataset.RDS pan_cancer_proteomics.txt pheno_prostate_cancer.RDS; do
    get "Gene_expression_project/Data/$f" "data/raw/gene_expression/$f"
  done
  for f in BR00127145.parquet BR00127146.parquet BR00127147.parquet BR00127148.parquet BR00127149.parquet \
           compound_info.csv compound_well_map.csv level6_axiom_selected_features.parquet load_data.csv \
           perturbation_controls.csv toxcast_cellbased_binary.parquet toxcast_cellfree_binary.parquet \
           toxcast_cellfree_info.parquet toxcast_cytotox_binary.parquet toxcast_cytotox_info.parquet \
           v5_oasis_03Sept2024_simple.csv; do
    get "Bioimaging_project/inputs/$f" "data/raw/bioimaging/$f"
  done
  # The bioimaging notebooks read ../../inputs/<file>; link the downloaded data into the local repo copy.
  BI_INPUTS="$BI/local/ewald-lab-training/inputs"
  if [[ -d "$BI_INPUTS" ]]; then
    for f in data/raw/bioimaging/*; do
      [[ -e "$BI_INPUTS/$(basename "$f")" ]] || ln -s "$PWD/$f" "$BI_INPUTS/$(basename "$f")"
    done
    echo "  ✓ linked data/raw/bioimaging/* into $BI_INPUTS"
  fi
fi

if $WITH_2025; then
  # 2025 edition (CC BY 4.0, DOI 10.6019/TOL.DataScience25-t.2025.00001.1). Supplementary, local-only.
  # Skipped: participants' flash-talk decks (student work), .pptx duplicates of PDFs, R cache files.
  echo "==> 2025 edition (supplementary, git-ignored)"
  E25="supplementary/2025_edition/local"
  while IFS= read -r f; do
    [[ -z "$f" ]] && continue
    get2025 "$(python3 -I -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1]))' "$f")" "$E25/$f"
  done <<'LIST'
Day1/Introduction Course.pptx
Day1/EMBLEBIdataresources_DAT25.pdf
Day1/2025-06-12_Data_management_and_FAIR.pdf
Day1/Graphic design principles for data vis.pdf
Day1/Python practicals/getting_started_with_python.ipynb
Day1/Python practicals/data_handling_with_python.ipynb
Day1/Python practicals/data_visualisation_with_python.ipynb
Day1/Python practicals/data/food.csv
Day1/Python practicals/data/food_tiny.csv
Day1/Python practicals/data/weekly_fruit_consumption.csv
Day2/stats/Statistics_lecture.pdf
Day2/stats/Copy of Copy of 2025-06-17-Statistics-in-python.ipynb
Day2/stats/mice.csv
Day2/stats/mice_dataset.csv
Day3/Machine learning - morning/Introduction_to_ML.pdf
Day3/Machine learning - morning/ML_practical.pdf
Day3/Machine learning - morning/Copy of Introduction_to_ML.ipynb
Day3/ML_for_Biology_Session.pdf
Day3/Gene expression/EBI_DataScience_course_06_09_2025.pdf
Day3/Protein structure group project/Data-science-for-life scientists_ Interpreting functional information from large scale protein structure data.pdf
Day4/Programmatic_Access_Data_Science.pdf
Day4/Copy of Copy of Programmatic Access Data Science.ipynb
Day4/Copy of Copy of Blast Workflow-2025.ipynb
Day4/Data Ethics & Responsible Data Governance.pdf
Day4/Lannelongue_GreenAlgorithms_2025-06_EBI.pdf
Day5/Wrap up session DAT25 - to share.pptx
Day5/Cytoscape/Intro_network_Analysis_theory_KP.pdf
Day5/Cytoscape/networkanalysis_practicals_kp.pdf
Day5/Cytoscape/Pratical materials.zip
LIST
  # Session Colab notebooks linked from the 2025 pages
  drive_nb 1AqeqAP-m_244aeeeodokyhcVeDyfRtLy "$E25/colab/getting_started_with_python.ipynb"
  drive_nb 15YlnWdAee-PTWIvM9x-qb770zE22mDZz "$E25/colab/data_visualisation_with_python.ipynb"
  drive_nb 1DxmbXh7l-n4wTu5g4yIetREnxQj6DwtA "$E25/colab/statistics_in_python.ipynb"
  drive_nb 1WatcmJ_PHGms5g4ORtP5oVPru4tM3j2Q "$E25/colab/programmatic_access_examples.ipynb"
  drive_nb 1nVzLfalxj_tpvLtBo7eIdOMV3jSWbWha "$E25/colab/programmatic_access_exercises_blast.ipynb"
  drive_nb 1YrK5L2goqzgdNpHINsBGKKn7UeAKvoVi "$E25/colab/ml_practical_iris.ipynb"
  # Repositories used by the 2025 sessions
  clone_snapshot "Functional-Genomics/data_science_2025" "$E25/repos/data_science_2025" false   # no licence file
  clone_snapshot "PDBeurope/pdbe-api-training"          "$E25/repos/pdbe-api-training" false  # Apache-2.0
  # Single-cell project dataset (165 MB AnnData)
  get2025 "Day3/Gene%20expression/project_data.h5ad" "data/raw/2025_gene_expression/project_data.h5ad"
fi

echo "Done."
