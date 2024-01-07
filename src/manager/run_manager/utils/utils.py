import os
from manager.query_manager import QueryManager

RUN_OUTPUT_FOLDER = "../docs/resources/runs/"
if not os.path.exists(RUN_OUTPUT_FOLDER):
    os.makedirs(RUN_OUTPUT_FOLDER)


def _construct_run_name(run_id, weighting_scheme, granularity=None, text_processor=None, parameters=None):
    if granularity:
        granularity_str = '_'.join(granularity).replace('.//', '')
        base_filename = f"../docs/resources/runs/BengezzouIdrissMezianeGhilas_{run_id}_{weighting_scheme}_{granularity_str}_{text_processor}"
    else:
        base_filename = f"../docs/resources/runs/BengezzouIdrissMezianeGhilas_{run_id}_{weighting_scheme}_article_{text_processor}"

    if parameters:
        for key, value in parameters.items():
            base_filename += f"_{key}{value}"

    return f"{base_filename}.txt"


def _write_results(query_results, run_file_path):
    with open(run_file_path, 'a') as output_file:
        for result in query_results:
            output_file.write(
                f"{result[0]} {result[1]} {result[2]} {result[3]} {result[4]} {result[5]} {result[6]}\n")


def _get_run_id(folder_path=RUN_OUTPUT_FOLDER):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return len(files) + 1


def evaluate_run(collection, granularity):
    """
    Runs the baseline. The baseline generates 12 runs : 3 (weighting schemes) * 2 (stop-list) * 2 (stemmer)
    """
    run_id = _get_run_id(RUN_OUTPUT_FOLDER)
    scheme = collection.weighting_strategy.get_weighting_scheme_name()
    parameters = collection.weighting_strategy.get_weighting_scheme_parameters()
    # text_processor = "_".join(collection.label.split("_")[1:])
    text_processor = collection.text_processor.get_text_processor_name()

    run_file_path = _construct_run_name(run_id, scheme, granularity=granularity, text_processor=text_processor, parameters=parameters)
    query_manager = QueryManager(collection)

    parsed_queries = query_manager.parse_query_file()

    for query_id, query in parsed_queries:
        query_results = query_manager.launch_query(query_id, query)
        _write_results(query_results, run_file_path)
