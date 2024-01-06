# Information Retrieval

This project aim to explore the different techniques of information retrieval. We implemented different probabilistic models and compared them to the vector space model and some machine learning models.

## Getting Started

Here is a guide to help you run the project on your local machine.

### Prerequisites

You need to install the requirements.txt file to run the project. You can use the makefile to do so.

```bash
make install
```

or

```bash
pip install -r requirements.txt
```

### Running the project

To run the project, you can either use the makefile or run the main file.

Here is the options you can use:

| Option                     | Description                                     |
|----------------------------|-------------------------------------------------|
| -h, --help                 | Show the help message and exit                  |
| -e, --export-inverted-index| Export collection                               |
| -i, --import-inverted-index| Import collection                               |
| -s, --statistics           | Export statistics                               |
| --ltn                       | Use LTN weighting scheme                         |
| --ltc                       | Use LTC weighting scheme, length normalization and cosine similarity |
| --lnu                       | Use LNU weighting scheme                         |
| --bm25                      | Use BM25 weighting scheme                        |
| --bm25fw                    | Use BM25Fw weighting scheme                      |
| --bm25fr                    | Use BM25Fr weighting scheme                      |
| --cos-sim                   | Use cosine similarity for evaluation             |
| -o, --bm25_optimization     | Run BM25 parameter optimization experiment       |
| -g, --granularity GRANULARITY | Granularity of the XPath query                  |
| --baseline                  | Run baseline                                    |
| --export-weighted-idx       | Export weighted index to JSON file               |
| --query-file QUERY_FILE     | File containing queries                          |


#### Examples

Here is some examples of how to run the project.

```bash
make practice5v5 -- --bm25 -g "'.//article'" "'.//title'"

make practice5v5 -- --baseline
```