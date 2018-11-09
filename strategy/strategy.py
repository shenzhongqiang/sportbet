import pandas as pd
import betdata.hkjc
import betdata.cnlot

def find_best_bet(a, b, c):
    x = b*c
    y = a*c
    z = a*b
    x = x/(x+y+z)
    y = y/(x+y+z)
    z = z/(x+y+z)
    profit = 1/(1/a+1/b+1/c) - 1
    return (x, y, z, profit)

def sort_matches(matches):
    result = sorted(matches)
    return result

# both are sorted matches
def find_common_matches(a_matches, b_matches):
    i = 0
    j = 0
    result = []
    while i < len(a_matches) and j < len(b_matches):
        a_match = a_matches[i]
        b_match = b_matches[j]
        if a_match < b_match:
            i += 1
        elif a_match > b_match:
            j += 1
        else:
            result.append((a_match, b_match))
            i += 1
            j += 1
    return result

if __name__ == "__main__":
    hkjc_feed = betdata.hkjc.Feed()
    cnlot_feed = betdata.cnlot.Feed()
    hkjc_matches = hkjc_feed.get_sports()
    cnlot_matches = cnlot_feed.get_games('2018-11-08')
    matches = []
    matches.extend(hkjc_matches)
    matches.extend(cnlot_matches)
    matches_dict = list(map(lambda x: x.to_dict(), matches))
    df = pd.DataFrame(matches_dict)

    grouped = df.groupby(['team_home', 'team_away', 'handicap', 'time'])
    for name, group in grouped:
        home_win = group["home_win"].max()
        away_win = group["away_win"].max()
        draw = group["draw"].max()
        (x, y, z, profit) = find_best_bet(home_win, away_win, draw)
        if profit > 0:
            print(name)
            print(x, y, z, profit)
