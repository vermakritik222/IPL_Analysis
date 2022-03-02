import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def AllTeams(df):
    a = df["team1"].unique().tolist()
    a.sort()
    return a


def AllTeamYearWise(df, year):
    a_df = df[df["year"] == year]
    temp = a_df["team1"]
    temp.append(a_df["team2"])
    temp = temp.unique().tolist()
    temp.sort()
    return temp


def AllYears(df):
    return df["year"].unique().tolist()


def AllPlayers(df2):
    Players = np.concatenate((df2["batsman"].unique(), df2["bowler"].unique()))
    Players.sort()
    return Players


def AllBatsman(df2):
    batsman = df2["batsman"].unique()
    batsman.sort()
    return batsman

# ############   "Overall Analysis",
#


def plotOverallYearsWiseWin(df, year):
    data = []
    for yr in year:
        data.append(
            df[df["year"] == yr]["winner"].value_counts(
            ).reset_index().iloc[0]["index"]
        )

    levels = np.tile([-5, 5, -3, 3, -1, 1],
                     int(np.ceil(len(year) / 6)))[: len(year)]

    fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)
    ax.set(title="Season wise winers of IPL")

    ax.vlines(year, 0, levels, color="tab:red")
    ax.plot(year, np.zeros_like(year), "-o", color="k", markerfacecolor="w")

    for d, l, r in zip(year, levels, data):
        ax.annotate(
            r,
            xy=(d, l),
            xytext=(-3, np.sign(l) * 3),
            textcoords="offset points",
            horizontalalignment="right",
            verticalalignment="bottom" if l > 0 else "top",
        )

    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

    ax.yaxis.set_visible(False)
    ax.spines[["left", "top", "right"]].set_visible(False)

    ax.margins(y=0.1)
    return fig, data


def plotOverallfrequencyOfWining(data, year):
    frequencyOfWining = pd.Series(data, year)
    frequencyOfWining = frequencyOfWining.value_counts().reset_index()
    frequencyOfWining.sort_values(0, inplace=True)

    fig = px.line(
        x=frequencyOfWining["index"],
        y=frequencyOfWining[0],
        labels={"y": "Count", "x": "Teams"},
    )
    fig.update_traces(mode="markers+lines")
    return fig


def plotOverallfrequencyOfWinnerNnoOfMatchesPlayed(df):
    frequencyOfWinner = df["winner"].value_counts().reset_index()
    frequencyOfWinner.sort_values("winner", inplace=True)
    frequencyOfWinner.rename(
        columns={"index": "Teams", "winner": "No. of Matches Win"}, inplace=True
    )
    noOfMatchesPlayed = df["team2"].value_counts() + df["team1"].value_counts()
    noOfMatchesPlayed = noOfMatchesPlayed.reset_index()
    noOfMatchesPlayed.rename(
        columns={"index": "Teams", 0: "No. of Matches Played"}, inplace=True
    )
    noOfMatchesPlayed.sort_values("No. of Matches Played", inplace=True)
    frequencyOfWinner = frequencyOfWinner.merge(
        noOfMatchesPlayed, how="left", on="Teams"
    )

    fig = px.line(
        frequencyOfWinner,
        x="Teams",
        y=frequencyOfWinner.columns,
        labels={"value": "Count", "variable": "Matches"},
    )
    fig.update_layout(height=600, width=800)
    fig.update_traces(mode="markers+lines")
    # fig.update_traces(height=600, width=800,mode='markers+lines')
    return fig


def plotOverallfrequencyOfCities(df):
    frequencyOfcities = df["city"].value_counts().reset_index()
    frequencyOfcities.sort_values("city", inplace=True)
    frequencyOfcities.rename(
        columns={"index": "Cities", "city": "No. of Matches"}, inplace=True
    )

    fig = px.line(frequencyOfcities, x="Cities", y="No. of Matches")
    fig.update_traces(mode="markers+lines")

    return fig


