from models.collection import Collection

from weighting_strategies.bm25_weighting import BM25Weighting
from weighting_strategies.bm25Fr_weighting import BM25FrWeighting
from weighting_strategies.bm25Fw_weighting import BM25FwWeighting
from weighting_strategies.lnu_weighting import LNUWeighting

import itertools
import numpy as np
import json

from manager.run_manager.utils.utils import evaluate_run


class ParametersTuning:
    def __init__(self, collection_file, args):
        self.COLLECTION_FILE = collection_file
        self.args = args

    def run_optimization(self):
        self.bm25_grid_search()
        self.bm25fw_grid_search()
        self.bm25fr_grid_search()
        self.lnu_search()

    def lnu_search(self):
        import_collection = False
        export_collection = True

        for slope in np.arange(0.1, 1.2, 0.1):
            slope = round(slope, 2)
            collection = Collection(self.COLLECTION_FILE,
                                    import_collection=import_collection,
                                    export_collection=export_collection,
                                    export_statistics=self.args.statistics,
                                    lnu_weighting=True,
                                    export_weighted_idx=self.args.export_weighted_idx,
                                    is_collection_pre_processed=self.args.pre_processed,
                                    )
            import_collection = True
            export_collection = False

            collection.weighting_strategy = LNUWeighting(slope=slope)
            collection.weighted_index = collection.weighting_strategy.calculate_weight(collection)

            evaluate_run(collection, self.args.granularity, self.args.pre_processed)

    def bm25_grid_search(self):
        """
        Runs the baseline. The baseline generates 12 runs : 3 (weighting schemes) * 2 (stop-list) * 2 (stemmer)
        """
        import_collection = False
        export_collection = True

        for k1 in np.arange(1, 1.6, 0.1):
            k1 = round(k1, 2)
            for b in np.arange(0.5, 0.80, 0.05):
                b = round(b, 2)
                
                collection = Collection(self.COLLECTION_FILE,
                                        import_collection=import_collection,
                                        export_collection=export_collection,
                                        export_statistics=self.args.statistics,
                                        bm25_weighting=True,
                                        export_weighted_idx=self.args.export_weighted_idx,
                                        is_collection_pre_processed=self.args.pre_processed,
                                        )
                import_collection = True
                export_collection = False

                collection.weighting_strategy = BM25Weighting(k1=k1, b=b)
                collection.weighted_index = collection.weighting_strategy.calculate_weight(collection)

                evaluate_run(collection, self.args.granularity, self.args.pre_processed)


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
        export_collection = True

        # Loop for optimizing alpha(i) with fixed b=0.75 and k1=1.2
        alphas = np.arange(1, 2, 0.5)
        betas = np.arange(1, 2, 0.5)
        gammas = np.arange(1, 2, 0.5)

        combinations = itertools.product(alphas, betas, gammas)
        for alpha, beta, gamma in combinations:
            alpha = round(alpha, 2)
            beta = round(beta, 2)
            gamma = round(gamma, 2)
            
            if (alpha == beta == gamma) and (alpha != 1):
                continue

            collection = Collection(self.COLLECTION_FILE,
                                    import_collection=import_collection,
                                    export_collection=export_collection,
                                    export_statistics=self.args.statistics,
                                    bm25fw_weighting=True,
                                    export_weighted_idx=self.args.export_weighted_idx,
                                    is_collection_pre_processed=self.args.pre_processed,
                                    parser_granularity=[".//bdy", ".//title", ".//categories"],
                                    )

            import_collection = True
            export_collection = False

            collection.weighting_strategy = BM25FwWeighting(k1=1.2, b=0.75, alpha=alpha, beta=beta, gamma=gamma)
            collection.weighted_index = collection.weighting_strategy.calculate_weight(collection)

            evaluate_run(collection, self.args.granularity, self.args.pre_processed)

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
        export_collection = True

        # Loop for optimizing alpha(i) with fixed b=0.75 and k1=1.2
        alphas = np.arange(1, 2, 0.5)
        betas = np.arange(1, 2, 0.5)
        gammas = np.arange(1, 2, 0.5)

        combinations = itertools.product(alphas, betas, gammas)
        for alpha, beta, gamma in combinations:
            alpha = round(alpha, 2)
            beta = round(beta, 2)
            gamma = round(gamma, 2)
            
            if (alpha == beta == gamma) and (alpha != 1):
                continue

            collection = Collection(self.COLLECTION_FILE,
                                    import_collection=import_collection,
                                    export_collection=export_collection,
                                    export_statistics=self.args.statistics,
                                    bm25fr_weighting=True,
                                    export_weighted_idx=self.args.export_weighted_idx,
                                    is_collection_pre_processed=self.args.pre_processed,
                                    parser_granularity=[".//bdy", ".//title", ".//categories"],
                                    )

            import_collection = True
            export_collection = False

            collection.weighting_strategy = BM25FrWeighting(k1=1.2, b=0.75, alpha=alpha, beta=beta, gamma=gamma)
            collection.weighted_index = collection.weighting_strategy.calculate_weight(collection)
            
            evaluate_run(collection, self.args.granularity, self.args.pre_processed)
