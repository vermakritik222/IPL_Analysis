import streamlit as st
import pandas as pd
import preprocessor
import controller


df = pd.read_csv("IPL Matches 2008-2020.csv")
df2 = pd.read_csv("IPL Ball-by-Ball 2008-2020.csv")

df, df2 = preprocessor.process(df, df2)

st.sidebar.title("IPL Analysis (2008-2020)")
# st.sidebar.image("./Logo.png")
menu_bar = st.sidebar.radio(
    "Select an Option",
    (
        "Overall Analysis",
        "Season Wise Analysis",
        "Team Wise Analysis",
        "Match Wise Analysis",
        "Player Wise Analysis",
    ),
)

if menu_bar == "Overall Analysis":
    st.title("Overall Analysis (2008-2020)")
    st.header("Season wise winers of IPL")
    allYear = controller.AllYears(df)
    allTeams = controller.AllTeams(df)
    plot01, TeamsWin = controller.plotOverallYearsWiseWin(df, allYear)
    st.pyplot(plot01)

    TeamsWin_df = pd.DataFrame()
    TeamsWin_df["Teams"] = TeamsWin
    TeamsWin_df["Season"] = allYear
    allTeams_df = pd.DataFrame()
    allTeams_df["Teams"] = allTeams

    col1, col2 = st.columns(2)
    with col1:
        st.header("Teams Participader")
        st.table(allTeams_df)
    with col2:
        st.header("Winning Teams")
        st.table(TeamsWin_df)

    st.title("Frequency of wining the seasons")
    plot = controller.plotOverallfrequencyOfWining(TeamsWin, allYear)
    st.plotly_chart(plot)

    st.title("Comparision of No. of Matches Played VS No. of Matches Win")
    plot = controller.plotOverallfrequencyOfWinnerNnoOfMatchesPlayed(df)
    st.plotly_chart(plot)

    st.title("Frequency of Matches in Different Cities")
    plot = controller.plotOverallfrequencyOfCities(df)
    st.plotly_chart(plot)

    st.title("Frequency of Matches in Different Stadiums")
    plot = controller.plotOverallfrequencyOfVenue(df)
    st.plotly_chart(plot)

    st.title("Top Players of all time")
    plot = controller.plotOverallTop50PlayersOfAllTime(df)
    st.plotly_chart(plot)

    st.title("Toss Decision per Team")
    plot = controller.plotOverallToss(df)
    st.plotly_chart(plot)

    st.title("Overall Toss Decision")
    plot = controller.pieplotOverallToss(df)
    st.plotly_chart(plot)


# #######################  "Season Wise  Analysis"
if menu_bar == "Season Wise Analysis":
    allYearS = controller.AllYears(df)
    selected_Year = st.sidebar.selectbox("Select Year", allYearS)
    allTeamsS = controller.AllTeamYearWise(df, selected_Year)

    working_df = preprocessor.processSeasonWiseData(df, selected_Year)

    Season_id = working_df["id"].tolist()
    st.error("")
    st.header("Winner Of The Season : Chennai Super Kings")

    # col1, col2, col3 = st.columns(3)
    # with col1:
    #     st.metric(
    #         label="Total Matches Played By Chennai Super Kings",
    #         value=working_df.shape[0],
    #     )
    # with col2:
    #     st.metric(
    #         label="""Total Matches Win By
    #                 Chennai Super Kings""",
    #         value=working_df.shape[0],
    #     )
    # with col3:
    #     st.metric(
    #         label="Total Runs Scored By Chennai Super Kings", value=working_df.shape[0]
    #     )

    st.title("Comparision of No. of Matches Played VS No. of Matches Win")
    plot = controller.plotOverallfrequencyOfWinnerNnoOfMatchesPlayed(
        working_df)
    st.plotly_chart(plot)

    st.title("Frequency of Matches in Different Cities")
    plot = controller.plotOverallfrequencyOfCities(working_df)
    st.plotly_chart(plot)

    st.title("Frequency of Matches in Different Stadiums")
    plot = controller.plotOverallfrequencyOfVenue(working_df)
    st.plotly_chart(plot)

    st.title("Top Players of all time")
    plot = controller.plotOverallTop50PlayersOfAllTime(working_df)
    st.plotly_chart(plot)

    st.title("Top performing Bollers")
    compairWithTWickets = st.selectbox(
        "Select Comparision", ["None", "Compair with total wickets"]
    )
    if compairWithTWickets == "None":
        plot = controller.plotSeasonBowlers(Season_id, df2, False)
    else:
        plot = controller.plotSeasonBowlers(Season_id, df2, True)
    st.plotly_chart(plot)

    st.title("Distribution of 4's and 6's")
    PlotType = st.selectbox(
        "Select Plot Type", ["Line Plot", "Box Plot of 4's", "Box Plot of 6's"]
    )
    if PlotType == "Line Plot":
        plot = controller.plotSeasonalRunDistribution(
            selected_Year, allTeamsS, df2)
        st.plotly_chart(plot)
    elif PlotType == "Box Plot of 4's":
        plot = controller.boxPlotSeasonalRunDistribution(
            allTeamsS, df, df2, "4s")
        st.plotly_chart(plot)
    elif PlotType == "Box Plot of 6's":
        plot = controller.boxPlotSeasonalRunDistribution(
            allTeamsS, df, df2, "6s")
        st.plotly_chart(plot)

    st.title("Over-wise runs distribution of season")
    QuartileMethod = st.selectbox(
        "Select quartile method ", ["linear", "inclusive", "exclusive"]
    )
    plot = controller.plotOverwiseRunDistributionOfSeason(
        allTeamsS, df, df2, QuartileMethod
    )
    st.plotly_chart(plot)

    st.title("Eliminator Rounds")
    (
        eliminatorRounds_df,
        eliminatorRounds_IDs,
    ) = controller.eliminatorRoundsTableOfSeason(working_df)
    st.table(eliminatorRounds_df)

    st.title("Toss statistics of season")
    plot = controller.plotTossSeasonStat(working_df)
    st.plotly_chart(plot)

    st.title("Plot of overall Toss desions")
    plot = controller.piPlotTossSeasonStat(working_df)
    st.plotly_chart(plot)


