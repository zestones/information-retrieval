from models.collection import Collection

from weighting_strategies.bm25_weighting import BM25Weighting
from weighting_strategies.bm25Fr_weighting import BM25FrWeighting
from weighting_strategies.bm25Fw_weighting import BM25FwWeighting

import itertools
import numpy as np

from manager.run_manager.utils.utils import evaluate_run


class BM25GridSearch:
    def __init__(self, collection_file, args):
        self.COLLECTION_FILE = collection_file
        self.args = args
        
    def run_bm25_optimization(self):
        self.bm25_grid_search()
        self.bm25fw_grid_search()
        self.bm25fr_grid_search()

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

            collection.weighting_strategy = BM25Weighting(k1=k1, b=0.75)
            collection.weighted_index = collection.weighting_strategy.calculate_weight(collection)

            evaluate_run(collection, self.args.granularity)

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

            collection.weighting_strategy = BM25Weighting(k1=1.2, b=b)
            collection.weighted_index = collection.weighting_strategy.calculate_weight(collection)

            evaluate_run(collection, self.args.granularity)

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

            collection.weighting_strategy = BM25FwWeighting(k1=1.2, b=0.75, alpha=alpha, beta=beta, gamma=gamma)
            collection.weighted_index = collection.weighting_strategy.calculate_weight(collection)

            evaluate_run(collection, self.args.granularity)

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

            collection.weighting_strategy = BM25FrWeighting(k1=1.2, b=0.75, alpha=alpha, beta=beta, gamma=gamma)
            collection.weighted_index = collection.weighting_strategy.calculate_weight(collection)
