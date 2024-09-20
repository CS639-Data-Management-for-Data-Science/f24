import nbformat
from nbconvert import PythonExporter
from nbconvert.preprocessors import ExecutePreprocessor
import pandas as pd
import pickle
import argparse
import os
import subprocess

def unzip_and_store(zip_path, temp_dir):
  if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)
  subprocess.run(["unzip", "-o", zip_path, "-d", temp_dir])
  

def parse_pickle(path_to_pickle):
  with open(path_to_pickle, 'rb') as f:
    return pickle.load(f)
  

def grade_notebook(notebook_path):
    with open(notebook_path, 'r') as f:
        notebook = nbformat.read(f, as_version=4)

    with open('test_output.txt', 'w') as out:
      total_score = 0 
      question_tags_seen = []

      for cell in notebook.cells:

        if cell.cell_type == 'code':
          # print(cell.source)
          if "create_engine" in cell.source and ".connect()" in cell.source: 
            out.write("Connection to database established: 2.5 points\n")

          elif "pd.read_sql" in cell.source:
            # Find the comment #qXX in the cell.source
            if cell.source[0] == "#": 
              # print(cell.source)
              question_tag = cell.source.split("#")[1].split("\n")[0]
              # print(f"Found question tag: {question_tag}")
            else:
              out.write(f"[!] Missing question number comment identifier on first line of the cell containing SQL query: {cell.source} \n\n")
              continue

            if question_tag in question_tags_seen: # Make sure no duplicate questions are graded
              continue
            else:
              question_tags_seen.append(question_tag)
              question_number = int(question_tag[1:])
            
            # Grading
            if 'outputs' in cell: # Check whether the notebook has been executed
              try:
                with open(question_tag + ".pkl", 'rb') as ao:
                  actual_output = pickle.load(ao)
              except FileNotFoundError:
                out.write(f"[!] Missing/Incorrect pickle file name for question {question_number}\n")
                
              with open(f"answers/pkls/p{question_number}.pkl", 'rb') as eo:
                expected_output = pickle.load(eo)
              if actual_output.equals(expected_output):
                out.write(f"Question {question_number}: 2.5/2.5 points\n")
                total_score += 2.5
              # if actual_output == expected_output:
              #   out.write(f"Question {question_number}: 2.5 points\n")
              #   total_score += 2.5
            else:
              out.write(f"Question {question_number}: 0 points\n")
            print("Processed", question_tag)
      out.write(f"---------------------------------------------------------------\n Total Score: {total_score}/{2.5 * (35 + 1)}\n---------------------------------------------------------------\n")
      print("-----------------------------")
      print(f"Total Score: {total_score}/{2.5 * (35 + 1)}\n-----------------------------\nDo `cat test_output.txt` for individual question-wise results :)")

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("-nb", "--notebook_path", type=str, default="p2.ipynb")
    args = args.parse_args()

    unzip_and_store("answers.zip", "answers")
    score = grade_notebook(args.notebook_path)