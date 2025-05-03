import pytest
import pandas as pd
from ..services.esma_data_loader import EsmaDataLoader
from ..services.esma_utils import Utils

@pytest.fixture(scope="module")
def esma_loader():
    """Create ESMA data loader instance"""
    return EsmaDataLoader()

@pytest.mark.esma
@pytest.mark.slow
def test_load_latest_files(esma_loader):
    result = esma_loader.load_latest_files()
    assert isinstance(result, pd.DataFrame)

@pytest.mark.esma
def test_load_fca(esma_loader):
    result = esma_loader.load_fca_firds_file_list()
    assert isinstance(result, pd.DataFrame)

@pytest.mark.esma
def test_load_mifid(esma_loader):
    result = esma_loader.load_mifid_file_list()
    assert isinstance(result, pd.DataFrame)

@pytest.mark.esma
@pytest.mark.slow
def test_download_file(esma_loader):
    url = 'https://firds.esma.europa.eu/firds/FULINS_C_20250426_01of01.zip'
    result = esma_loader.download_file(url)
    cached = esma_loader.download_file(url, update=True)
    assert isinstance(cached, pd.DataFrame)

@pytest.mark.esma
def test_wrong_cfi(esma_loader):
    result = esma_loader.load_latest_files(cfi='TEST')
    assert result is None

@pytest.mark.esma
def test_wrong_dataset(esma_loader):
    result = esma_loader.load_mifid_file_list(datasets=['TEST'])
    assert result is None

@pytest.mark.esma
def test_latest_files_wrong_isin(esma_loader):
    result = esma_loader.load_latest_files(isin=['TEST'])
    assert isinstance(result, pd.DataFrame)

@pytest.mark.esma
def test_vcap_latest_files(esma_loader):
    result = esma_loader.load_latest_files(vcap=True)
    assert isinstance(result, pd.DataFrame)

@pytest.mark.esma
def test_ssr_files(esma_loader):
    result = esma_loader.load_ssr_exempted_shares(today=True)
    assert isinstance(result, pd.DataFrame)