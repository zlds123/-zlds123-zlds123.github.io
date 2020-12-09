library(magrittr) 
library(dplyr) 
library(tidyverse)
library(reshape)
options(warn=-1)

tidy_loans <- function(loans){
  non_status_fields = c('id', 'account_id', 'date', 'amount', 'payments')
  status_fields = setdiff(colnames(loans), non_status_fields)
  binary_status_fields = loans %>% select(status_fields)
  new_binary <- binary_status_fields %>% 
    mutate_all(funs(str_replace(., "X", "1"))) %>%
    mutate_all(funs(str_replace(., "-", "0")))
  loans2 <- cbind(loans %>% select(non_status_fields), as.data.frame(sapply(new_binary, as.numeric)) )
  loans3 <- melt(loans2, id = non_status_fields) %>% filter(value == 1)
  loans4 <- loans3 %>%
    separate(variable, c("term", "status"), "_") %>%
    separate(term, c("todrop", "term"), "X") 
  loans4$active_status <- ifelse(loans4$status %in% c("A", "B") , "expired", "current")
  loans4$payment <- ifelse(loans4$status %in% c("B", "D"), "default", ifelse(loans4$status == "A", "full", "in_progress"))
  loans4 %>% select(c(non_status_fields, "term", "active_status", "payment"))
  write.csv(loans4, "loans_r.csv")
  return(loans4)
}

main <- function(){
  loans = read.csv('./data/loans.csv')
  tidy_loans(loans)
}

if (!interactive()) {
  main()
}