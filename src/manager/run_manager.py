from models.collection import Collection
from manager.query_manager import QueryManager

from manager.text_processor import CustomTextProcessorNoStopNoStem
from manager.text_processor import CustomTextProcessorNoStem
from manager.text_processor import CustomTextProcessorNoStop

from weighting_strategies.bm25_weighting import BM25Weighting
from weighting_strategies.bm25Fr_weighting import BM25FrWeighting
from weighting_strategies.bm25Fw_weighting import BM25FwWeighting

import itertools
import numpy as np
import os


class RunManager:
    def __init__(self, args):
        self.RUN_OUTPUT_FOLDER = "../docs/resources/runs/"
        if not os.path.exists(self.RUN_OUTPUT_FOLDER):
            os.makedirs(self.RUN_OUTPUT_FOLDER)

        # XML-Coll-withSem
        self.COLLECTION_FILE = '../lib/data/practice_05/small.zip'
        self.args = args

    def run(self):
        if self.args.baseline:
            self.run_baseline()
        elif self.args.bm25_optimization:
            self.run_bm25_optimization()
        else:
            self.run_custom()

    def construct_run_name(self, run_id, weighting_scheme, k1=None, b=None, granularity=None, text_processor=None, alpha=None, beta=None, gamma=None):
        print("granularity", granularity)
        if granularity:
            granularity_str = '_'.join(granularity).replace('.//', '')
            base_filename = f"../docs/resources/runs/BengezzouIdrissMezianeGhilas_{run_id}_{weighting_scheme}_{granularity_str}_{text_processor}"
        else:
            base_filename = f"../docs/resources/runs/BengezzouIdrissMezianeGhilas_{run_id}_{weighting_scheme}_article_{text_processor}"

        if k1 is not None and b is not None:
            base_filename = f"{base_filename}_k{k1}_b{b}"
        if alpha is not None and beta is not None and gamma is not None:
            base_filename = f"{base_filename}_alpha{alpha}_beta{beta}_gamma{gamma}.txt"
        else:
            base_filename = f"{base_filename}.txt"

        return base_filename

    def write_results(self, query_results, run_file_path):
        with open(run_file_path, 'a') as output_file:
            for result in query_results:
                output_file.write(
                    f"{result[0]} {result[1]} {result[2]} {result[3]} {result[4]} {result[5]} {result[6]}\n")

    def get_run_id(self, folder_path):
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        return len(files) + 1

    def get_weighting_scheme(self, ltn=False, ltc=False, bm25=False, bm25fr=False, bm25fw=False):
        if ltn:
            return "ltn"
        elif ltc:
            return "ltc"
        elif bm25:
            return "bm25"
        elif bm25fw:
            return "bm25fw"
        elif bm25fr:
            return "bm25fr"
        else:
            raise ValueError("No weighting scheme selected")

    def evaluate_baseline(self, collection, ltn=False, ltc=False, bm25=False, bm25fr=False, bm25fw=False, k1=None, b=None, text_processor="None"):
        """
        Runs the baseline. The baseline generates 12 runs : 3 (weighting schemes) * 2 (stop-list) * 2 (stemmer)
        """
        run_id = self.get_run_id(self.RUN_OUTPUT_FOLDER)

        scheme = self.get_weighting_scheme(ltn, ltc, bm25, bm25fr, bm25fw)
        run_file_path = self.construct_run_name(
            run_id, scheme, granularity=self.args.granularity, k1=k1, b=b, text_processor=text_processor)
        query_manager = QueryManager(collection)

        parsed_queries = query_manager.parse_query_file(self.args.query_file)

        for query_id, query in parsed_queries:
            query_results = query_manager.launch_query(query_id, query)
            self.write_results(query_results, run_file_path)

    def run_baseline_with_stop_and_stem(self):
        collection = Collection(self.COLLECTION_FILE,
                                plot_statistics=self.args.plot,
                                import_collection=False,
                                export_collection=True,
                                export_statistics=self.args.statistics,
                                ltn_weighting=True,
                                ltc_weighting=False,
                                bm25_weighting=False,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity
                                )
        self.evaluate_baseline(collection, ltn=True, text_processor="stop671_porter")

        collection = Collection(self.COLLECTION_FILE,
                                plot_statistics=self.args.plot,
                                import_collection=True,
                                export_collection=False,
                                export_statistics=self.args.statistics,
                                ltn_weighting=False,
                                ltc_weighting=True,
                                bm25_weighting=False,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity
                                )
        self.evaluate_baseline(collection, ltc=True, text_processor="stop671_porter")

        collection = Collection(self.COLLECTION_FILE,
                                plot_statistics=self.args.plot,
                                import_collection=True,
                                export_collection=False,
                                export_statistics=self.args.statistics,
                                ltn_weighting=False,
                                ltc_weighting=False,
                                bm25_weighting=True,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity
                                )
        self.evaluate_baseline(collection, bm25=True, k1=1, b=0.5, text_processor="stop671_porter")

    def run_baseline_with_stop_and_no_stem(self):
        collection = Collection(self.COLLECTION_FILE,
                                plot_statistics=self.args.plot,
                                import_collection=False,
                                export_collection=True,
                                export_statistics=self.args.statistics,
                                ltn_weighting=True,
                                ltc_weighting=False,
                                bm25_weighting=False,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity,
                                text_processor=CustomTextProcessorNoStem()
                                )
        self.evaluate_baseline(collection, ltn=True, text_processor="stop671_nostem")

        collection = Collection(self.COLLECTION_FILE,
                                plot_statistics=self.args.plot,
                                import_collection=True,
                                export_collection=False,
                                export_statistics=self.args.statistics,
                                ltn_weighting=False,
                                ltc_weighting=True,
                                bm25_weighting=False,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity
                                )
        self.evaluate_baseline(collection, ltc=True, text_processor="stop671_nostem")

        collection = Collection(self.COLLECTION_FILE,
                                plot_statistics=self.args.plot,
                                import_collection=True,
                                export_collection=False,
                                export_statistics=self.args.statistics,
                                ltn_weighting=False,
                                ltc_weighting=False,
                                bm25_weighting=True,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity
                                )
        self.evaluate_baseline(collection, bm25=True, k1=1, b=0.5, text_processor="stop671_nostem")

    def run_baseline_with_no_stop_and_stem(self):
        collection = Collection(self.COLLECTION_FILE,
                                plot_statistics=self.args.plot,
                                import_collection=False,
                                export_collection=True,
                                export_statistics=self.args.statistics,
                                ltn_weighting=True,
                                ltc_weighting=False,
                                bm25_weighting=False,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity,
                                text_processor=CustomTextProcessorNoStop()
                                )
        self.evaluate_baseline(collection, True, False, False, text_processor="nostop_porter")

        collection = Collection(self.COLLECTION_FILE,
                                plot_statistics=self.args.plot,
                                import_collection=True,
                                export_collection=False,
                                export_statistics=self.args.statistics,
                                ltn_weighting=False,
                                ltc_weighting=True,
                                bm25_weighting=False,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity
                                )
        self.evaluate_baseline(collection, False, True, False, text_processor="nostop_porter")

        collection = Collection(self.COLLECTION_FILE,
                                plot_statistics=self.args.plot,
                                import_collection=True,
                                export_collection=False,
                                export_statistics=self.args.statistics,
                                ltn_weighting=False,
                                ltc_weighting=False,
                                bm25_weighting=True,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity
                                )
        self.evaluate_baseline(collection, bm25=True, k1=1, b=0.5, text_processor="nostop_porter")

    def run_baseline_with_no_stop_and_no_stem(self):
        collection = Collection(self.COLLECTION_FILE,
                                plot_statistics=self.args.plot,
                                import_collection=False,
                                export_collection=True,
                                export_statistics=self.args.statistics,
                                ltn_weighting=True,
                                ltc_weighting=False,
                                bm25_weighting=False,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity,
                                text_processor=CustomTextProcessorNoStopNoStem()
                                )
        self.evaluate_baseline(collection, ltn=True, text_processor="nostop_nostem")

        collection = Collection(self.COLLECTION_FILE,
                                plot_statistics=self.args.plot,
                                import_collection=True,
                                export_collection=False,
                                export_statistics=self.args.statistics,
                                ltn_weighting=False,
                                ltc_weighting=True,
                                bm25_weighting=False,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity
                                )
        self.evaluate_baseline(collection, ltc=True, text_processor="nostop_nostem")

        collection = Collection(self.COLLECTION_FILE,
                                plot_statistics=self.args.plot,
                                import_collection=True,
                                export_collection=False,
                                export_statistics=self.args.statistics,
                                ltn_weighting=False,
                                ltc_weighting=False,
                                bm25_weighting=True,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity
                                )
        self.evaluate_baseline(collection, bm25=True, k1=1, b=0.5, text_processor="nostop_nostem")

    def run_baseline(self):
        """
        Runs the baseline. The baseline generates 12 runs : 3 (weighting schemes) * 2 (stop-list) * 2 (stemmer)
        """
        self.run_baseline_with_stop_and_stem()
        self.run_baseline_with_stop_and_no_stem()
        self.run_baseline_with_no_stop_and_stem()
        self.run_baseline_with_no_stop_and_no_stem()

    def run_custom(self):
        collection = Collection(self.COLLECTION_FILE,
                                plot_statistics=self.args.plot,
                                import_collection=self.args.import_inverted_index,
                                export_collection=self.args.export_inverted_index,
                                export_statistics=self.args.statistics,
                                ltn_weighting=self.args.ltn,
                                ltc_weighting=self.args.ltc,
                                bm25_weighting=self.args.bm25,
                                bm25fw_weighting=self.args.bm25fw,
                                bm25fr_weighting=self.args.bm25fr,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=(
                                    [".//bdy", ".//title", ".//categories"] if (self.args.bm25fw or self.args.bm25fr) else self.args.granularity),
                                )

        run_id = self.get_run_id(self.RUN_OUTPUT_FOLDER)

        scheme = self.get_weighting_scheme(self.args.ltn,
                                           self.args.ltc,
                                           self.args.bm25,
                                           self.args.bm25fr,
                                           self.args.bm25fw)
        if self.args.bm25:
            run_file_path = self.construct_run_name(
                run_id, scheme, k1=1, b=0.5, granularity=self.args.granularity, text_processor="stop671_porter")

        elif self.args.bm25fw:
            run_file_path = self.construct_run_name(
                run_id, scheme, k1=1, b=0.5, granularity=self.args.granularity, text_processor="stop671_porter", alpha=3, beta=1, gamma=2)

        elif self.args.bm25fr:
            run_file_path = self.construct_run_name(
                run_id, scheme, k1=1, b=0.5, granularity=self.args.granularity, text_processor="stop671_porter", alpha=3, beta=1, gamma=2)

        else:
            run_file_path = self.construct_run_name(
                run_id, scheme, granularity=self.args.granularity, text_processor="stop671_porter")

        query_manager = QueryManager(collection)
        parsed_queries = query_manager.parse_query_file(self.args.query_file)

        for query_id, query in parsed_queries:
            query_results = query_manager.launch_query(query_id, query)
            self.write_results(query_results, run_file_path)

    def bm25_grid_search(self):
        """
        Runs the baseline. The baseline generates 12 runs : 3 (weighting schemes) * 2 (stop-list) * 2 (stemmer)
        """
        import_collection = False
        exort_collection = True

        for k1 in np.arange(0, 4.2, 0.2):
            k1 = round(k1, 2)
            collection = Collection(self.COLLECTION_FILE,
                                    plot_statistics=self.args.plot,
                                    import_collection=import_collection,
                                    export_collection=exort_collection,
                                    export_statistics=self.args.statistics,
                                    ltn_weighting=False,
                                    ltc_weighting=False,
                                    bm25_weighting=True,
                                    export_weighted_idx=self.args.export_weighted_idx,
                                    parser_granularity=[".//article"]
                                    )
            import_collection = True
            exort_collection = False

            query_manager = QueryManager(collection)
            parsed_queries = query_manager.parse_query_file(self.args.query_file)

            collection.weighted_index = BM25Weighting(k1=k1, b=0.75).calculate_weight(collection)

            run_id = self.get_run_id(self.RUN_OUTPUT_FOLDER)
            scheme = self.get_weighting_scheme(bm25=True)
            run_file_path = self.construct_run_name(
                run_id, scheme, granularity=self.args.granularity, text_processor="stop671_porter", k1=k1, b=0.75)

            query_manager = QueryManager(collection)
            parsed_queries = query_manager.parse_query_file(self.args.query_file)

            for query_id, query in parsed_queries:
                query_results = query_manager.launch_query(query_id, query)
                self.write_results(query_results, run_file_path)

        for b in np.arange(0, 1.1, 0.1):
            b = round(b, 2)
            collection = Collection(self.COLLECTION_FILE,
                                    plot_statistics=self.args.plot,
                                    import_collection=import_collection,
                                    export_collection=exort_collection,
                                    export_statistics=self.args.statistics,
                                    ltn_weighting=False,
                                    ltc_weighting=False,
                                    bm25_weighting=True,
                                    export_weighted_idx=self.args.export_weighted_idx,
                                    parser_granularity=[".//article"]
                                    )
            import_collection = True
            exort_collection = False

            query_manager = QueryManager(collection)
            parsed_queries = query_manager.parse_query_file(self.args.query_file)

            collection.weighted_index = BM25Weighting(k1=1.2, b=b).calculate_weight(collection)

            run_id = self.get_run_id(self.RUN_OUTPUT_FOLDER)
            scheme = self.get_weighting_scheme(bm25=True)
            run_file_path = self.construct_run_name(
                run_id, scheme, granularity=self.args.granularity, text_processor="stop671_porter", k1=1.2, b=b)

            query_manager = QueryManager(collection)
            parsed_queries = query_manager.parse_query_file(self.args.query_file)

            for query_id, query in parsed_queries:
                query_results = query_manager.launch_query(query_id, query)
                self.write_results(query_results, run_file_path)

    def bm25fw_grid_search(self):
        """
        We want to find the best values for alpha, beta and gamma.
        BM25F variant: optimizing bi for each field [Zaragoza04]:
        - Optimizing k1 and bi for each field (K optimizations 2 Dim).
        - With these b(i) and alpha(i) = 1: optimizing k1 (1 optimization 1 Dim).
        - With these b(i) and k1 : optimizing alpha(i) (1 optimization (K-1) Dim).
        alpha(i) refers to the different fields (title, abstract, body), so alpha, beta and gamma values
        """
        # Loop for optimizing k1 with fixed b(i) and alpha(i) = 1
        import_collection = False
        exort_collection = True

        # Loop for optimizing alpha(i) with fixed b=0.75 and k1=1.2
        alphas = np.arange(1, 4)
        betas = np.arange(1, 4)
        gammas = np.arange(1, 4)

        combinations = itertools.product(alphas, betas, gammas)
        for alpha, beta, gamma in combinations:
            alpha = round(alpha, 2)
            beta = round(beta, 2)
            gamma = round(gamma, 2)

            collection = Collection(self.COLLECTION_FILE,
                                    plot_statistics=self.args.plot,
                                    import_collection=import_collection,
                                    export_collection=exort_collection,
                                    export_statistics=self.args.statistics,
                                    ltn_weighting=False,
                                    ltc_weighting=False,
                                    bm25fw_weighting=True,
                                    export_weighted_idx=self.args.export_weighted_idx,
                                    parser_granularity=[".//bdy", ".//title", ".//categories"]
                                    )

            import_collection = True
            exort_collection = False

            query_manager = QueryManager(collection)
            parsed_queries = query_manager.parse_query_file(self.args.query_file)

            collection.weighted_index = BM25FwWeighting(
                k1=1.2, b=0.75, alpha=alpha, beta=beta, gamma=gamma).calculate_weight(collection)

            run_id = self.get_run_id(self.RUN_OUTPUT_FOLDER)
            scheme = self.get_weighting_scheme(bm25fw=True)
            run_file_path = self.construct_run_name(
                run_id, scheme, granularity=self.args.granularity, text_processor="stop671_porter", k1=1.2, b=0.75, alpha=alpha, beta=beta, gamma=gamma)

            query_manager = QueryManager(collection)
            parsed_queries = query_manager.parse_query_file(self.args.query_file)

            for query_id, query in parsed_queries:
                query_results = query_manager.launch_query(query_id, query)
                self.write_results(query_results, run_file_path)

    def bm25fr_grid_search(self):
        """
        We want to find the best values for alpha, beta and gamma.
        BM25F variant: optimizing bi for each field [Zaragoza04]:
        - Optimizing k1 and bi for each field (K optimizations 2 Dim).
        - With these b(i) and alpha(i) = 1: optimizing k1 (1 optimization 1 Dim).
        - With these b(i) and k1 : optimizing alpha(i) (1 optimization (K-1) Dim).
        alpha(i) refers to the different fields (title, abstract, body), so alpha, beta and gamma values
        """
        # Loop for optimizing k1 with fixed b(i) and alpha(i) = 1
        import_collection = False
        exort_collection = True

        # Loop for optimizing alpha(i) with fixed b=0.75 and k1=1.2
        alphas = np.arange(1, 4)
        betas = np.arange(1, 4)
        gammas = np.arange(1, 4)

        combinations = itertools.product(alphas, betas, gammas)
        for alpha, beta, gamma in combinations:
            alpha = round(alpha, 2)
            beta = round(beta, 2)
            gamma = round(gamma, 2)

            collection = Collection(self.COLLECTION_FILE,
                                    plot_statistics=self.args.plot,
                                    import_collection=import_collection,
                                    export_collection=exort_collection,
                                    export_statistics=self.args.statistics,
                                    ltn_weighting=False,
                                    ltc_weighting=False,
                                    bm25fr_weighting=True,
                                    export_weighted_idx=self.args.export_weighted_idx,
                                    parser_granularity=[".//bdy", ".//title", ".//categories"]
                                    )

            import_collection = True
            exort_collection = False

            query_manager = QueryManager(collection)
            parsed_queries = query_manager.parse_query_file(self.args.query_file)

            collection.weighted_index = BM25FrWeighting(
                k1=1.2, b=0.75, alpha=alpha, beta=beta, gamma=gamma).calculate_weight(collection)

            run_id = self.get_run_id(self.RUN_OUTPUT_FOLDER)
            scheme = self.get_weighting_scheme(bm25fr=True)
            run_file_path = self.construct_run_name(
                run_id, scheme, granularity=self.args.granularity, text_processor="stop671_porter", k1=1.2, b=0.75, alpha=alpha, beta=beta, gamma=gamma)

            query_manager = QueryManager(collection)
            parsed_queries = query_manager.parse_query_file(self.args.query_file)

            for query_id, query in parsed_queries:
                query_results = query_manager.launch_query(query_id, query)
                self.write_results(query_results, run_file_path)

    def run_bm25_optimization(self):
        self.bm25_grid_search()
        self.bm25fw_grid_search()
        self.bm25fr_grid_search()
