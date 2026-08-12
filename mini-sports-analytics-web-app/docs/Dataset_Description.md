# Dataset_Description

# Dataset Description: 2022 FIFA World Cup Matches

## Overview

This dataset contains the complete match-by-match record of the **2022 FIFA World Cup**, held in Qatar. It covers all **64 matches** played across the tournament, from the Group Stage (November 20, 2022) through the Final (December 18, 2022).

- **File name:** `matches.csv`
- **Number of records (rows):** 64
- **Number of features (columns):** 10
- **Missing values:** None (all fields fully populated)
- **Time span:** November 20, 2022 – December 18, 2022

## Features

| # | Column | Type | Description |
| --- | --- | --- | --- |
| 1 | `year` | Integer | Year the tournament was held (constant: 2022) |
| 2 | `date` | Date (MM/DD/YYYY) | Date the match was played |
| 3 | `stage` | Categorical | Tournament stage: Group, Round of 16, Quarter-final, Semi-final, Third Place Play-off, Final |
| 4 | `stadium` | Categorical | Name of the stadium where the match was hosted |
| 5 | `city` | Categorical | City in Qatar where the stadium is located |
| 6 | `home_team` | Categorical | Team listed as the "home" side for the match |
| 7 | `away_team` | Categorical | Team listed as the "away" side for the match |
| 8 | `home_score` | Integer | Number of goals scored by the home team |
| 9 | `away_score` | Integer | Number of goals scored by the away team |
| 10 | `result` | Categorical | Outcome of the match — winning team's name, or "Draw" if tied |

## Summary Statistics

**Matches per stage:**

| Stage | Matches |
| --- | --- |
| Group | 48 |
| Round of 16 | 8 |
| Quarter-final | 4 |
| Semi-final | 2 |
| Third Place Play-off | 1 |
| Final | 1 |

**Matches per stadium:**

| Stadium | Matches |
| --- | --- |
| Al Bayt Stadium | 11 |
| Lusail Stadium | 10 |
| Khalifa International Stadium | 8 |
| Ahmad Bin Ali Stadium | 6 |
| Education City Stadium | 7 |
| Al Janoub Stadium | 7 |
| Al Thumama Stadium | 7 |
| 974 Stadium | 7 |
| Al Rayyan Stadium | 1 |

**Cities represented:** Al Khor, Doha, Al Rayyan, Al Wakrah, Lusail (5 cities)

**Teams:** 32 national teams participated — Argentina, Australia, Belgium, Brazil, Cameroon, Canada, Costa Rica, Croatia, Denmark, Ecuador, England, France, Germany, Ghana, Iran, Japan, Mexico, Morocco, Netherlands, Poland, Portugal, Qatar, Saudi Arabia, Senegal, Serbia, South Korea, Spain, Switzerland, Tunisia, USA, Uruguay, Wales.

**Champion:** Argentina (won the Final 3–3 against France, decided on penalties, per the `result` field showing Argentina as winner).

**Runner-up:** France

**Third place:** Croatia (beat Morocco 2–1 in the Third Place Play-off)

## Full Dataset

