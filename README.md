# Major League Baseball - Statistical Analysis and Predictions 

![Well, how can you not be romantic about baseball?](https://media.giphy.com/media/13kzikBxzyRaRG/giphy.gif)

## Motivation and Process Overview 

Baseball is many things. It's an immensely popular professional sport, a [convenient metaphor](https://deadspin.com/baseball-is-the-horniest-sport-1809943124) for uncomfortable conversations, and perhaps above all else, it's quintessentially American. For some, it conjures nostalgic images of a shared history with its country of origin or childhood daydreams of glory.  It can remind us of who we used to be. But for me, baseball represents a vision of what America could be. A world in which we take [care of our own](https://benefitsbclp.com/major-league-baseball-pension-and-healthcare-benefits/), where respect and hard work are acknowledged and rewarded, diversity is celebrated, and [cheaters never prosper](https://www.usatoday.com/story/sports/mlb/astros/2020/01/13/astros-stealing-signs-penalties-jeff-luhnow-aj-hinch-suspended-year/4456644002/).

It's also a hotbed for [statistical analysis](https://en.wikipedia.org/wiki/Baseball_statistics). *The Baseball Encyclopedia*, published in 1969, was one of the earliest examples of coding and computer software in book publishing. It was the first book to use computer typesetting besides besides the phone book. In those days, every player's data were individually compiled on sheets of paper, coded into punch cards, and sorted by an IBM 360. The results were totaled, combined, and compared with official records. Inconsistencies were flagged by the computer for further investigation. 

For this project, we'll perform a similar process for our analyses. Instead of using punch cards and magnetic tape, we'll use Python and the [SQLAlchemy ORM framework](https://docs.sqlalchemy.org/en/13/orm/index.html) for storing and accessing data gathered from the MLB API, explore our data with visualizations in Plotly, and perform statistical analysis with Pandas and scikit-learn. 


### MLB Stats API and SQLAlchemy ORM
The MLB stats API returns an exceptional amount of information for every game. The first and most substantial part of this project was parsing the information from a single game's API into a normalized database. The work was worth it because storing this information systematically means that I don't have to return to the API to perform my analysis, and I'll have the information ready for future projects. 

Our database allows us to store and retrieve comprehensive data on games, players, teams, team records, pitches, plays, runners, and the relationships between them. In it's current form, the database stores this information in 17 different tables.

The SQL Alchemy ORM framework facilitates a connection between Python objects and SQL records. 

## Statistical Modeling

### Predicting Game Winners

![Branch Rickey. Life Magazine, 1954](images/Rickey_obp.jpg)

In 
### Predicting the Next Pitch 
