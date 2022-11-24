import csv
import logging
from typing import List

from model.OutputModel import ResultData


logger = logging.getLogger(__name__)

def write_header(file_path: str) -> None:
    """ ヘッダー行の出力
    Args:
        file_path (str): ファイルパス
    """
    print(file_path)
    with open(file_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(ResultData.get_field_names())


def output_result(result_list: List[ResultData], file_path: str) -> None:
    """ 結果出力（追記）
    Args:
        result_list (List[ResultData]): 結果データ
        file_path (str): 出力先ファイルパス
    """

    logger.debug('result_list: %s', result_list)

    with open(file_path, 'a', encoding='utf-8') as f:

        writer = csv.writer(f)
        for result in result_list:
            writer.writerow(result.to_list())