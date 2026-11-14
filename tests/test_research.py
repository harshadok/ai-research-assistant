from fastapi.testclient import TestClient

from app.main import create_app
from app.runtime import ProviderError


class Search:
    def __init__(self):
        self.fetched = 0
    def search(self, query, limit):
        return [{'pageid': i} for i in range(20)]
    def fetch(self, candidate):
        self.fetched += 1
        return {'title': 'Synthetic handbook', 'url': f"https://example.com/{candidate['pageid']}", 'text': 'Employees receive 24 days of annual leave.', 'retrieved_at': '2026-01-01', 'sha256': 'fixture'}


class Model:
    def structured(self, *args):
        return {'claims': [
            {'text': 'The handbook provides 24 leave days.', 'source_id': 'S1', 'quote': '24 days of annual leave'},
            {'text': 'Invented claim', 'source_id': 'S1', 'quote': 'This quote does not exist'},
            {'text': 'Unknown source', 'source_id': 'S99', 'quote': '24 days of annual leave'}],
            'uncertainties': ['This is a synthetic test source.']}


def test_agent_budget_and_quote_verification(tmp_path):
    search = Search()
    client = TestClient(create_app(tmp_path / 'db', search, Model()))
    response = client.post('/research', json={'question': 'annual leave', 'max_sources': 2})
    assert response.status_code == 201
    result = response.json()
    assert search.fetched == 2
    assert len(result['sources']) == 2
    assert len(result['claims']) == 1
    assert len(result['rejected_claims']) == 2
    assert result['claims'][0]['verification'] == 'quote_present_in_fetched_source'
    assert 'not establish' in result['verification_scope']
    exported = client.get('/research/' + result['id'] + '/export')
    assert exported.status_code == 200
    assert 'Invented claim' not in exported.text
    assert '24 days' in exported.text
    reopened = TestClient(create_app(tmp_path / 'db', Search(), Model()))
    assert reopened.get('/research/' + result['id']).json()['status'] == 'completed'


def test_sources_only_does_not_call_model(tmp_path):
    class Broken:
        def structured(self, *args):
            raise AssertionError('Should not call the model')
    client = TestClient(create_app(tmp_path / 'db', Search(), Broken()))
    result = client.post('/research', json={'question': 'annual leave', 'synthesize': False}).json()
    assert result['mode'] == 'sources_only'
    assert result['claims'] == []


def test_no_sources_and_provider_failure(tmp_path):
    class Empty(Search):
        def search(self, query, limit):
            return []
    client = TestClient(create_app(tmp_path / 'empty', Empty(), Model()))
    assert client.post('/research', json={'question': 'missing'}).json()['mode'] == 'insufficient_evidence'
    class Broken:
        def structured(self, *args):
            raise ProviderError('offline')
    client = TestClient(create_app(tmp_path / 'broken', Search(), Broken()))
    response = client.post('/research', json={'question': 'annual leave'})
    assert response.status_code == 502
    record_id = response.json()['detail']['id']
    assert client.get('/research/' + record_id).json()['status'] == 'failed'
    assert client.get('/research/' + record_id + '/export').status_code == 409


def test_bad_inputs(tmp_path):
    client = TestClient(create_app(tmp_path / 'db', Search(), Model()))
    assert client.post('/research', json={'question': 'ok', 'max_sources': 500}).status_code == 422
    assert client.get('/research/missing').status_code == 404
