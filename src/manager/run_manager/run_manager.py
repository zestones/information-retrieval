from models.collection import Collection
from manager.query_manager import QueryManager

from manager.text_processor import CustomTextProcessorNoStopNoStem
from manager.text_processor import CustomTextProcessorNoStem
from manager.text_processor import CustomTextProcessorNoStop
from manager.text_processor import RegexTextProcessor

from manager.run_manager.run_generator.baseline import Baseline
from manager.run_manager.run_generator.grid_search import ParametersTuning
import manager.run_manager.utils.utils as utils

import os


class RunManager:
    def __init__(self, args):
        self.RUN_OUTPUT_FOLDER = "../docs/resources/runs/"
        if not os.path.exists(self.RUN_OUTPUT_FOLDER):
            os.makedirs(self.RUN_OUTPUT_FOLDER)

        # XML-Coll-withSem
        self.COLLECTION_FILE = '../lib/processed_data/XML-Coll-withSem_stop671_porter.zip'
        self.args = args

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
                                parser_granularity=(
                                    [".//bdy", ".//title", ".//categories"] if (self.args.bm25fw or self.args.bm25fr) else self.args.granularity),
                                )

        utils.evaluate_run(collection, self.args.granularity)
