import json
import shutil

import yaml


class Exporter(object):
    def __init__(
        self, nlu, resp, stories, nlu_file_md, nlu_file_json, domain_file, stories_file
    ):
        self.nlu = nlu
        self.resp = resp
        self.stories = stories
        self.nlu_file_md = nlu_file_md
        self.nlu_file_json = nlu_file_json
        self.domain_file = domain_file
        self.stories_file = stories_file

    def export(self):
        nlu_data = self.nlu.export_data()
        resp_data = self.resp.export_data()
        stories_data = self.stories.export_data()

        with open(self.nlu_file_md, "w", encoding="utf-8") as nf:
            nlu_data["result"].seek(0)
            shutil.copyfileobj(nlu_data["result"], nf)

        with open(self.nlu_file_json, "w", encoding="utf-8") as nfj:
            nfj.write(json.dumps(nlu_data["result_json"], ensure_ascii=False, indent=4))

        domain_data = {
            "actions": resp_data["actions"],
            "intents": nlu_data["intents"],
            "responses": resp_data["responses"],
        }
        with open(self.domain_file, "w", encoding="utf-8") as df:
            df.write(yaml.safe_dump(domain_data, allow_unicode=True))

        with open(self.stories_file, "w", encoding="utf-8") as sf:
            stories_data.seek(0)
            shutil.copyfileobj(stories_data, sf)
