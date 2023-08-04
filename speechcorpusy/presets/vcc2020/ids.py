"""VCC2020 identity"""

from typing import List
from itertools import chain

from speechcorpusy.interface import ItemId


def _gen_ids() -> List[ItemId]:
    """Generate item_id of all VCC2020 corpus item"""

    ids = []
    # "train_source"
    for spk in ["F1", "F2", "M1", "M2"]:
        for name in map(lambda num: f"E100{str(num).zfill(2)}", range(1, 71)):
            ids.append(ItemId("VCC20", "train_source", f"vcc20_SE{spk}", name))

    # "train_target_task1"
    for spk in ["F1", "F2", "M1", "M2"]:
        names_1 = map(lambda num: f"E100{str(num).zfill(2)}", range(51, 71))
        names_2 = map(lambda num: f"E200{str(num).zfill(2)}", range(1, 51))
        for name in chain(names_1, names_2):
            ids.append(ItemId("VCC20", "train_target_task1", f"vcc20_TE{spk}", name))

    # "train_target_task2"
    for spk in ["FF1", "FM1", "GF1", "GM1", "MF1", "MM1"]:
        for name in map(lambda num: f"{spk[0]}100{str(num).zfill(2)}", range(1, 71)):
            ids.append(ItemId("VCC20", "train_target_task2", f"vcc20_T{spk}", name))

    # "eval_source"
    for spk in ["F1", "F2", "M1", "M2"]:
        for name in map(lambda num: f"E300{str(num).zfill(2)}", range(1, 26)):
            ids.append(ItemId("VCC20", "eval_source", f"vcc20_SE{spk}", name))

    # "groundtruth" english
    for spk in ["F1", "F2", "M1", "M2"]:
        for name in map(lambda num: f"E300{str(num).zfill(2)}", range(1, 26)):
            ids.append(ItemId("VCC20", "groundtruth", f"vcc20_TE{spk}", name))

    # "groundtruth" cross-lingual
    for spk in ["FF1", "FM1", "GF1", "GM1", "MF1", "MM1"]:
        for name in map(lambda num: f"{spk[0]}300{str(num).zfill(2)}", range(1, 26)):
            ids.append(ItemId("VCC20", "groundtruth", f"vcc20_T{spk}", name))

    return ids

item_ids = _gen_ids()
