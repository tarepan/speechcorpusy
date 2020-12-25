# corpuspy - Python corpus handler infrastructure
For data science, corpus handling is indispensable - but troublesome - part.  
With common interface and utility functions, corpus handler implementation become easy.  
`corpuspy` is the one!  

## What `corpuspy` do?
`corpuspy` provides two functionalities for corpus handler.  

- Interface / AbstractBaseClass
- Implementation utilities
  - Data get, private mirror, directory handling etc.
  
Following the interface, you can smoothly implement your corpus handlers.  
The utilities shortcut common/boilerplate implementations.  
With these two functionality, you can **focus on corpus-specific implementations**.  

## Demo
```python
```

## APIs
- [corpuspy.interface.AbstractCorpus](https://github.com/tarepan/corpuspy/blob/main/corpuspy/interface.py): the interface
- utilities
  - [corpuspy.helper.contents.get_contents](https://github.com/tarepan/corpuspy/blob/main/corpuspy/helper/contents.py): Corpus contents acquisition (private local/S3/GDrive/etc & hook for origin)
  - [corpuspy.helper.forward.forward_from_GDrive](https://github.com/tarepan/corpuspy/blob/main/corpuspy/helper/forward.py) Forward from GoogleDrive to any adress for corpus copy
 
## Project's Territory/Responsibility
```
     Corpus ------------- Dataset ------------- Loader/Batcher  
[Data / Handler]     [Data / Handler] 
           ↑
       This part!
```
