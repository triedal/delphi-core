import pefile
import glob
import pandas as pd
from config import cfg


class PEMiner(object):
    '''This class is used to mine PE header data from Windows PE files.'''
    
    def __init__(self):
        pass
        
    def __extract_features(self, path, is_malware):
        pe = pefile.PE(path, fast_load=True)
        features = {
            'e_cblp':                      pe.DOS_HEADER.e_cblp,
            'e_cp':                        pe.DOS_HEADER.e_cp,
            'e_cparhdr':                   pe.DOS_HEADER.e_cparhdr,
            'e_maxalloc':                  pe.DOS_HEADER.e_maxalloc,
            'e_sp':                        pe.DOS_HEADER.e_sp,
            'e_lfanew':                    pe.DOS_HEADER.e_lfanew,
            'NumberOfSections':            pe.FILE_HEADER.NumberOfSections,
            'MajorLinkerVersion':          pe.OPTIONAL_HEADER.MajorLinkerVersion,
            'MinorLinkerVersion':          pe.OPTIONAL_HEADER.MinorLinkerVersion,
            'SizeOfCode':                  pe.OPTIONAL_HEADER.SizeOfCode,
            'SizeOfInitializedData':       pe.OPTIONAL_HEADER.SizeOfInitializedData,
            'SizeOfUninitializedData':     pe.OPTIONAL_HEADER.SizeOfUninitializedData,
            'AddressOfEntryPoint':         pe.OPTIONAL_HEADER.AddressOfEntryPoint,
            'BaseOfCode':                  pe.OPTIONAL_HEADER.BaseOfCode,
            'BaseOfData':                  pe.OPTIONAL_HEADER.BaseOfData,
            'MajorOperatingSystemVersion': pe.OPTIONAL_HEADER.MajorOperatingSystemVersion,
            'MinorOperatingSystemVersion': pe.OPTIONAL_HEADER.MinorOperatingSystemVersion,
            'MajorImageVersion':           pe.OPTIONAL_HEADER.MajorImageVersion,
            'MinorImageVersion':           pe.OPTIONAL_HEADER.MinorImageVersion,
            'CheckSum':                    pe.OPTIONAL_HEADER.CheckSum,
            'MajorSubsystemVersion':       pe.OPTIONAL_HEADER.MajorSubsystemVersion,
            'MinorSubsystemVersion':       pe.OPTIONAL_HEADER.MinorSubsystemVersion,
            'Subsystem':                   pe.OPTIONAL_HEADER.Subsystem,
            'SizeOfStackReserve':          pe.OPTIONAL_HEADER.SizeOfStackReserve,
            'SizeOfStackCommit':           pe.OPTIONAL_HEADER.SizeOfStackCommit,
            'SizeOfHeapReserve':           pe.OPTIONAL_HEADER.SizeOfHeapReserve,
            'SizeOfHeapCommit':            pe.OPTIONAL_HEADER.SizeOfHeapCommit,
            'LoaderFlags':                 pe.OPTIONAL_HEADER.LoaderFlags,
            'Classification':              ('benign', 'malware')[is_malware]
        }
        return features
        
    def get_feature_set(self):
        """Builds dataframe by extracting features from Windows PE files. Files are located
        in the test_data directory.
        
        Returns:
            Pandas dataframe object.
        """
        root = cfg['paths']['proj_root']
        maldir = cfg['paths']['test_dirs']['malware']
        bendir = cfg['paths']['test_dirs']['benign']
        mal_paths = glob.glob(root + maldir + '/*.exe')
        ben_paths = glob.glob(root + bendir + '/*.exe')
        
        # TODO: I think there is a way to make this faster. Concatenating doesn't seem like the best option.
        mal_df = pd.DataFrame([self.__extract_features(path, True) for path in mal_paths])
        ben_df = pd.DataFrame([self.__extract_features(path, False) for path in ben_paths])
        df = pd.concat([mal_df, ben_df])
        return df

if __name__ == '__main__':
    miner = PEMiner()
    miner.get_feature_set()
    # pe_miner.extract_raw_features(sys.argv[1])
    # print pd.DataFrame([miner.extract_features(path) for path in paths]).to_string()
    
    