# Stability Audit

This repository contains code used to audit the stability of personality predictions made by two algorithmic hiring systems, Humantic AI and Crystal. This codebase supports the 2021 manuscript entitled "External Stability Auditing to Test the Validity of Personality Prediction in AI Hiring," authored by Alene K. Rhea, Kelsey Markey, Lauren D'Arinzo, Hilke Schellmann, Mona Sloane, Paul Squires, and Julia Stoyanovich. 

## Code
The Jupyter notebook `analysis.ipynb` reads in the survey and system output data, and performs all stability analysis. The notebook begins with a demographic summarization, and then estimates stability metrics for each facet experiment as described in the manuscript. 

Spearman's rank correlation is used to measure rank-order stability, two-tailed Wilcoxon signed rank testing is used to measure locational stability, and normalized L1 distance is used to measure total change across each facet. Medians of each facet treatment are estimated as well. Results are saved to the `results` directory, organized by metric and by system (Humantic AI and Crystal). Subgroup analysis is performed for rank-order stability and total change. Highlighting is employed to indicate correlations below 0.95 and 0.90, and Wilcoxon p-values below the Bonferroni and Benjamini-Hochberg corrected thresholds. Scatterplots are produced to compare the outputs from each pair of facet treatments. Boxplots illustrate total change. Boxplots comparing relevant subgroup analysis for each facet are produced as well.


## Data

### Survey
Anonymized survey results are saved in `data/survey.csv`. Columns described in the table below.
| Column | Type | Description | Values |
| :-----: | :----: | :------------------------: | :------------------------: |
| Participant_ID | str | Unique ID used to identify participant. | "ID2" - "ID101" (missing IDs indicate potential subjects were screened out of participation) |
| gender | str | Participant gender, as reported in the survey. Pre-processed to mask rare responses in order to preserve anonymity. | ["Male"  "Female"  "Other Gender"] |
| race | str | Participant race, as reported in the survey. Pre-processed to mask rare responses in order to preserve anonymity. Empty entries indicates participants declined to self-identify their race in the survey. | ["Asian"  "White"  "Other Race"  NaN] |
| birth_country | str | Participant birth country, as reported in the survey. Pre-processed to mask rare responses in order to preserve anonymity. Empty entries indicates participants declined to provide their birth country in the survey. | ["China"  "India"  "USA"  "Other Country"  NaN] |
| primary_language | str | Primary language of participant, as reported in the survey. | ["English"  "Other Langauge"] |
| resume | bool | Boolean flag indicating whether participant provided a resume in the survey. | ["True"  "False"] |
| linkedin | bool | Boolean flag indicating whether participant provided a LinkedIn in the survey. | ["True"  "False"] |
| twitter | bool | Boolean flag indicating whether participant provided a public Twitter handle in the survey. | ["True"  "False"] |
| linkedin_in_orig_resume | bool | Boolean flag indicating whether participant included a reference to their LinkedIn in the resume they submitted. Empty entries indicate participants did not submit a resume. | ["True"  "False"  NaN] |
| orig_embed_type | str | Description of the method by which the participant referenced their LinkedIn in their submitted resume. Empty entries indicate participant did not submit a resume containing a reference to LinkedIn. | ["True"  "False"  NaN] |
| orig_file_type | str | Filetype of the resume submitted by the participant. Empty entries indicate participants did not submit a resume. | ["pdf"  "docx"  "txt"  NaN] |


### Humantic AI and Crystal Output
Output from Humantic AI and Crystal is saved in the `data` directory. Each run is saved as a CSV and is named with its Run ID. Tables 3 and 4 in the manuscript (reproduced below) provide details of each run.  Each file contains one row for each submitted input.  `Participant_ID` provides a unique key, and `output_success` is a Boolean flag indicating that the system successfully produced output from the given input. Wherever `output_success` is true, there will be numeric predictions for each trait. Crystal results contain predictions for DiSC traits, and Humantic AI results contain predictions for DiSC traits and Big Five traits.

| Run ID | System | Description | Run Dates |
| :-----: | :--------: | :-------------------: | :--------: |
| HRo1 | Humantic AI | Original Resume | 11/23/2020 - 01/14/2021 |
| HRi1 | Humantic AI | De-Identified Resume | 03/20/2021 - 03/28/2021 |
| HRi2 | Humantic AI | De-Identified Resume | 04/20/2021 - 04/28/2021 |
| HRi3 | Humantic AI | De-Identified Resume | 04/20/2021 - 04/28/2021 |
| HRd1 | Humantic AI | DOCX Resume | 03/20/2021 - 03/28/2021 |
| HRu1 | Humantic AI | URL-Embedded Resume | 04/09/2021 - 04/11/2021 |
| HL1 | Humantic AI | LinkedIn | 11/23/2020 - 01/14/2021 |
| HL2 | Humantic AI | LinkedIn | 08/10/2021 - 08/11/2021 |
| HT1 | Humantic AI | Twitter | 11/23/2020 - 01/14/2021 |
| HT2 | Humantic AI | Twitter | 08/10/2021 - 08/11/2021 |
| CRr1 | Crystal | Raw Text Resume | 03/31/2021 - 04/02/2021 |
| CRr2 | Crystal | Raw Text Resume | 05/01/2021 - 05/03/2021 |
| CRr3 | Crystal | Raw Text Resume | 05/01/2021 - 05/03/2021 |
| CRp1 | Crystal | PDF Resume | 11/23/2020 - 01/14/2021 |
| CL1 | Crystal | LinkedIn | 11/23/2020 - 01/14/2021 |
| CL2 | Crystal | LinkedIn | 09/13/2020 - 09/16/2021 |