def plotOverallfrequencyOfVenue(df):
    frequencyOfVenue = df["venue"].value_counts().reset_index()
    frequencyOfVenue.sort_values("venue", inplace=True)
    frequencyOfVenue.rename(
        columns={"index": "Venue", "venue": "No. of Matches"}, inplace=True
    )

    fig = px.line(frequencyOfVenue, x="Venue", y="No. of Matches")
    fig.update_layout(height=600, width=800)
    fig.update_traces(mode="markers+lines")
    return fig


def plotOverallTop50PlayersOfAllTime(df):
    top50player_of_match = df["player_of_match"].value_counts().reset_index()
    top50player_of_match = top50player_of_match.head(50)
    top50player_of_match.sort_values("player_of_match", inplace=True)
    top50player_of_match.rename(
        columns={"index": "Player of Match",
                 "player_of_match": "No. of Matches"},
        inplace=True,
    )

    fig = px.line(
        top50player_of_match,
        x="Player of Match",
        y="No. of Matches",
        labels={"Player of Match": "Players"},
    )
    fig.update_layout(height=600, width=800)
    fig.update_traces(mode="markers+lines")
    return fig


def plotOverallToss(df):
    toss = df["toss_winner"].value_counts().reset_index()
    df[df["toss_winner"] == "Kolkata Knight Riders"]["toss_decision"].value_counts()
    toss["Field"] = toss["index"].apply(
        lambda x: df[df["toss_winner"] == x]["toss_decision"].value_counts()[0]
    )
    toss["Bat"] = toss["toss_winner"] - toss["Field"]
    toss.sort_values("toss_winner", inplace=True)
    toss.rename(columns={"toss_winner": "Toss Win"}, inplace=True)

    fig = px.line(
        toss,
        x="index",
        y=toss.columns,
        labels={"value": "Count", "index": "Teams",
                "variable": "Toss Decision"},
    )
    fig.update_traces(mode="markers+lines")
    return fig


def pieplotOverallToss(df):
    tossbi = df["toss_decision"].value_counts().reset_index()
    fig = px.pie(
        tossbi,
        values="toss_decision",
        color="index",
        color_discrete_map={"field": "royalblue", "bat": "darkblue"},
    )
    fig.update_traces(textposition="inside", textinfo="percent")
    return fig


