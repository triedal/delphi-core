"""Contains different classes associated with feature mining."""

import pefile
import glob
import logging
import pandas as pd
from sqlalchemy import create_engine
from tqdm import tqdm, trange
from config import cfg

engine = create_engine(cfg['sql_connection'])
logger = logging.getLogger(__name__)

class PEMiner(object):
    """This class is used to mine PE header data from Windows PE files."""

    def __init__(self):
        pass

    @staticmethod
    def __extract_features(path, is_malware):
        """Extracts features from a single PE file.

        Args:
            path (str): Path to PE file.
            is_malware (bool): Used for labeling. Denotes whether the file is malware or not.

        Returns:
            dict: Contains the mined features.
        """
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
            'Type':                        ('benign', 'malware')[is_malware]
        }
        return features

    def get_feature_set(self):
        """Builds dataframe by extracting features from Windows PE files. Files are located
        in the test_data directory.

        Returns:
            pandas.DataFrame: Complete dataframe object with features from dataset.
        """
        if cfg['read_features_from_db']:
            df = pd.read_sql_table('mal_clf_features', engine)
        else:
            root = cfg['paths']['proj_root']
            maldir = cfg['paths']['data_dirs']['malware']
            bendir = cfg['paths']['data_dirs']['benign']
            mal_paths = glob.glob(root + maldir + '/*.exe')
            ben_paths = glob.glob(root + bendir + '/*.exe')

            print '\n----- MINING STATUS -----\n'
            # TODO: I think there is a way to make this faster. Concatenating doesn't seem like the best option.
            mal_df = pd.DataFrame([self.__extract_features(path, True) for path in tqdm(mal_paths, desc='Mal', ncols=75)])
            ben_df = pd.DataFrame([self.__extract_features(path, False) for path in tqdm(ben_paths, desc='Ben', ncols =75)])
            print '\n-------------------------\n'

            # ignore_index=True reindexes the dataframe so we do not have duplicate indexes
            df = pd.concat([mal_df, ben_df], ignore_index=True)
            
            logger.info(' [!] Saving features to database.')
            df.to_sql('mal_clf_features', engine, if_exists='append')

        return df