# #######################   "Team Wise Analysis"
if menu_bar == "Team Wise Analysis":

    allYear = controller.AllYears(df)
    selected_year = st.sidebar.selectbox("Select Year", allYear)
    allTeams = controller.AllTeamYearWise(df, selected_year)
    selected_team = st.sidebar.selectbox("Select team", allTeams)
    st.title(selected_team + " performance in " + str(selected_year))

    YearTeam_df, YearTeam_id = preprocessor.processYearTeamData(
        df, selected_year, selected_team
    )

    YearTeamWin_id = YearTeam_df[YearTeam_df["winner"]
                                 == selected_team]["id"].tolist()

    Total_Matches_Played = YearTeam_df.shape[0]
    Total_Matches_Win = YearTeam_df[YearTeam_df["winner"]
                                    == selected_team].shape[0]
    total, s6, s4 = controller.TeamYearTotalData(
        YearTeamWin_id, selected_team, df2)

    col1, col2 = st.columns(2)
    with col1:
        st.header("Total Matches Played")
        st.title(Total_Matches_Played)
    with col2:
        st.header("Total Matches Win")
        st.title(Total_Matches_Win)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Total Runs")
        st.title(total)
    with col2:
        st.header("Total 4's")
        st.title(s4)
    with col3:
        st.header("Total 6's")
        st.title(s6)

    plot1 = controller.plotYearTeamWinVSPlayed(
        YearTeam_id, YearTeamWin_id, selected_team, df2
    )

    st.plotly_chart(plot1)

    st.title("Top performing Batsman")
    compairWithTRun = st.selectbox(
        "Select Comparision", ["None", "Compair with total runs"]
    )
    if compairWithTRun == "Compair with total runs":
        plot2 = controller.plotYearTeamTopBatsman(
            YearTeam_id, selected_team, df2, True)
    else:
        plot2 = controller.plotYearTeamTopBatsman(
            YearTeam_id, selected_team, df2, False
        )
    st.plotly_chart(plot2)

    st.title("Top performing Bollers")
    compairWithTWickets = st.selectbox(
        "Select Comparision", ["None", "Compair with total wickets"]
    )
    if compairWithTWickets == "None":
        plot3 = controller.plotYearTeamBowler(
            YearTeam_id, selected_team, df2, False)
    else:
        plot3 = controller.plotYearTeamBowler(
            YearTeam_id, selected_team, df2, True)
    st.plotly_chart(plot3)

    st.title("Distribution of 4's and 6's")
    plot4 = controller.plotYearTeam4sN6s(YearTeam_id, selected_team, df2)
    st.plotly_chart(plot4)

    st.title("Run Distribution")
    plot5 = controller.plotYearTeamRunDistribution(
        selected_year, selected_team, df2)
    st.plotly_chart(plot5)

    st.title("Over wise Run Distribution")
    plot6, plot7 = controller.plotYearTeamOverWiseBoxplot(
        YearTeam_id, selected_team, df2
    )
    st.plotly_chart(plot6)

    st.title("Over wise HeatMap of all matches of season")
    st.pyplot(plot7)