# ####################   "Season Wise Analysis",
def plotSeasonBowlers(ids, df2, compare):
    date = []
    bowler = []
    wicket = []
    totalWickes = []
    for id in ids:

        season_df = df2[df2["id"] == id]
        date.append(season_df["date"].tolist()[0].date())
        team = season_df["bowling_team"].unique().tolist()

        bowler_df = season_df[season_df["bowling_team"] == team[0]]
        bowler_df["ball"] = 1
        bowler_df = bowler_df.groupby("bowler").sum()
        if max(bowler_df["is_wicket"].tolist()) == min(bowler_df["is_wicket"].tolist()):
            bowler_df.sort_values("ball", inplace=True, ascending=False)
        else:
            bowler_df.sort_values("is_wicket", inplace=True, ascending=False)
        temp_bowler1 = bowler_df.reset_index(
        )[["bowler", "is_wicket"]].iloc[0][0]
        temp_wicket1 = bowler_df.reset_index(
        )[["bowler", "is_wicket"]].iloc[0][1]
        if compare:
            temp_totalWickes1 = bowler_df.reset_index()["is_wicket"].sum()

        bowler_df = season_df[season_df["bowling_team"] == team[1]]
        bowler_df["ball"] = 1
        bowler_df = bowler_df.groupby("bowler").sum()
        if max(bowler_df["is_wicket"].tolist()) == min(bowler_df["is_wicket"].tolist()):
            bowler_df.sort_values("ball", inplace=True, ascending=False)
        else:
            bowler_df.sort_values("is_wicket", inplace=True, ascending=False)

        temp_bowler2 = bowler_df.reset_index(
        )[["bowler", "is_wicket"]].iloc[0][0]
        temp_wicket2 = bowler_df.reset_index(
        )[["bowler", "is_wicket"]].iloc[0][1]
        if compare:
            temp_totalWickes2 = bowler_df.reset_index()["is_wicket"].sum()

        if temp_wicket2 > temp_wicket1:
            bowler.append(temp_bowler2)
            wicket.append(temp_wicket2)
            if compare:
                totalWickes.append(temp_totalWickes2)
        else:
            bowler.append(temp_bowler1)
            wicket.append(temp_wicket1)
            if compare:
                totalWickes.append(temp_totalWickes1)

    temp_df = pd.DataFrame()
    temp_df["Matches"] = date
    temp_df["Bowler"] = bowler
    temp_df["Wicket"] = wicket

    if compare:
        temp_df["Total Wicket"] = totalWickes
    temp_df.sort_values("Matches", inplace=True)

    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(
        go.Scatter(
            x=temp_df["Matches"].tolist(),
            y=temp_df["Wicket"].tolist(),
            hovertemplate="Wickets: Wickets of Top Bowler"
            + "<br>Matche: %{x}<br>"
            + "Wicket: %{y}<br>"
            + "Bowler: %{text}",
            text=temp_df["Bowler"].tolist(),
            name="Wickets of Top Bowler",
        ),
        row=1,
        col=1,
    )

    if compare:
        fig.add_trace(
            go.Scatter(
                x=temp_df["Matches"].tolist(),
                y=temp_df["Total Wicket"].tolist(),
                hovertemplate="Wickets: Total Wickets"
                + "<br>Matche: %{x}<br>"
                + "Wicket: %{y}",
                text=temp_df["Bowler"].tolist(),
                name="Total Wickets",
            ),
            row=1,
            col=1,
        )
    fig.update_traces(mode="markers+lines")
    fig.update_layout(
        height=600,
        width=900,
        title_text="Top Performing Bowler",
        xaxis_title="Matches",
        yaxis_title="Count",
        legend_title="Wickets",
    )

    return fig


def plotSeasonalRunDistribution(year, teams, df2):
    s4 = []
    s6 = []
    for team in teams:
        s4.append(
            df2[(df2["year"] == year) & (
                df2["batting_team"] == team)]["batsman_runs"]
            .value_counts()
            .sort_index()
            .loc[4]
        )
        s6.append(
            df2[(df2["year"] == year) & (
                df2["batting_team"] == team)]["batsman_runs"]
            .value_counts()
            .sort_index()
            .loc[6]
        )
    temp_df = pd.DataFrame()
    temp_df["Team"] = teams
    temp_df["s4"] = s4
    temp_df["s6"] = s6

    fig = px.line(
        temp_df,
        x="Team",
        y=["s4", "s6"],
        labels={"value": "Count", "variable": "Boundaries"},
    )
    fig.update_layout(height=600, width=900)
    fig.update_traces(mode="markers+lines")

    return fig


def boxPlotSeasonalRunDistribution(teams, df, df2, mode):
    temp_df = pd.DataFrame()
    fig = go.Figure()

    for team in teams:
        teamId = df[(df["team1"] == team) | (
            df["team2"] == team)]["id"].tolist()
        s = []

        for id in teamId:
            q = df2[(df2["id"] == id) & (df2["batting_team"] == team)][
                "batsman_runs"
            ].value_counts()
            if 6 in q.index.tolist() and mode == "6s":
                s.append(q.loc[6])
            if 4 in q.index.tolist() and mode == "4s":
                s.append(q.loc[4])

        fig.add_trace(go.Box(y=s, quartilemethod="linear", name=team))

    fig.update_layout(
        height=600,
        width=900,
        title_text="Total number of {}'s".format(mode.split("s")[0]),
        xaxis_title="Team's",
        yaxis_title="Count of {}".format(mode.split("s")[0]),
        legend_title="Team's",
    )
    return fig


