"""Preset corpus handlers"""

from .jsut.jsut import JSUT       # pylint: disable=unused-import
from .jvs.jvs import JVS          # pylint: disable=unused-import
from .zr19.zr19 import ZR19       # pylint: disable=unused-import
from .lj.lj import LJ             # pylint: disable=unused-import
from .vctk.vctk import VCTK       # pylint: disable=unused-import
from .vcc2020.vcc20 import VCC20  # pylint: disable=unused-import
from .act100tsukuyomi.act100tsukuyomi import Act100TKYM # pylint: disable=unused-import
from .rhn46zunda.rhn46zunda import RHN46ZND             # pylint: disable=unused-import
from .testcorpus.testcorpus import TEST, TESTbeta       # pylint: disable=unused-import
from .adhoc.adhoc import AdHoc    # pylint: disable=unused-import


corpus_list = ["JSUT", "JVS", "ZR19", "LJ", "VCTK", "VCC20", "Act100TKYM", "RHN46ZND", "TEST", "TESTbeta", "AdHoc",]
