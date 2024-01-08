from models.collection import Collection

from manager.text_processor import CustomTextProcessorNoStopNoStem
from manager.text_processor import CustomTextProcessorNoStem
from manager.text_processor import CustomTextProcessorNoStop

from manager.run_manager.utils.utils import evaluate_run


class Baseline:
    def __init__(self, collection_file, args):
        self.COLLECTION_FILE = collection_file
        self.args = args
        
        if self.args.pre_processed:
            self.collection_name = collection_file.split('/')[-1].split('.')[0]
            self.collection_dir = collection_file.split(self.collection_name + '.zip')[0]
            if "_stop" in self.collection_name:
                self.collection_name = self.collection_name.split("_stop")[0]
            elif "_no_stop" in self.collection_name:
                self.collection_name = self.collection_name.split("_no_stop")[0]
                
            self.COLLECTION_FILE_STOP_PORTER = self.collection_dir + self.collection_name + "_stop670_porter.zip"
            self.COLLECTION_FILE_STOP_NO_STEM = self.collection_dir + self.collection_name + "_stop670_no_stem.zip"
            self.COLLECTION_FILE_NO_STOP_PORTER = self.collection_dir + self.collection_name + "_no_stop_porter.zip"
            self.COLLECTION_FILE_NO_STOP_NO_STEM = self.collection_dir + self.collection_name + "_no_stop_no_stem.zip"

    def run_baseline(self):
        """
        Runs the baseline. The baseline generates 12 runs : 3 (weighting schemes) * 2 (stop-list) * 2 (stemmer)
        """
        self.run_baseline_with_stop_and_stem()
        self.run_baseline_with_stop_and_no_stem()
        self.run_baseline_with_no_stop_and_stem()
        self.run_baseline_with_no_stop_and_no_stem()

    def run_baseline_with_stop_and_stem(self):
        collection = Collection(self.COLLECTION_FILE_STOP_PORTER if self.args.pre_processed else self.COLLECTION_FILE,
                                export_collection=True,
                                export_statistics=self.args.statistics,
                                ltn_weighting=True,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity,
                                is_collection_pre_processed=self.args.pre_processed,
                                )

        evaluate_run(collection, self.args.granularity, self.args.pre_processed)

        collection = Collection(self.COLLECTION_FILE_STOP_PORTER if self.args.pre_processed else self.COLLECTION_FILE,
                                import_collection=True,
                                export_statistics=self.args.statistics,
                                ltc_weighting=True,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity,
                                is_collection_pre_processed=self.args.pre_processed,
                                )
        evaluate_run(collection, self.args.granularity, self.args.pre_processed)

        collection = Collection(self.COLLECTION_FILE_STOP_PORTER if self.args.pre_processed else self.COLLECTION_FILE,
                                import_collection=True,
                                export_statistics=self.args.statistics,
                                bm25_weighting=True,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity,
                                is_collection_pre_processed=self.args.pre_processed,
                                )
        evaluate_run(collection, self.args.granularity, self.args.pre_processed)

    def run_baseline_with_stop_and_no_stem(self):
        collection = Collection(self.COLLECTION_FILE_STOP_NO_STEM if self.args.pre_processed else self.COLLECTION_FILE,
                                export_collection=True,
                                export_statistics=self.args.statistics,
                                ltn_weighting=True,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity,
                                is_collection_pre_processed=self.args.pre_processed,
                                text_processor=CustomTextProcessorNoStem()
                                )
        evaluate_run(collection, self.args.granularity, self.args.pre_processed)

        collection = Collection(self.COLLECTION_FILE_STOP_NO_STEM if self.args.pre_processed else self.COLLECTION_FILE,
                                import_collection=True,
                                export_statistics=self.args.statistics,
                                ltc_weighting=True,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity,
                                is_collection_pre_processed=self.args.pre_processed,
                                text_processor=CustomTextProcessorNoStem()
                                )
        evaluate_run(collection, self.args.granularity, self.args.pre_processed)

        collection = Collection(self.COLLECTION_FILE_STOP_NO_STEM if self.args.pre_processed else self.COLLECTION_FILE,
                                import_collection=True,
                                export_statistics=self.args.statistics,
                                bm25_weighting=True,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity,
                                is_collection_pre_processed=self.args.pre_processed,
                                text_processor=CustomTextProcessorNoStem()
                                )
        evaluate_run(collection, self.args.granularity, self.args.pre_processed)

    def run_baseline_with_no_stop_and_stem(self):
        collection = Collection(self.COLLECTION_FILE_NO_STOP_PORTER if self.args.pre_processed else self.COLLECTION_FILE,
                                export_collection=True,
                                export_statistics=self.args.statistics,
                                ltn_weighting=True,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity,
                                is_collection_pre_processed=self.args.pre_processed,
                                text_processor=CustomTextProcessorNoStop()
                                )
        evaluate_run(collection, self.args.granularity, self.args.pre_processed)

        collection = Collection(self.COLLECTION_FILE_NO_STOP_PORTER if self.args.pre_processed else self.COLLECTION_FILE,
                                import_collection=True,
                                export_statistics=self.args.statistics,
                                ltc_weighting=True,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity,
                                is_collection_pre_processed=self.args.pre_processed,
                                text_processor=CustomTextProcessorNoStop()
                                )
        evaluate_run(collection, self.args.granularity, self.args.pre_processed)

        collection = Collection(self.COLLECTION_FILE_NO_STOP_PORTER if self.args.pre_processed else self.COLLECTION_FILE,
                                import_collection=True,
                                export_statistics=self.args.statistics,
                                bm25_weighting=True,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity,
                                is_collection_pre_processed=self.args.pre_processed,
                                text_processor=CustomTextProcessorNoStop()
                                )
        evaluate_run(collection, self.args.granularity, self.args.pre_processed)

    def run_baseline_with_no_stop_and_no_stem(self):
        collection = Collection(self.COLLECTION_FILE_NO_STOP_NO_STEM if self.args.pre_processed else self.COLLECTION_FILE,
                                export_collection=True,
                                export_statistics=self.args.statistics,
                                ltn_weighting=True,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity,
                                is_collection_pre_processed=self.args.pre_processed,
                                text_processor=CustomTextProcessorNoStopNoStem()
                                )
        evaluate_run(collection, self.args.granularity, self.args.pre_processed)

        collection = Collection(self.COLLECTION_FILE_NO_STOP_NO_STEM if self.args.pre_processed else self.COLLECTION_FILE,
                                import_collection=True,
                                export_statistics=self.args.statistics,
                                ltc_weighting=True,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity,
                                is_collection_pre_processed=self.args.pre_processed,
                                text_processor=CustomTextProcessorNoStopNoStem()
                                )
        evaluate_run(collection, self.args.granularity, self.args.pre_processed)

        collection = Collection(self.COLLECTION_FILE_NO_STOP_NO_STEM if self.args.pre_processed else self.COLLECTION_FILE,
                                import_collection=True,
                                export_statistics=self.args.statistics,
                                bm25_weighting=True,
                                export_weighted_idx=self.args.export_weighted_idx,
                                parser_granularity=self.args.granularity,
                                is_collection_pre_processed=self.args.pre_processed,
                                text_processor=CustomTextProcessorNoStopNoStem()
                                )
        evaluate_run(collection, self.args.granularity, self.args.pre_processed)