def plotOverwiseRunDistributionOfSeason(teams, df, df2, QuartileMethod):
    temp_df = pd.DataFrame()
    fig = go.Figure()
    for team in teams:
        teamId = df[(df["team1"] == team) | (
            df["team2"] == team)]["id"].tolist()
        runs = []
        for id in teamId:
            runs.append(
                df2[(df2["id"] == id) & (df2["batting_team"] == team)][
                    "total_runs"
                ].sum()
            )
        fig.add_trace(go.Box(y=runs, quartilemethod=QuartileMethod, name=team))
    return fig


def eliminatorRoundsTableOfSeason(working_df):
    temp = working_df[working_df["eliminator"] == "Y"]
    eliminatorRounds = pd.DataFrame()
    eliminatorRounds["Teams"] = temp["team1"] + " VS " + temp["team2"]
    eliminatorRounds["Toss Winner"] = temp["toss_winner"]
    eliminatorRounds["Toss Decision"] = temp["toss_decision"]
    eliminatorRounds["Winner"] = temp["winner"]
    eliminatorRounds["Result"] = temp["result"]
    eliminatorRounds["Result Margin"] = temp["result_margin"]
    eliminatorRounds["Player Of Match"] = temp["player_of_match"]
    eliminatorRounds["City"] = temp["city"]
    eliminatorRounds["Stadium"] = temp["venue"]
    eliminatorRounds["Date"] = temp["date"].apply(lambda x: x.date())
    eliminatorRoundsID = temp["id"].tolist()
    return eliminatorRounds, eliminatorRoundsID


def plotTossSeasonStat(working_df):
    toss = working_df["toss_winner"].value_counts().reset_index()
    working_df[working_df["toss_winner"] == "Kolkata Knight Riders"][
        "toss_decision"
    ].value_counts()
    toss["Field"] = toss["index"].apply(
        lambda x: working_df[working_df["toss_winner"] == x][
            "toss_decision"
        ].value_counts()[0]
    )
    toss["Bat"] = toss["toss_winner"] - toss["Field"]
    toss.sort_values("toss_winner", inplace=True)
    toss.rename(columns={"toss_winner": "Toss Win"}, inplace=True)

    fig = px.line(
        toss,
        x="index",
        y=toss.columns,
        labels={"value": "Count", "index": "Teams",
                "variable": "Toss Decision"},
    )
    fig.update_traces(mode="markers+lines")
    return fig


def piPlotTossSeasonStat(working_df):
    tossbi = working_df["toss_decision"].value_counts().reset_index()
    fig = px.pie(
        tossbi,
        values="toss_decision",
        color="index",
        color_discrete_map={"field": "royalblue", "bat": "darkblue"},
    )
    fig.update_traces(textposition="inside", textinfo="percent")
    return fig


# ####################   "Team Wise Analysis",
#
def TeamYearTotalData(ids, team, df2):
    data = 0
    s6 = 0
    s4 = 0
    for id in ids:
        a = df2[(df2["id"] == id) & (
            df2["batting_team"] == team)]["total_runs"]
        data += a.sum()
        s6 += a[a == 6].size
        s4 += a[a == 4].size
    return data, s6, s4


def getRunOfTeamYear(ids, team, df2):
    dates = []
    runs = []
    for id in ids:
        dates.append(
            df2[(df2["id"] == id) & (df2["batting_team"] == team)
                ]["date"].tolist()[0]
        )
        runs.append(
            df2[(df2["id"] == id) & (df2["batting_team"] == team)
                ]["total_runs"].sum()
        )
    temp_df = pd.DataFrame()
    temp_df["Matches"] = dates
    temp_df["Runs"] = runs
    return temp_df


