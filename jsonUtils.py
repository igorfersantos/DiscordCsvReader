import json


def filterJson(jsonFile, keywords = None):
    with open(jsonFile, 'rt', encoding="utf8") as json_file:
        data = json.load(json_file)

        if keywords is not None:
            for (k, v) in data.copy().items():
                dataValue = str(v)
                i = 0
                for keyword in keywords:
                    if keyword in dataValue: i += 1

                # se o i for igual a 0 significa que nenhum dos nomes foi encontrado
                if i == 0:
                    del data[k]
        else:
            return data

        return data;