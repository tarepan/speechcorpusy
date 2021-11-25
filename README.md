<div align="center">

# 🎤 speechcorpusy 📖
The Python speech corpus handler

</div>

For data science on speech, corpus handling is indispensable - but troublesome - part.  
With preset handlers & interface & utilities, it become easy.  
`speechcorpusy` is the one!  

```python
corpus = speechcorpusy.presets.ZR19(conf)
corpus.get_contents()
all_utterances = corpus.get_identities()
path_wave_No1 = corpus.get_item_path(all_utterances[0])

sr, wave = scipy.io.wavfile.read(path_wave_No1)
# You can read a wav file with only five lines of code!
```

## What `speechcorpusy` do?
`speechcorpusy` provides three functionalities for corpus handler.  

- Preset hander
- Interface / AbstractBaseClass
- Implementation utilities
  - Data get, private mirror, directory handling etc.

With presets, you can use speech corpus with only few line of code.  
Thanks to the interface, you can switch corpuses without changing codes.  
The utilities shortcut common/boilerplate implementations of your original corpus.  

With these three functionalities, you can  
- **focus on corpus usage** as corpus user
- **focus on corpus-specific implementations** as handler implementer

## Usecases
### .wav Read
You can read a wav file with only five lines of code.
```python
corpus = speechcorpusy.presets.LJ(ConfCorpus(None, download=True)) # Preset LJSpeech corpus
corpus.get_contents() # Automatic corpus data download
all_utterances = corpus.get_identities() # List up utterances
path_wave_No1 = corpus.get_item_path(all_utterances[0]) # Get the path

sr, wave = scipy.io.wavfile.read(path_wave_No1)
```
### Corpus Switching
You can switch corpus without change in corpus-using codes.  
```python
# corpus = speechcorpusy.presets.LJ(conf) # LJSpeech corpus
corpus = speechcorpusy.presets.JVS(conf) # Japanese versatile speech corpus

# That's all. Now data is switched from LJSpeech to JVS.
# All downsteam code are never affected!
```
### Item selection
Choose your favorite data!  
```python
corpus = speechcorpusy.presets.LJ(conf)
alls = corpus.get_identities() # All itemID acquired

# Any your favorite items!
speaker_a = filter(lambda item_id: item_id.speaker == "Mr.A", alls) # only speaker Mr.A
whispers = filter(lambda item_id: item_id.subtype == "whisper", alls) # only whisper subcorpus

# Read is totally same
wave_speaker_a_No1 = librosa.load(corpus.get_item_path(speaker_a[0])
```

## APIs
### For handler user
For handler user, understanding just 3 classes is enough; *itemID* & *config* & *corpus*.  
**All handers use same config, have same methods and yield same itemID**.  

```python
@dataclass
class ItemId:
    subtype: str # Sub-corpus name
    speaker: str # Speaker ID
    name: str    # Item name

@dataclass
class ConfCorpus:
    root     # Adress of the directory under which the corpus archive is found or downloaded
    download # Whether to download original corpus if it is not found in `root`

class AbstractCorpus:
    def __init__(self, conf: ConfCorpus) -> None:

    def get_contents(self) -> None:
        """Get corpus contents into local."""

    def get_identities(self) -> List[ItemId]:
        """Get corpus item identities."""

    def get_item_path(self, item_id: ItemId) -> Path:
        """Get a path of the item."""
```
### For handler developer
Implement `speechcorpusy` with helpers.  
We strongly encourage you to check preset (e.g. [LJ](https://github.com/tarepan/speechcorpusy/blob/main/speechcorpusy/presets/lj/lj.py)).  
Once you understand helpers, you may be able to implement new handler within 15-min!  

### Full API list
All handlers 
- `speechcorpusy.presets`
  - LJSpeech/`LJ`, ZeroSpeech2019/`ZR19`, JVS/`JVS`, and others coming soon!
- [`speechcorpusy.interface.AbstractCorpus`](https://github.com/tarepan/speechcorpusy/blob/main/speechcorpusy/interface.py): the interface
- `speechcorpusy.helper`
  - [`.contents.get_contents`](https://github.com/tarepan/speechcorpusy/blob/main/speechcorpusy/helper/contents.py): Corpus contents acquisition (private local/S3/GDrive/etc & hook for origin)
  - [`.forward`](https://github.com/tarepan/speechcorpusy/blob/main/speechcorpusy/helper/forward.py)
    - `.forward`: Forward a corpus archive from origin to any adress for download or mirroring
    - `.forward_from_GDrive`: Forward from GoogleDrive to any adress for corpus copy

Of course, the value of `ItemID`'s `subtype`/`speaker`/`name` differ corpus by corpus.  
Currently, please check these values in each preset codes.  

### Advanced usecase
#### Dynamic corpus switching
Python's built-in `getattr` enable dynamic preset class use.  
With this feature, you can access any presets with just one-line.

```python
# `args.corpus_name` is exact corpus Class name (e.g. "LJ")
corpus = getattr(speechcorpusy.presets, args.corpus_name)(conf_corpus)
# If you switch command-line argument, corpus is automatically switched, wow!
```

For safe access in real usecase, we provide `corpus_list`.  

```python
from speechcorpusy import presets

if args.corpus_name in presets.corpus_list:
    corpus_cls = getattr(presets, args.corpus_name)
    corpus = corpus_cls(conf_corpus)
else:
    raise Exception(f"Corpus '{args.corpus_name}' is not supported by 'speechcurpusy'.")
```

## Project's Territory/Responsibility
```
     Corpus ------------- Dataset ------------- Loader/Batcher  
[Data / Handler]     [Data / Handler] 
           ↑
       This part!
```
