import pandas as pd


def process(df, df2):
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].apply(lambda x: x.year)
    temp = df[["date", "id"]]
    df2 = df2.merge(temp, how="left", on="id")
    df2["year"] = df2["date"].apply(lambda x: x.year)
    return df, df2


def processYearTeamData(df, year, team):
    YearTeam_df = df[
        (df["year"] == year) & ((df["team1"] == team) | (df["team2"] == team))
    ]
    YearTeam_id = YearTeam_df["id"].tolist()
    return YearTeam_df, YearTeam_id


def processSeasonWiseData(df, year):
    return df[df["year"] == year]


def processMactheWiseData(df, year):
    working_df = df[df["year"] == year]
    working_df["date"] = working_df["date"].apply(lambda x: x.date())
    return working_df
