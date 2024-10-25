import json
import os
import pytest
import nbformat
from pathlib import Path

SOLUTIONS_DIR = 'answers/'
NOTEBOOK_NAME = 'p4.ipynb'

weights = [0.5, 0.6, 0.6, 0.6, 0.6, 
          0.6, 0.7, 0.6, 0.6, 0.6]

# Track total score
test_scores = {}
max_score = sum(weights)

def get_code_cells(notebook):
    """Extract all code cells from the Jupyter notebook."""
    return [cell['source'] for cell in notebook.cells if cell['cell_type'] == 'code']


@pytest.fixture
def load_notebook():
    """Load the Jupyter notebook and return the code cells."""
    with open(NOTEBOOK_NAME, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)
    return get_code_cells(notebook)


def test_wget_unzip_usage(load_notebook):
    """Check that wget and unzip were used to download and extract the sample_mflix dataset."""
    notebook_code = "\n".join(load_notebook)
    assert "!wget" in notebook_code, "wget command to download datasets not found."
    assert "!unzip" in notebook_code, "unzip command to extract the dataset not found."


def test_imports(load_notebook):
    """Check that the required modules are imported."""
    notebook_code = "\n".join(load_notebook)
    required_imports = [ 
        "os",
        "json", 
        "elasticsearch",
    ]
    for imp in required_imports:
        assert imp in notebook_code, f"Required import '{imp}' not found."


def load_json(file):
    with open(file, 'r') as f:
        return json.load(f)


@pytest.mark.parametrize("question", [1])
def test_client_info(question):
    try:
        student_answer = load_json(f"{SOLUTIONS_DIR}/q{question}.json")
    except Exception as e:
        assert False, f"Question {question} json not found at {SOLUTIONS_DIR}/q{question}.json"
    check_keys = ["name", "cluster_name", "cluster_uuid", "version", "tagline"]
    check_elastic_version_number = ["8.15.2", "8.15.3"]
    assert student_answer is not None, f"Question {question}: No solution found."
    for key in check_keys:
        assert key in student_answer, f"Question {question}: '{key}' key not found."
    # print(student_answer["version"]["number"], check_elastic_version_number)
    assert student_answer["version"]["number"] in check_elastic_version_number, f"Question {question}: Elastic version number mismatch. We are using 8.15.2/3!"
    test_scores[question] = weights[question - 1]


@pytest.mark.parametrize("question", [2,3])
def test_mappings(question):
    try:
        student_answer = load_json(f"{SOLUTIONS_DIR}/q{question}.json")
    except Exception as e:
        assert False, f"Question {question} json not found at {SOLUTIONS_DIR}/q{question}.json"
    assert student_answer is not None, f"Question {question}: No solution found."
    assert "madmap" in student_answer, f"Question {question}: 'madmap' key not found."
    assert "mappings" in student_answer["madmap"], f"Question {question}: 'mappings' key not found in student_answer['madmap']"
    assert "properties" in student_answer["madmap"]["mappings"], f"Question {question}: 'properties' key not found in student_answer['madmap']['mappings']"
    if question == 2:
        entries_to_match = ["arrests", "articles", "places"]
    elif question == 3:
        entries_to_match = ["arrests", "articles", "places", "wiki"]

    for entry in entries_to_match:
        assert entry in student_answer["madmap"]["mappings"]["properties"], f"Question {question}: '{entry}' key not found in student_answer['madmap']['mappings']['properties']"
    test_scores[question] = weights[question - 1]


@pytest.mark.parametrize("question", [4])
def test_q4(question):
    try:
        student_answer = load_json(f"{SOLUTIONS_DIR}/q{question}.json")
    except Exception as e:
        assert False, f"Question {question} json not found at {SOLUTIONS_DIR}/q{question}.json"
    assert student_answer is not None, f"Question {question}: No solution found."
    q4_threshold = 6.0
    assert "hits" in student_answer, f"Question {question}: 'hits' key not found."
    assert "max_score" in student_answer["hits"], f"Question {question}: 'max_score' key not found in student_answer['hits']"
    student_answer = student_answer["hits"]["max_score"]
    assert student_answer >= q4_threshold, f"Question {question}: Max score achieved is less than 6."
    test_scores[question] = weights[question - 1]


@pytest.mark.parametrize("question", [5])
def test_q5(question):
    try:
        student_answer = load_json(f"{SOLUTIONS_DIR}/q{question}.json")
    except Exception as e:
        assert False, f"Question 5 json not found at {SOLUTIONS_DIR}/q5.json"
    assert student_answer is not None, f"Question 5: No solution found."
    assert "wiki" in student_answer, f"Question 5: 'wiki' key not found."
    expected = {
    "wiki": [
        "Rivalries\nThe Wisconsin Badgers' most notable <em>rivalry</em> within the Big Ten is with the Minnesota Golden",
        "Gophers, which is the most-played <em>rivalry</em> in Division I-A football.",
        "The I-94 <em>rivalry</em> between Wisconsin men's basketball and the in-state Marquette Golden Eagles has been"
    ]}
    assert expected["wiki"] in student_answer["wiki"], f"Question 5: Expected answer not found."
    test_scores[question] = weights[question - 1]