| Year | Date | Stage | Stadium | City | Home Team | Away Team | Home Score | Away Score | Result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2022 | 11/20/2022 | Group | Al Bayt Stadium | Al Khor | Qatar | Ecuador | 0 | 2 | Ecuador |
| 2022 | 11/21/2022 | Group | Khalifa International Stadium | Doha | England | Iran | 6 | 2 | England |
| 2022 | 11/21/2022 | Group | Ahmad Bin Ali Stadium | Al Rayyan | Senegal | Netherlands | 0 | 2 | Netherlands |
| 2022 | 11/21/2022 | Group | Al Rayyan Stadium | Al Rayyan | USA | Wales | 1 | 1 | Draw |
| 2022 | 11/22/2022 | Group | Lusail Stadium | Lusail | Argentina | Saudi Arabia | 1 | 2 | Saudi Arabia |
| 2022 | 11/22/2022 | Group | Education City Stadium | Al Rayyan | Mexico | Poland | 0 | 0 | Draw |
| 2022 | 11/22/2022 | Group | Al Janoub Stadium | Al Wakrah | Denmark | Tunisia | 0 | 0 | Draw |
| 2022 | 11/22/2022 | Group | Al Bayt Stadium | Al Khor | France | Australia | 4 | 1 | France |
| 2022 | 11/23/2022 | Group | Khalifa International Stadium | Doha | Germany | Japan | 1 | 2 | Japan |
| 2022 | 11/23/2022 | Group | Al Thumama Stadium | Doha | Spain | Costa Rica | 7 | 0 | Spain |
| 2022 | 11/23/2022 | Group | Al Janoub Stadium | Al Wakrah | Morocco | Croatia | 0 | 0 | Draw |
| 2022 | 11/23/2022 | Group | Ahmad Bin Ali Stadium | Al Rayyan | Belgium | Canada | 1 | 0 | Belgium |
| 2022 | 11/24/2022 | Group | Lusail Stadium | Lusail | Switzerland | Cameroon | 1 | 0 | Switzerland |
| 2022 | 11/24/2022 | Group | Al Thumama Stadium | Doha | Uruguay | South Korea | 0 | 0 | Draw |
| 2022 | 11/24/2022 | Group | 974 Stadium | Doha | Portugal | Ghana | 3 | 2 | Portugal |
| 2022 | 11/24/2022 | Group | Education City Stadium | Al Rayyan | Brazil | Serbia | 2 | 0 | Brazil |
| 2022 | 11/25/2022 | Group | 974 Stadium | Doha | Wales | Iran | 0 | 2 | Iran |
| 2022 | 11/25/2022 | Group | Al Bayt Stadium | Al Khor | Qatar | Senegal | 0 | 3 | Senegal |
| 2022 | 11/25/2022 | Group | Al Thumama Stadium | Doha | Netherlands | Ecuador | 1 | 1 | Draw |
| 2022 | 11/25/2022 | Group | Khalifa International Stadium | Doha | England | USA | 0 | 0 | Draw |
| 2022 | 11/26/2022 | Group | Education City Stadium | Al Rayyan | Poland | Saudi Arabia | 2 | 0 | Poland |
| 2022 | 11/26/2022 | Group | Lusail Stadium | Lusail | Argentina | Mexico | 2 | 0 | Argentina |
| 2022 | 11/26/2022 | Group | Al Janoub Stadium | Al Wakrah | Tunisia | Australia | 0 | 1 | Australia |
| 2022 | 11/26/2022 | Group | Al Bayt Stadium | Al Khor | France | Denmark | 2 | 1 | France |
| 2022 | 11/27/2022 | Group | Ahmad Bin Ali Stadium | Al Rayyan | Japan | Costa Rica | 0 | 1 | Costa Rica |
| 2022 | 11/27/2022 | Group | Al Bayt Stadium | Al Khor | Belgium | Morocco | 0 | 2 | Morocco |
| 2022 | 11/27/2022 | Group | 974 Stadium | Doha | Croatia | Canada | 4 | 1 | Croatia |
| 2022 | 11/27/2022 | Group | Al Thumama Stadium | Doha | Spain | Germany | 1 | 1 | Draw |
| 2022 | 11/28/2022 | Group | Al Janoub Stadium | Al Wakrah | Cameroon | Serbia | 3 | 3 | Draw |
| 2022 | 11/28/2022 | Group | Lusail Stadium | Lusail | South Korea | Ghana | 2 | 3 | Ghana |
| 2022 | 11/28/2022 | Group | Education City Stadium | Al Rayyan | Brazil | Switzerland | 1 | 0 | Brazil |
| 2022 | 11/28/2022 | Group | Khalifa International Stadium | Doha | Portugal | Uruguay | 2 | 0 | Portugal |
| 2022 | 11/29/2022 | Group | Khalifa International Stadium | Doha | Netherlands | Qatar | 2 | 0 | Netherlands |
| 2022 | 11/29/2022 | Group | Al Thumama Stadium | Doha | Ecuador | Senegal | 1 | 2 | Senegal |
| 2022 | 11/29/2022 | Group | Ahmad Bin Ali Stadium | Al Rayyan | Wales | England | 0 | 3 | England |
| 2022 | 11/29/2022 | Group | Al Bayt Stadium | Al Khor | Iran | USA | 0 | 1 | USA |
| 2022 | 11/30/2022 | Group | Al Janoub Stadium | Al Wakrah | Australia | Denmark | 1 | 0 | Australia |
| 2022 | 11/30/2022 | Group | 974 Stadium | Doha | Tunisia | France | 1 | 0 | Tunisia |
| 2022 | 11/30/2022 | Group | Lusail Stadium | Lusail | Poland | Argentina | 0 | 2 | Argentina |
| 2022 | 11/30/2022 | Group | Education City Stadium | Al Rayyan | Saudi Arabia | Mexico | 1 | 2 | Mexico |
| 2022 | 12/1/2022 | Group | Al Bayt Stadium | Al Khor | Croatia | Belgium | 0 | 0 | Draw |
| 2022 | 12/1/2022 | Group | Khalifa International Stadium | Doha | Canada | Morocco | 1 | 2 | Morocco |
| 2022 | 12/1/2022 | Group | Al Thumama Stadium | Doha | Japan | Spain | 2 | 1 | Japan |
| 2022 | 12/1/2022 | Group | Ahmad Bin Ali Stadium | Al Rayyan | Costa Rica | Germany | 2 | 4 | Germany |
| 2022 | 12/2/2022 | Group | Lusail Stadium | Lusail | South Korea | Portugal | 2 | 1 | South Korea |
| 2022 | 12/2/2022 | Group | Al Janoub Stadium | Al Wakrah | Ghana | Uruguay | 0 | 2 | Uruguay |
| 2022 | 12/2/2022 | Group | Al Bayt Stadium | Al Khor | Cameroon | Brazil | 1 | 0 | Cameroon |
| 2022 | 12/2/2022 | Group | 974 Stadium | Doha | Serbia | Switzerland | 2 | 3 | Switzerland |
| 2022 | 12/3/2022 | Round of 16 | 974 Stadium | Doha | Netherlands | USA | 3 | 1 | Netherlands |
| 2022 | 12/3/2022 | Round of 16 | Khalifa International Stadium | Doha | Argentina | Australia | 2 | 1 | Argentina |
| 2022 | 12/4/2022 | Round of 16 | Al Bayt Stadium | Al Khor | France | Poland | 3 | 1 | France |
| 2022 | 12/4/2022 | Round of 16 | Ahmad Bin Ali Stadium | Al Rayyan | England | Senegal | 3 | 0 | England |
| 2022 | 12/5/2022 | Round of 16 | Al Janoub Stadium | Al Wakrah | Japan | Croatia | 1 | 1 | Croatia |
| 2022 | 12/5/2022 | Round of 16 | 974 Stadium | Doha | Brazil | South Korea | 4 | 1 | Brazil |
| 2022 | 12/6/2022 | Round of 16 | Education City Stadium | Al Rayyan | Morocco | Spain | 0 | 0 | Morocco |
| 2022 | 12/6/2022 | Round of 16 | Lusail Stadium | Lusail | Portugal | Switzerland | 6 | 1 | Portugal |
| 2022 | 12/9/2022 | Quarter-final | Education City Stadium | Al Rayyan | Croatia | Brazil | 1 | 1 | Croatia |
| 2022 | 12/9/2022 | Quarter-final | Lusail Stadium | Lusail | Netherlands | Argentina | 2 | 2 | Argentina |
| 2022 | 12/10/2022 | Quarter-final | Al Thumama Stadium | Doha | Morocco | Portugal | 1 | 0 | Morocco |
| 2022 | 12/10/2022 | Quarter-final | Al Bayt Stadium | Al Khor | England | France | 1 | 2 | France |
| 2022 | 12/13/2022 | Semi-final | Lusail Stadium | Lusail | Argentina | Croatia | 3 | 0 | Argentina |
| 2022 | 12/14/2022 | Semi-final | Al Bayt Stadium | Al Khor | France | Morocco | 2 | 0 | France |
| 2022 | 12/17/2022 | Third Place Play-off | Khalifa International Stadium | Doha | Croatia | Morocco | 2 | 1 | Croatia |
| 2022 | 12/18/2022 | Final | Lusail Stadium | Lusail | Argentina | France | 3 | 3 | Argentina |

*Note: Some knockout-stage matches (including the Final) were decided by penalty shootouts after the score above ended in a draw; the `result` column reflects the overall match winner rather than the 90-minute regulation score in those cases.*