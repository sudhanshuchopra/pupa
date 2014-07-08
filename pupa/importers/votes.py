from .base import BaseImporter
from opencivicdata.models import VoteEvent, LegislativeSession


class VoteImporter(BaseImporter):
    _type = 'vote'
    model_class = VoteEvent
    related_models = {'counts': {}, 'votes': {}, 'sources': {}}

    def __init__(self, jurisdiction_id,
                 person_importer, org_importer, bill_importer):

        super(VoteImporter, self).__init__(jurisdiction_id)
        self.person_importer = person_importer
        self.bill_importer = bill_importer
        self.org_importer = org_importer

    def get_object(self, vote):
        spec = {
            'identifier': vote['identifier'],
            'legislative_session__identifier': vote['legislative_session'],
            'legislative_session__jurisdiction_id': self.jurisdiction_id,
        }
        # TODO: use bill, session, etc.
        return self.model_class.objects.get(**spec)

    def prepare_for_db(self, data):
        data['legislative_session'] = LegislativeSession.objects.get(
            name=data.pop('legislative_session'), jurisdiction_id=self.jurisdiction_id)
        data['organization_id'] = self.org_importer.resolve_json_id(data.pop('organization'))
        data['bill_id'] = self.bill_importer.resolve_json_id(data.pop('bill'))
        return data
