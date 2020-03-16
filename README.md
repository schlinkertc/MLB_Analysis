# Major League Baseball - Statistical Analysis and Predictions 

![Well, how can you not be romantic about baseball?](https://media.giphy.com/media/13kzikBxzyRaRG/giphy.gif)

## Motivation and Process Overview 

Baseball is many things. It's an immensely popular professional sport, a [convenient metaphor](https://deadspin.com/baseball-is-the-horniest-sport-1809943124) for uncomfortable conversations, and perhaps above all else, it's quintessentially American. For some, it conjures nostalgic images of a shared history with its country of origin or childhood daydreams of glory.  It can remind us of who we used to be. But for me, baseball represents a vision of what America could be. A world in which we take [care of our own](https://benefitsbclp.com/major-league-baseball-pension-and-healthcare-benefits/), where respect and hard work are acknowledged and rewarded, diversity is celebrated, and [cheaters never prosper](https://www.usatoday.com/story/sports/mlb/astros/2020/01/13/astros-stealing-signs-penalties-jeff-luhnow-aj-hinch-suspended-year/4456644002/).

It's also a hotbed for [statistical analysis](https://en.wikipedia.org/wiki/Baseball_statistics). *The Baseball Encyclopedia*, published in 1969, was one of the earliest examples of coding and computer software in book publishing. It was the first book to use computer typesetting besides besides the phone book. In those days, every player's data were individually compiled on sheets of paper, coded into punch cards, and sorted by an IBM 360. The results were totaled, combined, and compared with official records. Inconsistencies were flagged by the computer for further investigation. 

For this project, we'll perform a similar process for our analyses. Instead of using punch cards and magnetic tape, we'll use Python and the [SQLAlchemy ORM framework](https://docs.sqlalchemy.org/en/13/orm/index.html) for storing and accessing data gathered from the MLB API, explore our data with visualizations in Plotly, and perform statistical analysis with Pandas and scikit-learn. 


## MLB Stats API and SQLAlchemy ORM
*explain how and why we build the RDB*

## Statistical Testing

### One-Sample T-test

The Houston Astros have been caught cheating, and the baseball world is angry. When rules are broken in basball, opposing players will often retaliate by sending an unspoken message: they hit the batters with a pitch. So far, the in-game fallout from the Astros cheating scandal has only taken place in spring training of the 2020 season. We'll run a one-sample t-test to determine whether Astros players have been unusually targeted by opposing pitchers. 

#### Questions to Consider: How can we tell if a batter was hit on purpose? 
- If I was going to send a message by hitting a batter, I'd probably do it on the first pitch, and that pitch would be a little softer than a competitive fastball. Maybe we can use these assumptions to determine wheter batters were purposefully targeted or if the pitcher just made a mistake. 
- If this pitcher has a tendency to throw innacurately, there's a better chance there was no intended retaliatory message. 

### Analysis of Variance in Different Stadiums

The Colorado Rockies play their home games at Coors Field where the altitude is higher than any other stadium in professional baseball. This has a [dramatic effect](http://baseball.physics.illinois.edu/Denver.html) on the aerodynamic forces that influence trajectory of hit baseballs. It's known as the "Coors Field Effect". We'll use ANOVA tests to show this effect. 

## Statistical Modeling

### Predicting Game Winners

![Branch Rickey. Life Magazine, 1954](images/Rickey_obp.jpg)


### Predicting the Next Pitch 
