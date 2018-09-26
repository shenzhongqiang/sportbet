import os

def get_team_encn_mapping():
    folder = os.path.dirname(__file__)
    path = os.path.join(folder, "..", "betdata", "teams.csv")
    with open(path) as f:
        content = f.read()
        lines = content.split("\n")
        mapping = {}
        for line in lines:
            if not line:
                continue
            [en, cn]= line.split(",")
            if en and cn:
                mapping[en] = cn
        return mapping

def get_team_cnen_mapping():
    encn_mapping = get_team_encn_mapping()
    mapping = {}
    for en, cn in encn_mapping.items():
        mapping[cn] = en

    return mapping

def get_team_cn():
    mapping = get_team_encn_mapping()
    cn = mapping.values()
    return cn

def get_team_en():
    mapping = get_team_encn_mapping()
    en = mapping.keys()
    return en
