"""Contains different classes associated with feature mining."""

import pefile
import glob
import logging
import sys
import pandas as pd
from sqlalchemy import create_engine, exc
from tqdm import tqdm
from config import cfg
from datetime import datetime

engine = create_engine(cfg['sql_connection'], connect_args={'connect_timeout': 5})
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
        try:
            pe = pefile.PE(path, fast_load=True)
        except pefile.PEFormatError as err:
            return {}

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

    @staticmethod
    def get_feature_set():
        """Reads dataframe from SQL database.

        Returns:
            pandas.DataFrame: Complete dataframe object with features from dataset.
        """
        try:
            df = pd.read_sql_table('mal_clf_features', engine)
        except exc.SQLAlchemyError as err:
            logger.critical(' [X] %s', err)
            logger.critical(' [X] Exiting.')
            sys.exit(1)

        return df

    def mine_features_to_csv(self, mdir, bdir):
        """"Builds dataframe by extracting features from Windows PE files and exports dataframe
        to CSV file. Places CSV in current working directory.
        """
        mal_paths = glob.glob(mdir + '/*.exe')
        ben_paths = glob.glob(bdir + '/*.exe')

        print '\n----- MINING STATUS -----\n'
        # TODO: I think there is a way to make this faster. Concatenating doesn't seem like the best option.
        mal_df = pd.DataFrame([self.__extract_features(path, True) for path in tqdm(mal_paths, desc='Mal', ncols=75)])
        ben_df = pd.DataFrame([self.__extract_features(path, False) for path in tqdm(ben_paths, desc='Ben', ncols=75)])

        # ignore_index=True reindexes the dataframe so we do not have duplicate indexes
        df = pd.concat([mal_df, ben_df], ignore_index=True)

        if pd.isnull(df).values.any():
            df = df.dropna(how='all')
            df.reset_index(drop=True, inplace=True)

        print '\nTotal features: {}'.format(df.shape[1]-1)
        print 'Total samples:  {}'.format(df.shape[0])
        print '-------------------------\n'

        logger.info(' [!] Exporting features to CSV.')
        fname = 'features-' + datetime.now().strftime("%Y%m%d-%H%M%S") + '.csv'
        df.to_csv(fname)

    @staticmethod
    def save_csv_to_db(fpath):
        """Reads CSV file into dataframe and then saves dataframe to SQL db.

        Args:
            fpath (str): Path to PE file.
        """
        df = pd.read_csv(fpath, index_col=0)
        logger.info(' [!] Saving features to db.')
        df.to_sql('mal_clf_features', engine, if_exists='append')