def plotYearTeamWinVSPlayed(ids, idws, team, df2):
    AllMatchesRun = getRunOfTeamYear(ids, team, df2)
    AllMatchesRun.sort_values("Matches", inplace=True)

    WinMatchesRun = getRunOfTeamYear(idws, team, df2)
    WinMatchesRun.sort_values("Matches", inplace=True)
    fig = make_subplots(rows=1, cols=1)

    fig.add_trace(
        go.Scatter(
            x=AllMatchesRun["Matches"].tolist(),
            y=AllMatchesRun["Runs"].tolist(),
            name="Matches Played",
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=WinMatchesRun["Matches"].tolist(),
            y=WinMatchesRun["Runs"].tolist(),
            name="Matches Win",
        ),
        row=1,
        col=1,
    )

    fig.update_layout(
        height=600,
        width=800,
        title_text="Overall Matches Plot",
        xaxis_title="Matches",
        yaxis_title="Runs",
    )
    return fig


def plotYearTeamTopBatsman(ids, team, df2, compair):
    batsman = []
    dates = []
    run = []
    totalRun = []
    for id in ids:
        dates.append(
            df2[(df2["id"] == id) & (df2["batting_team"] == team)
                ]["date"].tolist()[0]
        )
        a = (
            df2[(df2["id"] == id) & (df2["batting_team"] == team)]
            .groupby("batsman")
            .sum()["batsman_runs"]
            .reset_index()
            .sort_values("batsman_runs", ascending=False)
        )
        batsman.append(a.iloc[0]["batsman"])
        run.append(a.iloc[0]["batsman_runs"])
        if compair:
            totalRun.append(
                df2[(df2["id"] == id) & (df2["batting_team"] == team)][
                    "total_runs"
                ].sum()
            )
    temp_df = pd.DataFrame()
    temp_df["Batsman"] = batsman
    temp_df["Matches"] = dates
    temp_df["Run"] = run
    if compair:
        temp_df["Total Run"] = totalRun
    temp_df.sort_values("Matches", inplace=True)

    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(
        go.Scatter(
            x=temp_df["Matches"].tolist(),
            y=temp_df["Run"].tolist(),
            text=temp_df["Batsman"].tolist(),
            hoverinfo=["text", "x", "y"],
            name="Run scored by top player",
        ),
        row=1,
        col=1,
    )
    if compair:
        fig.add_trace(
            go.Scatter(
                x=temp_df["Matches"].tolist(),
                y=temp_df["Total Run"].tolist(),
                name="Total run scored",
            ),
            row=1,
            col=1,
        )
    fig.update_layout(
        height=600,
        width=800,
        title_text="Top performing Batsman",
        xaxis_title="Matches",
        yaxis_title="Runs",
    )

    return fig


def plotYearTeamBowler(ids, team, df2, compair):
    bowler = []
    dates = []
    wickets = []
    totalWicket = []
    for id in ids:
        dates.append(
            df2[(df2["id"] == id) & (df2["bowling_team"] == team)
                ]["date"].tolist()[0]
        )
        a = (
            df2[(df2["id"] == id) & (df2["bowling_team"] == team)]
            .groupby("bowler")
            .sum()["is_wicket"]
            .reset_index()
            .sort_values("is_wicket", ascending=False)
        )
        bowler.append(a.iloc[0]["bowler"])
        wickets.append(a.iloc[0]["is_wicket"])

        if compair:
            totalWicket.append(
                df2[(df2["id"] == id) & (df2["bowling_team"] == team)][
                    "is_wicket"
                ].sum()
            )

    temp_df = pd.DataFrame()
    temp_df["Bowler"] = bowler
    temp_df["Matches"] = dates
    temp_df["Wicket"] = wickets

    if compair:
        temp_df["Total Wicket"] = totalWicket

    temp_df.sort_values("Matches", inplace=True)

    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(
        go.Scatter(
            x=temp_df["Matches"].tolist(),
            y=temp_df["Wicket"].tolist(),
            text=temp_df["Bowler"].tolist(),
            hoverinfo=["text", "x", "y"],
            name="Wickets of Top Bowler",
        ),
        row=1,
        col=1,
    )

    if compair:
        fig.add_trace(
            go.Scatter(
                x=temp_df["Matches"].tolist(),
                y=temp_df["Total Wicket"].tolist(),
                name="Total Wickets",
            ),
            row=1,
            col=1,
        )

    fig.update_layout(
        height=600,
        width=800,
        title_text="Top Performing Bowler",
        xaxis_title="Matches",
        legend_title="Wickets",
    )

    return fig


