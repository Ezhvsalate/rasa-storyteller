import shutil

import yaml


class Exporter(object):

    def __init__(self, nlu, resp, stories, nlu_file, domain_file, stories_file):
        self.nlu = nlu
        self.resp = resp
        self.stories = stories
        self.nlu_file = nlu_file
        self.domain_file = domain_file
        self.stories_file = stories_file

    def export(self):
        nlu_data = self.nlu.export_data()
        resp_data = self.resp.export_data()
        stories_data = self.stories.export_data()

        with open(self.nlu_file, 'w', encoding='utf-8') as nf:
            nlu_data['result'].seek(0)
            shutil.copyfileobj(nlu_data['result'], nf)

        domain_data = {"actions": resp_data['actions'],
                       "intents": nlu_data['intents'],
                       "responses": resp_data['responses']}
        with open(self.domain_file, 'w', encoding='utf-8') as df:
            df.write(yaml.safe_dump(domain_data, allow_unicode=True))

        with open(self.stories_file, 'w', encoding='utf-8') as sf:
            stories_data.seek(0)
            shutil.copyfileobj(stories_data, sf)