@pytest.mark.parametrize("question", [6])
def test_q6(question):
    try:
        student_answer = load_json(f"{SOLUTIONS_DIR}/q{question}.json")
    except Exception as e:
        assert False, f"Question 6 json not found at {SOLUTIONS_DIR}/q6.json"
    assert student_answer is not None, f"Question 6: No solution found."
    assert "hits" in student_answer, f"Question 6: 'hits' key not found."
    assert "hits" in student_answer["hits"], f"Question 6: 'hits' key not found in student_answer['hits']"
    assert "highlight" in student_answer["hits"]["hits"][0], f"Question 6: 'highlight' key not found in student_answer['hits']['hits'][0]"
    assert "_source" in student_answer["hits"]["hits"][0], f"Question 6: '_source' key not found in student_answer['hits']['hits'][0]"
    for dic in student_answer["hits"]["hits"][0]["_source"]["articles"]:
        these_keys = dic.keys()
        if "geoLocation" in these_keys and "title" in these_keys and "WhenIsItHappening" in these_keys:
            if "Coldplay concert at Camp Randall Stadium" in dic["title"]:
                assert True, "Q6 test passed"
                test_scores[question] = weights[question - 1]
                return
    assert False, "testing"


@pytest.mark.parametrize("question", [7])
def test_q7(question):
    try:
        student_answer = load_json(f"{SOLUTIONS_DIR}/q{question}.json")
    except Exception as e:
        assert False, f"Question {question} json not found at {SOLUTIONS_DIR}/q{question}.json"
    assert student_answer is not None, f"Question {question}: No solution found."
    solution_q7 = 1671
    assert "total_arrests_sum" in student_answer, f"Question {question}: 'total_arrests_sum' key not found."
    assert "value" in student_answer["total_arrests_sum"], f"Question {question}: 'value' key not found in student_answer['total_arrests_sum']"
    student_answer = int(student_answer["total_arrests_sum"]["value"])
    assert student_answer == solution_q7, f"Question {question}: Value match failed."
    test_scores[question] = weights[question - 1]


@pytest.mark.parametrize("question", [9])
def test_q9(question):
    try:
        student_answer = load_json(f"{SOLUTIONS_DIR}/q{question}.json")
    except Exception as e:
        assert False, f"Question {question} json not found at {SOLUTIONS_DIR}/q{question}.json"
    assert student_answer is not None, f"Question {question}: No solution found."
    # Check keys first
    assert "coordinates" in student_answer, f"Question {question}: 'coordinates' key not found."
    assert "formattedAddress" in student_answer, f"Question {question}: 'formattedAddress' key not found."
    assert "name" in student_answer, f"Question {question}: 'name' key not found in student_answer"
    assert "place_id" in student_answer, f"Question {question}: 'place_id' key not found in student_answer"
    assert "place_type" in student_answer, f"Question {question}: 'place_type' key not found in student_answer"
    assert "priceLevel" in student_answer, f"Question {question}: 'priceLevel' key not found in student_answer"
    # Check types & vals
    assert student_answer["coordinates"][0]["type"] == "Point", f"Question {question}: 'Point' type not found in student_answer['coordinates']"
    assert student_answer["formattedAddress"][0] == "1 S Pinckney St, Madison, WI 53703, USA", f"Question {question}: address didn't match the address reported in student_answer['formattedAddress']"
    assert student_answer["name"][0] == "L'Etoile Restaurant", f"Question {question}: name didn't match the name reported in student_answer['name'] (Respect the French!)"
    assert student_answer["place_id"][0] == "ChIJvw6XEsNTBogRN99XXAXk-pI", f"Question {question}: place_id didn't match the place_id reported in student_answer['place_id']"
    assert student_answer["place_type"][0] == "restaurants", f"Question {question}: place_type didn't match the place_type reported in student_answer['place_type']"
    assert student_answer["priceLevel"][0] == "PRICE_LEVEL_VERY_EXPENSIVE", f"Question {question}: priceLevel didn't match the priceLevel reported in student_answer['priceLevel'] (Only the most expensive and the best!)"
    test_scores[question] = weights[question - 1]


@pytest.mark.parametrize("question",  [8,10])
def test_imgs_exist(question):
    if os.path.exists(f"{SOLUTIONS_DIR}/q{question}.png"):
        assert True, f"Question {question}: Image found."
        test_scores[question] = weights[question - 1]
    else:
        assert False, f"Question {question}: Image not found."
