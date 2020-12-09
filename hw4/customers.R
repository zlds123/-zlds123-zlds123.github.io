library(magrittr) 
library(dplyr) 
library(tidyverse)
library(reshape)
library(data.table)
source(here::here('loans.R'))

tidy_customers <- function(accounts, districts, links, cards, loans, transactions, payment_orders){
  loans_new <- tidy_loans(loans)
  combined1 <- merge(accounts, districts, all.x=TRUE, by.x = "district_id", by.y = "id")
  setnames(combined1, "id", "account_id")
  setnames(combined1, "name", "district_name")
  setnames(combined1, "date", "open_date")
  combined3 <- merge(cards, links, all.y=TRUE, by.x = "link_id", by.y = "id")
  setnames(combined3, "id", "card_id")
  setnames(combined3, "type.x", "card_type")
  setnames(combined3, "issue_date", "card_issue_date")
  setnames(combined3, "type.y", "customer_type")
  card_account <- combined3 %>%
    group_by(account_id) %>%
    summarise(count = n())
  links_account <- links %>%
    group_by(account_id) %>%
    summarise(num_customers = n())
  combined2 <- merge(combined1, links_account, all.x=TRUE, by.x = "account_id", by.y = "account_id")
  combined4 <- merge(combined2, card_account, all.x=TRUE, by.x='account_id', by.y='account_id')
  setnames(combined4, "count", "credit_cards")
  combined5 <- merge(combined4, loans_new, by.x='account_id', by.y='account_id', all.x =TRUE)
  setnames(combined5, "id", "loan")
  combined5$loan <- ifelse(is.na(combined5$loan), FALSE, TRUE)
  setnames(combined5, "amount", "loan_amount")
  setnames(combined5, "payments", "loan_payments")
  setnames(combined5, "term", "loan_term")
  setnames(combined5, "active_status", "loan_status")
  combined5$loan_default <- ifelse((combined5$payment) == "default", TRUE, ifelse(combined5$payment %in% c("full", "in_progress"), FALSE, NA))
  max_withdrawal <- transactions %>% group_by(account_id) %>% summarize(max = max(amount))
  min_withdrawal <- transactions %>% group_by(account_id) %>% summarize(min = min(amount))
  combined6 <- merge(combined5, max_withdrawal, by.x='account_id', by.y='account_id', all.x=TRUE)
  combined7 <- merge(combined6, min_withdrawal, by.x='account_id', by.y='account_id', all.x=TRUE)
  setnames(combined7, "max", "max_withdrawal")
  setnames(combined7, "min", "min_withdrawal")
  payment_counts = payment_orders %>% group_by(account_id) %>% summarize(cc_payments = n())
  combined8 <- merge(combined7, payment_counts, by.x='account_id', by.y='account_id',all.X=TRUE)
  max_balance <- transactions %>% group_by(account_id) %>% summarize(max_balance = max(balance))
  min_balance <- transactions %>% group_by(account_id) %>% summarize(min_balance = min(balance))
  combined9 <- merge(combined8, max_balance, all.x=TRUE, by.x='account_id', by.y='account_id')
  combined9 <- merge(combined9, min_balance, all.x=TRUE, by.x='account_id', by.y='account_id')
  final_df <- combined9 %>% select(c('account_id', 'district_name', 'open_date', 'statement_frequency', 'num_customers', 'credit_cards', 'loan', 'loan_amount', 'loan_payments', 'loan_term', 'loan_status', 'loan_default', 'max_withdrawal', 'min_withdrawal', 'cc_payments', 'max_balance', 'min_balance'))
  final_df$loan_term <- as.numeric(final_df$loan_term)
  write.csv(final_df, "customers_r.csv")
  return(final_df)
}

main <- function(){
  accounts <- read.csv("data/accounts.csv")
  districts <- read.csv("data/districts.csv")
  links <- read.csv("data/links.csv")
  cards <- read.csv("data/cards.csv")
  loans <- read.csv("data/loans.csv")
  transactions <- read.csv("data/transactions.csv")
  payment_orders <- read.csv("data/payment_orders.csv")
  tidy_customers(accounts, districts, links, cards, loans, transactions, payment_orders)
}

if (!interactive()) {
  main()
}