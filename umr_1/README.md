# umr 1.0 processing
 ./run.sh


## Processing Steps

1. **input data**:
   - **english**: received from Julia.
   - **arapaho**: received from Julia .
   - **chinese**: exported from UMR Writer. (export_from_database.py)
   - **navajo**: exported from UMR Writer.
   - **kukama**: exported from UMR Writer.
   - **Jens**: exported from UMR writer. 

2. **Preprocess**: (fix.py)
   - **(a)** Remove all irrelevant information: manual comments containing `#`, manually added random information, UMR writer metadata(info section and ending section).
   - **(b)** automatically fix undefined values due to illegal concepts or alignment bugs and manually checked.
   
3. **Sentence-Level Graph Well-Formedness Checks**: (check_valid_graph.py and function fix_in_json)
   - **(a)** Check for matching parentheses.
   - **(b)** Validate variable formats (e.g., `s1x1`).
   - **(c)** Verify Pennman graph:
      - Ensure valid triples. (detect incomplete annotations)
      - Nodes should be in form of variables/concepts, or constants.
   - **(d)** Roleset checks:
      - Check if the role exists.
      - Confirm capitalization of some roles.
      - Ensure roles are not acronyms.
   - **(e)** De-duplicate triples.
   - **(f)** Check for duplicated variables:
      - For instance, if two nodes in a sentence have an `sn2` variable and neither is a reentrancy, one should be corrected to `sn3`.
   - **(g)** Identify sentences lacking sentence-level graphs. 
   - 
4. **Document-Level Graph Well-Formedness Checks**: (check_valid_graph.py and function fix_in_json.py)
   - **(a)** Verify matching parentheses.
   - **(b)** Check variables:
      - Ensure document-level variables exist in the set of sentence-level variables.
   - **(c)** Triple graph check:
      - Identify incomplete annotations.
   - **(d)** De-duplicate triples.
   - **(e)** Identify sentences lacking document-level graphs.


5. **Alignment Well-Formedness Checks**:
   - **(a)** Check alignment types: (function check_align_format)
      - `s1x1: 1-2` (MWE).
      - `s1x2: 3-4,6-6` (non-contiguous MWE).
      - `s1x3: 1.1-1.2` (subword).
      - Abstract concept alignment: `0-0`.
   - **(b)** Confirm all variables have alignments.
   - **(c)** Verify that no variable in alignment doesn't exists at the sentence level.

6. **Postprocess**:
   - **(a)** Remove modal annotations at the sentence level. (function fix_in_json)

## Steps for Documents Exported from UMR

For documents exported from UMR, apply the following steps:

- Manually fix undefined values due to illegal concepts or alignment bugs.
- Identify sentences lacking document-level graphs.
- De-duplicate triples.
- De-duplicate document-level triples.
- Remove modal annotations at the sentence level.

Notes:
- use (s20u / umr-empty) for empty sentence level graph, use (s20s0 / sentence) for empty doc level graph
- Navajo: In document 'I_flew_over_Navajo_Land', in :: snt57, there are two sentence level graphs for one sentence
- Sanapana: Jens: The texts I used for annotation (and actually almost all the texts I have) are transcriptions of interviews, with one main narrator as well as one or more interlocutors who interviewed them and asked questions. I used AUTH in the modal superstructure to annotate the main narrator as conceiver of a proposition, and I used AUTH2/AUTH3 to annotate other interlocutors in the recording as conceivers. We never made a firm decision while I was on the grant about how to annotate multiple speakers as conceivers in the same text, so this was my temporary solution.
