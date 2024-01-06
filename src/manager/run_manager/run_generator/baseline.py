from models.collection import Collection

from manager.text_processor import CustomTextProcessorNoStopNoStem
from manager.text_processor import CustomTextProcessorNoStem
from manager.text_processor import CustomTextProcessorNoStop

from manager.run_manager.utils.utils import evaluate_run


class Baseline:
    def __init__(self, collection_file, args):
        self.COLLECTION_FILE = collection_file
        self.args = args

    def run_baseline(self):
        """
        Runs the baseline. The baseline generates 12 runs : 3 (weighting schemes) * 2 (stop-list) * 2 (stemmer)
        """
        self.run_baseline_with_stop_and_stem()
        self.run_baseline_with_stop_and_no_stem()
        self.run_baseline_with_no_stop_and_stem()
        self.run_baseline_with_no_stop_and_no_stem()

    def run_baseline_with_stop_and_stem(self):
        collection = Collection(self.COLLECTION_FILE,
                                export_collection=True,
                                export_statistics=self.args.statistics,
                                ltn_weighting=True,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity
                                )

        evaluate_run(collection, self.args.granularity)

        collection = Collection(self.COLLECTION_FILE,
                                import_collection=True,
                                export_statistics=self.args.statistics,
                                ltc_weighting=True,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity
                                )
        evaluate_run(collection, self.args.granularity)

        collection = Collection(self.COLLECTION_FILE,
                                import_collection=True,
                                export_statistics=self.args.statistics,
                                bm25_weighting=True,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity
                                )
        evaluate_run(collection, self.args.granularity)

    def run_baseline_with_stop_and_no_stem(self):
        collection = Collection(self.COLLECTION_FILE,
                                export_collection=True,
                                export_statistics=self.args.statistics,
                                ltn_weighting=True,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity,
                                text_processor=CustomTextProcessorNoStem()
                                )
        evaluate_run(collection, self.args.granularity)

        collection = Collection(self.COLLECTION_FILE,
                                import_collection=True,
                                export_statistics=self.args.statistics,
                                ltc_weighting=True,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity
                                )
        evaluate_run(collection, self.args.granularity)

        collection = Collection(self.COLLECTION_FILE,
                                import_collection=True,
                                export_statistics=self.args.statistics,
                                bm25_weighting=True,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity
                                )
        evaluate_run(collection, self.args.granularity)

    def run_baseline_with_no_stop_and_stem(self):
        collection = Collection(self.COLLECTION_FILE,
                                export_collection=True,
                                export_statistics=self.args.statistics,
                                ltn_weighting=True,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity,
                                text_processor=CustomTextProcessorNoStop()
                                )
        evaluate_run(collection, self.args.granularity)

        collection = Collection(self.COLLECTION_FILE,
                                import_collection=True,
                                export_statistics=self.args.statistics,
                                ltc_weighting=True,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity
                                )
        evaluate_run(collection, self.args.granularity)

        collection = Collection(self.COLLECTION_FILE,
                                import_collection=True,
                                export_statistics=self.args.statistics,
                                bm25_weighting=True,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity
                                )
        evaluate_run(collection, self.args.granularity)

    def run_baseline_with_no_stop_and_no_stem(self):
        collection = Collection(self.COLLECTION_FILE,
                                export_collection=True,
                                export_statistics=self.args.statistics,
                                ltn_weighting=True,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity,
                                text_processor=CustomTextProcessorNoStopNoStem()
                                )
        evaluate_run(collection, self.args.granularity)

        collection = Collection(self.COLLECTION_FILE,
                                import_collection=True,
                                export_statistics=self.args.statistics,
                                ltc_weighting=True,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity
                                )
        evaluate_run(collection, self.args.granularity)

        collection = Collection(self.COLLECTION_FILE,
                                import_collection=True,
                                export_statistics=self.args.statistics,
                                bm25_weighting=True,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity
                                )
        evaluate_run(collection, self.args.granularity)
