'''
Copied liberally from the tool by Zach del Rosario, https://github.com/zdelrosario/jupyter-authoring
Enze Chen, 2023/01/14
'''
import os 
import sys
import nbformat
import re
from copy import deepcopy
from datetime import datetime

def scrub_folder(dirname):
    files = os.listdir(dirname)
    for f in files:
        if f.endswith('_master.ipynb'):

            # Process the master notebook file
            filename_orig = os.path.join(dirname, f)
            filename_blank = filename_orig.replace('master', 'blank')

            # load the notebook
            nb_orig  = nbformat.read(filename_orig, as_version=4)
            nb_blank = deepcopy(nb_orig)
            nb_solu  = deepcopy(nb_orig)

            for cell_id in range(len(nb_orig['cells'])):
                cell_orig = nb_orig['cells'][cell_id]
                text_blank = cell_orig['source']

                # process markdown and code cells
                if (cell_orig['cell_type'] == 'markdown') or (cell_orig['cell_type'] == 'code'):
                    text_blank = re.sub(
                        '<!-- solution-begin -->(\n|.)*?<!-- solution-end -->\n?',
                        '',
                        text_blank
                    )
                    text_blank = re.sub(
                        '# solution-begin(\n|.)*?# solution-end',
                        '',
                        text_blank
                    )

                else:
                    raise ValueError(f'Unrecognized cell type {cell_orig["cell_type"]}.')

                # write the results
                nb_blank['cells'][cell_id]["source"] = text_blank


            # write blank notebook to file
            nbformat.write(nb_blank, filename_blank)
            print(f"{filename_orig.split('/')[-1]} successfully scrubbed! Blank notebook created.")


if __name__ == '__main__':
    print(f'Starting cleaning at {datetime.now()}')
    folders = [f for f in os.listdir('..') if f.startswith('lab')]
    for f in folders:
        scrub_folder(os.path.join('..', f))