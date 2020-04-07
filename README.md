# Pandemic Simulation 🦠

This project allows us to run highly customizable small scale simulation of a pandemic. By tweaking the parameters of the simulation, we can better understands what affects the spread of the infection, and what policies can be put in place to slow down the pandemic.
All results are graphed and important metrics reported.

This simulation was inspired by Grant Sanderson's [youtube video](https://www.youtube.com/watch?v=gxAaO2rsdIs&t=) from the channel [3Blue1Brown](https://www.3blue1brown.com/) with modifications that I wanted to explore.

**Disclamer:** I am not an epidemiologist in any way 

## The Simulation Setup

The simulation is made up with several communities with people living in each of these communities. Within these communities, families and friend groups are modelled by increasing their likelyhood to interact compared to two total strangers.

The simulation starts with a few people being infected in one of the communities. People can travel between communities and potentially spread the infection to the other communities. In order to travel, people have to pass by "Travel Hubs" that increase the chance of interacting with others because of the close proximity.

The simulation also supports the idea of public spaces, these can be thought of as grocery stores. The particularity of these public places, is that the chance to interact with other people is increased (due to the close proximity), which increases the chance of getting in contact with someone that is infected

<p align="center">
  <img src="img/simulation.png" width="700" />
</p>

### Basic Parameters

The basic parameters that can be configured in the simulation are:

- The number of communities
- The population of each community
- The average incubation time of the infection
- The average time people take to recover after starting to show symptoms
- The number days it takes to infect someone else on average
- The frequency of travel between communities
- The frequency and time spent on trips to public places

**Note:** all these parameters can be highly customized such as "80% of the population will travel between communities on average every 40 days with a standard deviation of 10 days and the remaining 20% of the population never travel"

### Policies

Policies that can be put into place in order to slow down the pandemic are:


