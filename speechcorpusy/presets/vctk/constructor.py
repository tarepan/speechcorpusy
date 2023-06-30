"""Preset handler constructor for future update."""


from pathlib import Path

from .vctk import MAX_UTTR_MIC2, SPKS_MIC2


def extract_speakers(adress_root: str) -> list[str]:
    """Extract speaker names from the corpus.

    Args:
        adress_root - Root of expanded corpus archive (e.g. `./DS_10283_3443`)
    Returns:
                    - Speaker name list (e.g. ['p225', 'p226', ...])
    """

    raw_spk_dirs = list(filter(lambda p: p.name != "log.txt", Path(f"{adress_root}/wav48_silence_trimmed").iterdir()))
    raw_spk_dirs.sort(key=lambda p: p.name)
    raw_speakers = list(map(lambda p: p.stem, raw_spk_dirs))
    return raw_speakers


def extract_max_indice_speaker_mic2(adress_root: str, speakers_mic2: list[str]) -> list[int]:
    """Extract maximum mic2-utterance indice of each speaker.

    Args:
        adress_root   - Root of expanded corpus archive (e.g. `./DS_10283_3443`)
        speakers_mic2 - Mic2 speaker list
    """
    max_indice_spk: list[int] = []
    for spk in speakers_mic2:
        spk_dir = Path(f"{adress_root}/wav48_silence_trimmed") / spk
        utters_mic2 = list(filter(lambda p: p.stem[-4:] == "mic2", spk_dir.iterdir()))
        utters_mic2.sort(key=lambda p: p.name)
        last_idx = list(map(lambda p: int(p.stem[-8:-5]), utters_mic2))[-1]
        max_indice_spk.append(last_idx)
    return max_indice_spk


if __name__ == '__main__':
    ADRESS_ROOT = "./DS_10283_3443"

    assert list(filter(lambda spk: (spk != "p280") and (spk != "p315"), extract_speakers(ADRESS_ROOT))) == SPKS_MIC2

    assert extract_max_indice_speaker_mic2(ADRESS_ROOT, SPKS_MIC2) == MAX_UTTR_MIC2
