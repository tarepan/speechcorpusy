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
  Corpus data get (local/S3/GDrive etc)
  - Private corpus mirror
  - Local corpus data directory handling

## Project's Territory/Responsibility
```
     Corpus ------------- Dataset ------------- Loader/Batcher  
[Data / Handler]     [Data / Handler] 
           ↑
       This part!
```