def plotYearTeam4sN6s(ids, team, df2):
    dates = []
    s4 = []
    s6 = []

    for id in ids:
        flag6 = 0
        flag4 = 0
        dates.append(
            df2[(df2["id"] == id) & (df2["batting_team"] == team)
                ]["date"].tolist()[0]
        )
        x = (
            df2[(df2["id"] == id) & (df2["batting_team"] == team)]["batsman_runs"]
            .value_counts()
            .reset_index()
        )

        for el in x["index"] == 4:
            if el:
                flag4 = 1
                s4.append(x[x["index"] == 4]["batsman_runs"].tolist()[0])
                break
        if flag4 == 0:
            s4.append(0)

        for el in x["index"] == 6:
            if el:
                flag6 = 1
                s6.append(x[x["index"] == 6]["batsman_runs"].tolist()[0])
                break
        if flag6 == 0:
            s6.append(0)

    temp_df = pd.DataFrame()
    temp_df["Matches"] = dates
    temp_df["4s"] = s4
    temp_df["6s"] = s6
    temp_df.sort_values("Matches", inplace=True)
    fig = make_subplots(rows=1, cols=1)

    fig.add_trace(
        go.Scatter(x=temp_df["Matches"].tolist(),
                   name="6's", y=temp_df["6s"].tolist()),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(x=temp_df["Matches"].tolist(),
                   name="4's", y=temp_df["4s"].tolist()),
        row=1,
        col=1,
    )
    fig.update_layout(
        height=600,
        width=800,
        title_text="Runs Distribution",
        xaxis_title="Matches",
        legend_title="Boundaries",
    )
    return fig


def plotYearTeamRunDistribution(year, team, df2):
    a = (
        df2[(df2["year"] == year) & (df2["batting_team"] == team)]["batsman_runs"]
        .value_counts()
        .reset_index()
    )
    a.sort_values("index", inplace=True)
    a.drop(0, inplace=True)

    fig = px.pie(
        a,
        names=["Singels", "Doubles", "Triple", "4's", "6's"],
        values="batsman_runs",
        color="index",
        color_discrete_map={1: "lightcyan",
                            2: "cyan", 4: "royalblue", 6: "darkblue"},
    )
    fig.update_traces(textposition="inside", textinfo="label+percent")
    return fig


def plotYearTeamOverWiseBoxplot(ids, team, df2):
    df = pd.DataFrame()
    df["over"] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                  10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

    for id in ids:
        date = df2[(df2["id"] == id) & (df2["batting_team"] == team)]["date"].tolist()[
            0
        ]
        k = (
            df2[(df2["id"] == id) & (df2["batting_team"] == team)]
            .groupby("over")
            .sum()
            .reset_index()[["over", "total_runs"]]
        )
        k.rename(columns={"total_runs": date}, inplace=True)
        df = df.merge(k, how="left", on="over")

    fig = px.box(
        df,
        labels={
            "value": "Overs",
            "variable": "Matches",
        },
    )
    fig.update_layout(title_text="Over wise Box plot of all matches of season")
    fig.update_layout(height=600, width=800)
    df.drop("over", axis=1, inplace=True)
    fig2, ax = plt.subplots(figsize=(17, 17))
    ax = sns.heatmap(df, cmap="Blues", annot=True)
    fig2
    return fig, fig2


# ################   "Match Wise Analysis"
#
def yearTeamToDate(working_df, team):
    return working_df[(working_df["team1"] == team) | (working_df["team2"] == team)][
        "date"
    ].tolist()


