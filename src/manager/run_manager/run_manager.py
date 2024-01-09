from models.collection import Collection
from manager.query_manager import QueryManager

from manager.text_processor import CustomTextProcessorNoStopNoStem
from manager.text_processor import CustomTextProcessorNoStem
from manager.text_processor import CustomTextProcessorNoStop
from manager.text_processor import ReferenceTextProcessor
from manager.text_processor import ReferenceRearrangedTextProcessor
from manager.text_processor import CustomTextProcessor

from manager.run_manager.run_generator.baseline import Baseline
from manager.run_manager.run_generator.grid_search import ParametersTuning
import manager.run_manager.utils.utils as utils

import os

class RunManager:
    def __init__(self, args):
        self.RUN_OUTPUT_FOLDER = "../docs/resources/runs/"
        if not os.path.exists(self.RUN_OUTPUT_FOLDER):
            os.makedirs(self.RUN_OUTPUT_FOLDER)

        self.args = args
        if self.args.pre_processed:
            # XML-Coll-withSem_stop670_porter
            self.COLLECTION_FILE = '../lib/processed_data/XML-Coll-withSem_stop670_porter.zip'
            self.text_processor = CustomTextProcessor()
        else:
            # XML-Coll-withSem
            self.COLLECTION_FILE = '../lib/data/practice_05/XML-Coll-withSem.zip'
            self.text_processor = CustomTextProcessor()

    def run(self):        
        if self.args.baseline:
            Baseline(self.COLLECTION_FILE, self.args).run_baseline()
        elif self.args.bm25_optimization:
            ParametersTuning(self.COLLECTION_FILE, self.args).run_optimization()
        else:
            self.run_custom()

    def run_custom(self):
        collection = Collection(self.COLLECTION_FILE,
                                import_collection=self.args.import_inverted_index,
                                export_collection=self.args.export_inverted_index,
                                export_statistics=self.args.statistics,
                                ltn_weighting=self.args.ltn,
                                ltc_weighting=self.args.ltc,
                                lnu_weighting=self.args.lnu,
                                bm25_weighting=self.args.bm25,
                                bm25fw_weighting=self.args.bm25fw,
                                bm25fr_weighting=self.args.bm25fr,
                                export_weighted_idx=self.args.export_weighted_idx,
                                is_collection_pre_processed=self.args.pre_processed,
                                parser_granularity=(
                                    [".//bdy", ".//title", ".//categories"] if (self.args.bm25fw or self.args.bm25fr) else self.args.granularity),
                                text_processor=self.text_processor
                                )

        utils.evaluate_run(collection, self.args.granularity, self.args.pre_processed)