# Dilemma Rock Paper Scissors
Dilemma Rock Paper Scissors: A Simple Game with Deep Layers
This but robust implementation of DRPS in Python for use with mostly AI stuff, with support for multi (3+) agent play sessions for training in a context with social play to allow for exploration strategy around kingmaking and other social play.

This game brings complex game theory concepts into a simple format of Rock, Paper, Scissors meets the Prisoner's Dilemma. The simplicity of the rules coupled with strategic depth makes it an excellent testbed for AI research and development. Enjoy playing the game or dive into building AI strategies with this open-source project.

## Game Rules

The goal of Dilemma RPS is to gather the most chips by using Rock, Paper, Scissors, Cooperate, Betray, and Block moves strategically. Each player starts with their own pool of chips and a central communal pot is created. Games happen between pairs of players who engage in a series of RPS matches until there's a cooperation, a double betrayal, or a tie, with the exception of a tie resulting from a blocked betrayal. The session ends when a player folds, after a cooperation, or upon table agreement. The player with the most chips at the end wins.

## License
Dilemma RPS is available under the MIT license. See the LICENSE file for more info.
