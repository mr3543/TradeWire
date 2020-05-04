import os
from typing import List

class Reader:
    def __init__(self,base_dir:str, file_stub:str,
                 com_list:List[str],output_type:str,
                 dct=None):
        
        """
        Parameters
        ------------
        
        base_dir: str, base directory containing company texts
        file_stub: str, name of the files to be read, a file is constructed
                   as base_dir/ticker/file_stub
        com_list: List[str], list of company tickers to read out
        output_type: str, 'list': splits a file on whitespace 
                           'bow': runs file through dct to get bow representation
                                  must also provide gensim dictionary object in dct
                                  parameter
                          'text': returns raw text file 
        dct: gensim.corpora.Dictionary, for 'bow' output_type will pass text through 
             dct to get bow representation
         """
        
        self.base_dir     = base_dir
        self.file_stub    = file_stub
        self.com_list     = com_list
        self.output_type  = output_type
        self.dct          = dct

    def get_bow(self,tckr):
        text = self.__getitem__(tckr)
        return self.dct.doc2bow(text.split(' '))
    
    def __getitem__(self,tckr):
        filename = os.path.join(self.base_dir,tckr,self.file_stub)
        with open(filename,'r') as f:
            text = f.read()
        return text

    def __iter__(self):
        for tckr in self.com_list:
            text = self.__getitem__(tckr)
            if self.output_type == 'bow':
                yield self.dct.doc2bow(text.split(' '))
            elif self.output_type == 'list':
                yield text.split(' ')
            else:
                yield text

    def __len__(self):
        return len(self.com_list)