# ################   "Match Wise Analysis"
if menu_bar == "Match Wise Analysis":
    st.title("Match Wise Analysis")

    allYear = controller.AllYears(df)
    selected_year = st.sidebar.selectbox("Select Season", allYear)
    allTeams = controller.AllTeamYearWise(df, selected_year)
    selected_team = st.sidebar.selectbox("Select Team", allTeams)

    working_df = preprocessor.processMactheWiseData(df, selected_year)

    Matches = controller.yearTeamToDate(working_df, selected_team)
    selected_match = st.selectbox("Select Matche", Matches)

    MatchData = controller.matchData(selected_match, working_df)

    st.header(MatchData["team1"] + " VS " + MatchData["team2"])
    st.header("Match Details")
    st.markdown("#### Winner of the Match : {}".format(MatchData["winner"]))

    st.markdown(
        """
            | Field's         | Description |
            | --------------- | ----------- |
            | Match id        | {}          |
            | Team 1          | {}          |
            | Team 2          | {}          |
            | Toss Winner     | {}          |
            | Toss Decision   | {}          |
            | Winner          | {}          |
            | Player Of Match | {}          |
            | Umpire 1        | {}          |
            | Umpire 2        | {}          |
            | City            | {}          |
            | Venue           | {}          |

    """.format(
            MatchData["ID"],
            MatchData["team1"],
            MatchData["team2"],
            MatchData["tossWinner"],
            MatchData["tossDecision"],
            MatchData["winner"],
            MatchData["playerOfMatch"],
            MatchData["umpire1"],
            MatchData["umpire2"],
            MatchData["city"],
            MatchData["venue"],
        )
    )

    stricktable1 = controller.teamMatchstrikers(
        MatchData["ID"], MatchData["team1"], df2
    )
    stricktable2 = controller.teamMatchstrikers(
        MatchData["ID"], MatchData["team2"], df2
    )
    bowler1 = controller.teamMatchBowler(
        MatchData["ID"], MatchData["team1"], df2)
    bowler2 = controller.teamMatchBowler(
        MatchData["ID"], MatchData["team2"], df2)

    col1, col2 = st.columns(2)
    with col1:
        st.header(MatchData["team1"])
        st.markdown("##### Team Description")
    with col2:
        st.header(MatchData["team2"])
        st.markdown("##### Team Description")

    colA1, colA2, colA3, colA4 = st.columns(4)

    with colA1:
        team = pd.DataFrame()
        team["strickers"] = stricktable1
        st.table(team)
    with colA2:
        team1 = pd.DataFrame()
        team1["Bollowers"] = bowler1
        st.table(team1)
    with colA3:
        team = pd.DataFrame()
        team["strickers"] = stricktable2
        st.table(team)
    with colA4:
        team1 = pd.DataFrame()
        team1["Bollowers"] = bowler2
        st.table(team1)

    st.header("Plot of runs scored by player's of " + MatchData["team1"])
    fig = controller.plotMatchbattingRuns(
        MatchData["ID"], MatchData["team1"], df2)
    st.plotly_chart(fig)

    st.header("Plot of runs scored by player's of " + MatchData["team2"])
    fig = controller.plotMatchbattingRuns(
        MatchData["ID"], MatchData["team2"], df2)
    st.plotly_chart(fig)

    st.title("Over wise Runs Distribution")
    RunsDistribution__PlotType = st.selectbox(
        "Plot Options",
        ["Line", "Bar"],
    )
    if RunsDistribution__PlotType == "Bar":
        fig = controller.plotMatchOverRunBar(MatchData, df2)
    if RunsDistribution__PlotType == "Line":
        fig = controller.plotMatchOverRunLine(MatchData, df2)

    st.plotly_chart(fig)

    st.title("Runs Rate")
    fig = controller.plotMatchRate(MatchData, df2)
    st.plotly_chart(fig)

# ################   "Player Wise Analysis"
if menu_bar == "Player Wise Analysis":
    allPlayers = controller.AllBatsman(df2)
    Years = controller.AllYears(df)
    selected_Player = st.sidebar.selectbox("Select Player", allPlayers)
    st.title(selected_Player)

    working_df2 = df2[df2["batsman"] == selected_Player]

    IDS = working_df2['id'].unique()
    IDS = IDS.tolist()

    col1, col2, col3 = st.columns(3)
    with col1:
        TotalRunScoredTillNow = working_df2["batsman_runs"].sum()
        st.metric(
            label="Total Run Scored Till Now",
            value=TotalRunScoredTillNow,
        )
    with col2:
        TotalballPlayedTillNow = working_df2.shape[0]
        st.metric(
            label="Total ball Played Till Now",
            value=TotalballPlayedTillNow,
        )
    with col3:
        TotalMatchesTillNow = len(IDS)
        st.metric(
            label="Total Matches Played Till Now", value=TotalMatchesTillNow
        )

    st.title("Batsman Run With bowler")
    plot = controller.plotBatsmanRunWithbowler(
        working_df2, selected_Player)
    st.plotly_chart(plot)

    st.title("Season-Wise Run Distrubution")
    plot = controller.plotRunSeason(
        working_df2, selected_Player)
    st.plotly_chart(plot)

    st.title("Match-Wise Run Distrubution")
    selected_Year = st.selectbox("Select Year", Years)
    plot = controller.plotRunMatch(
        working_df2, selected_Player, selected_Year, df)
    st.plotly_chart(plot)

    st.title("Distribution of 4's and 6's")
    plot = controller.PlotPlayers6ands4(
        working_df2, Years)
    st.plotly_chart(plot)
