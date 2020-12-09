library(magrittr) 
library(dplyr) 
library(tidyverse)
options(warn=-1)

tidy_districts <- function(districts){
  districts2 <- districts %>%
    separate(municipality_info, c("num_municipality_with_population_<500", "num_municipality_with_population_500-1999", "num_municipality_with_population_2000-9999", "num_municipality_with_population_>10000"), ",") 
  districts2$`num_municipality_with_population_<500` <- as.numeric(str_sub(districts2$`num_municipality_with_population_<500`, start=2))
  districts2$`num_municipality_with_population_>10000` <- as.numeric(str_sub(districts2$`num_municipality_with_population_>10000`, end=1))
  
  districts3 <- districts2 %>%
    separate(unemployment_rate, c("unemployment_rate_95", "unemployment_rate_96"), ",")
  districts3$unemployment_rate_95 <- as.numeric(str_sub(districts3$unemployment_rate_95, start=2))
  districts3$unemployment_rate_96 <- as.numeric(str_sub(districts3$unemployment_rate_96, end=-2))
  
  districts4 <- districts3 %>%
    separate(commited_crimes, c("crime_rate_95", "crime_rate_96"), ",")
  districts4$crime_rate_95 <- as.numeric(str_sub(districts4$crime_rate_95, start=2))
  districts4$crime_rate_96 <- as.numeric(str_sub(districts4$crime_rate_96, end=-2))
  districts4$`num_municipality_with_population_500-1999` <- as.numeric(districts4$`num_municipality_with_population_500-1999`)
  districts4$`num_municipality_with_population_2000-9999` <- as.numeric(districts4$`num_municipality_with_population_2000-9999`)
  write.csv(districts4, "district_r.csv")
  return(districts4)
}

main <- function(){
  districts <- read.csv("data/districts.csv")
  tidy_districts(districts)
}

if (!interactive()) {
  main()
}