def matchData(Match, working_df):
    temp = working_df[working_df["date"] == Match]

    return dict(
        ID=temp["id"].iloc[0],
        team1=temp["team1"].iloc[0],
        team2=temp["team2"].iloc[0],
        tossWinner=temp["toss_winner"].iloc[0],
        tossDecision=temp["toss_decision"].iloc[0],
        winner=temp["winner"].iloc[0],
        playerOfMatch=temp["player_of_match"].iloc[0],
        umpire1=temp["umpire1"].iloc[0],
        umpire2=temp["umpire2"].iloc[0],
        city=temp["city"].iloc[0],
        venue=temp["venue"].iloc[0],
    )


def teamMatchstrikers(ID, team, df2):
    a = df2[df2["id"] == ID]
    x = a[a["batting_team"] == team]["non_striker"]
    y = a[a["batting_team"] == team]["batsman"]
    x.append(y)
    striker = x.unique().tolist()
    return striker


def teamMatchBowler(ID, team, df2):
    a = df2[df2["id"] == ID]
    x = a[a["bowling_team"] == team]["bowler"]
    Bowler = x.unique().tolist()
    return Bowler


def plotMatchbattingRuns(ID, team, df2):
    a = df2[df2["id"] == ID]
    y = a[a["batting_team"] == team]["batsman"].unique().tolist()
    runs = []

    for bat in y:
        runs.append(a[a["batsman"] == bat]["batsman_runs"].sum())
    temp_df = pd.DataFrame()
    temp_df["Batsman"] = y
    temp_df["Runs"] = runs
    fig = px.line(temp_df, x="Batsman", y="Runs")
    fig.update_layout(height=600, width=900)
    fig.update_traces(mode="markers+lines")

    return fig


def plotMatchOverRun(ID, team, df2):
    a = (
        df2[(df2["id"] == ID) & (df2["batting_team"] == team)]
        .groupby("over")
        .sum()["total_runs"]
        .reset_index()
    )
    a["over"] = a["over"].apply(lambda x: x + 1)

    fig = px.bar(
        a,
        x="over",
        y="total_runs",
        labels={"total_runs": "Runs"},
        title=team + ": Runs Vs Overs",
    )
    fig.update_layout(height=600, width=900)
    return fig


def plotMatchOverRunBar(MatchData, df2):
    a = (
        df2[
            (df2["id"] == MatchData["ID"]) & (
                df2["batting_team"] == MatchData["team1"])
        ]
        .groupby("over")
        .sum()["total_runs"]
        .reset_index()
    )
    a["over"] = a["over"].apply(lambda x: x + 1)

    b = (
        df2[
            (df2["id"] == MatchData["ID"]) & (
                df2["batting_team"] == MatchData["team2"])
        ]
        .groupby("over")
        .sum()["total_runs"]
        .reset_index()
    )
    b["over"] = a["over"].apply(lambda x: x + 1)

    fig = make_subplots(rows=1, cols=1)

    fig.add_trace(go.Bar(x=a["over"], y=a["total_runs"]), row=1, col=1)

    fig.add_trace(go.Bar(x=b["over"], y=b["total_runs"]), row=1, col=1)
    fig.update_layout(height=600, width=900)
    #     fig = px.bar(a, x='over', y='total_runs',labels={'total_runs':"Runs"},title=team + ": Runs Vs Overs")
    return fig


def plotMatchOverRunLine(MatchData, df2):
    a = (
        df2[
            (df2["id"] == MatchData["ID"]) & (
                df2["batting_team"] == MatchData["team1"])
        ]
        .groupby("over")
        .sum()["total_runs"]
        .reset_index()
    )
    a["over"] = a["over"].apply(lambda x: x + 1)

    b = (
        df2[
            (df2["id"] == MatchData["ID"]) & (
                df2["batting_team"] == MatchData["team2"])
        ]
        .groupby("over")
        .sum()["total_runs"]
        .reset_index()
    )
    b["over"] = a["over"].apply(lambda x: x + 1)

    a = a.merge(b, how="left", on="over")
    a.rename(
        columns={
            "over": "Over",
            "total_runs_x": MatchData["team1"],
            "total_runs_y": MatchData["team2"],
        },
        inplace=True,
    )

    fig = px.line(a, x="Over", y=a.columns, labels={
                  "value": "Runs", "varible": "Team"})
    fig.update_layout(height=600, width=900)
    fig.update_traces(mode="markers+lines")
    return fig


def plotMatchRate(MatchData, df2):
    a = df2[
        (df2["id"] == MatchData["ID"]) & (
            df2["batting_team"] == MatchData["team1"])
    ]
    a["ball"] = 1
    a = a.groupby("batsman").sum().reset_index()[
        ["batsman", "ball", "batsman_runs"]]

    a["Rate"] = (a["batsman_runs"] / (a["ball"] / 6)) * 50

    a["Team"] = MatchData["team1"]

    b = df2[
        (df2["id"] == MatchData["ID"]) & (
            df2["batting_team"] == MatchData["team2"])
    ]
    b["ball"] = 1
    b = b.groupby("batsman").sum().reset_index()[
        ["batsman", "ball", "batsman_runs"]]

    b["Rate"] = (b["batsman_runs"] / (b["ball"] / 6)) * 50

    b["Team"] = MatchData["team2"]

    a = pd.concat([a, b])
    a.rename(
        columns={"batsman_runs": "Batsman Runs", "batsman": "Batsman"}, inplace=True
    )

    fig = px.scatter(
        a,
        x="Batsman",
        y="Batsman Runs",
        size="Rate",
        color="Team",
        hover_name="Batsman",
        size_max=60,
        title="Run Rate",
    )
    fig.update_layout(height=600, width=900)
    return fig


def plotBatsmanRunWithbowler(working_df2, Batsman):
    temp = working_df2.groupby("bowler").sum()
    temp.reset_index(inplace=True)
    temp.sort_values("batsman_runs", inplace=True, ascending=False)
    temp = temp[["bowler", "batsman_runs"]]

    fig = px.bar(temp, x='bowler', y='batsman_runs', text='batsman_runs',
                 title="{} vs Bowlers".format(Batsman))
    fig.update_layout(height=600, width=900)
    return fig


def plotRunSeason(working_df2, Batsman):
    temp = working_df2.groupby("year").sum()
    temp.reset_index(inplace=True)
    temp = temp[["year", "batsman_runs"]]

    fig = px.bar(temp, x='year', y='batsman_runs', text='batsman_runs',
                 title="{} vs Season".format(Batsman))
    fig.update_layout(height=600, width=900)
    return fig


def plotRunMatch(working_df2, Batsman, year, df):
    temp = working_df2.groupby("id").sum()
    temp.reset_index(inplace=True)
    temp = temp[["id", "batsman_runs"]]
    temp_df = df[df['year'] == year][['id', "date", "team1", "team2"]]
    temp = pd.merge(temp, temp_df, on='id', how='inner')
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Bar(
        x=temp["date"],
        y=temp["batsman_runs"],
        hovertemplate='%{text}' +
        '<br>Matche: %{x}<br>' +
        'Runs: %{y}<br>',
        text=temp["team1"] + "  VS  "+temp["team2"],
    ))
    fig.update_layout(height=600, width=900)
    return fig


def PlotPlayers6ands4(working_df2, year):
    ys6 = []
    ys4 = []

    for ye in year:
        ys6.append(working_df2[(working_df2['year'] == ye) & (
            working_df2['batsman_runs'] == 6)].shape[0])
        ys4.append(working_df2[(working_df2['year'] == ye) & (
            working_df2['batsman_runs'] == 4)].shape[0])

    temp_df = pd.DataFrame()
    temp_df["Year"] = year
    temp_df["6's"] = ys6
    temp_df["4's"] = ys4

    fig = px.line(
        temp_df,
        x="Year",
        y=["4's", "6's"],
        labels={"value": "Count", 'variable': 'Boundaries'},
    )
    fig.update_layout(height=600, width=900)
    fig.update_traces(mode="markers+lines")
    return fig
