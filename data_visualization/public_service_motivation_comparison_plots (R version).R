
## PSM Comparison
# The purpose of this file is to generate public service motivation (PSM) comparision plots 
# using PSM data from different studies in the literature, and data from  
# the International Social Survey Programme (ISSP) (a cross-national survey).  
# The plots are used to visualize the comparision of PSM within and between countries.


rm(list = ls()) # clear global envirnoment

library(tidyverse)
library(ggpubr)
library(ggplot2) 
library(data.table) 




##******************** My Local Directory *************************
##
opt_my_dir<-"C:/Users/henry_dw8mcdk/Documents/JHU_Work/Johns_Hopkins_RA/Projects_Summer_2020/PSM comparison/replication_archive/R plots"
##
##*****************************************************************

setwd(opt_my_dir)

# Import the data and look at the first six rows
df = read.csv(file = 'full_psm_processed.csv')
df = as.data.table(df)


## PSM Comparison of Bureaucrats between Developed and Developing countries 
## (public employees issp + psm studies)

df_public= df[employee_type == "bureaucrats",]


p1<-ggboxplot(data=df_public, x="developed", y="psm",
              ylab="PSM Score",
              xlab="Economy Classifications",
              #title="PSM Comparison between Developed and Developing Countries \n(with ISSP data)",
              add="dotplot",
              add.params=list(size=0.3,jitter=50),
              legend = "none",
              label="country_code_2_ltr",
             # label.select = list(top.up = 10, top.down = 4),
              font.label=list(size=10),
              repel=TRUE) +  theme(plot.title = element_text(hjust = 0.5))

ggsave("Develop_v_Developing_bureaucrats_all.jpeg",p1,path="outputs")




## PSM Comparison of Bureaucrats between Developed and Developing countries 
## (public employees psm studies)

df_public_no_ISSP= df_public[issp == 0,]


p2<-ggboxplot(data=df_public_no_ISSP, x="developed", y="psm",
              ylab="PSM Score",
              xlab="Economy Classifications",
              #title="PSM Comparison between Developed and Developing Countries \n(without ISSP data)",
              add="dotplot",
              add.params=list(size=0.3,jitter=50),
              legend = "none",
              label="country_code_2_ltr",
              font.label=list(size=10),
              repel=TRUE) +  theme(plot.title = element_text(hjust = 0.5))

ggsave("Develop_v_Developing_bureaucrats_psm_studies_only.jpeg",p2,path="outputs")


## PSM Comparison of Bureaucrats between Developed and Developing countries 
## (public employees with ISSP only)
df_public_ISSP_only= df_public[issp == 1,]


p3<-ggboxplot(data=df_public_ISSP_only, x="developed", y="psm",
              ylab="PSM Score",
              xlab="Economy Classifications",
              add="dotplot",
              add.params=list(size=0.3,jitter=50),
              legend = "none",
              label="country_code_2_ltr",
              font.label=list(size=10),
              repel=TRUE) +  theme(plot.title = element_text(hjust = 0.5))

ggsave("Develop_v_Developing_bureaucrats_issp_only.jpeg",p3,path="outputs")




## PSM Comparison of Bureaucrats vs Non-Bureacrats (all data) 
p4<-ggboxplot(data=df, x="employee_type", y="psm",
              ylab="PSM Score",
              xlab="Employee Type",
              add="dotplot",
              add.params=list(size=0.3,jitter=50),
              legend = "none",
              label="country_code_2_ltr",
              font.label=list(size=10),
              repel=TRUE) +  theme(plot.title = element_text(hjust = 0.5))

ggsave("Public_vs_Private_all.jpeg",p4,path="outputs")



## PSM Comparison of Bureaucrats vs Non-Bureacrats (psm studies only) 
df_no_ISSP = df[issp == 0,]
  
p5<-ggboxplot(data=df_no_ISSP, x="employee_type", y="psm",
              ylab="PSM Score",
              xlab="Employee Type",
              add="dotplot",
              add.params=list(size=0.3,jitter=50),
              legend = "none",
              label="country_code_2_ltr",
              font.label=list(size=10),
              repel=TRUE) +  theme(plot.title = element_text(hjust = 0.5))

ggsave("Public_vs_Private_psm_studies_only.jpeg",p5,path="outputs")



## PSM Comparison of Bureaucrats vs Non-Bureacrats (ISSP only) 
df_ISSP_only = df[issp == 1,]

p6<-ggboxplot(data=df_ISSP_only, x="employee_type", y="psm",
              ylab="PSM Score",
              xlab="Employee Type",
              add="dotplot",
              add.params=list(size=0.3,jitter=50),
              legend = "none",
              label="country_code_2_ltr",
              font.label=list(size=10),
              repel=TRUE) +  theme(plot.title = element_text(hjust = 0.5))

ggsave("Public_vs_Private_ISSP_only.jpeg",p6,path="outputs")





## PSM Comparison of Bureaucrats across Geographic Regions (all) 

p7<-ggboxplot(data=df_public, x="region", y="psm",
              ylab="PSM Score",
              xlab="Geographic Region",
              #title="PSM Comparison of Bureaucrats across Geographic Regions \n(with ISSP data)",
              add="dotplot",
              add.params=list(size=0.3,jitter=50),
              legend = "none",
              label="country_code_2_ltr",
              # label.select = list(top.up = 10, top.down = 4),
              font.label=list(size=10),
              repel=TRUE) +  theme(plot.title = element_text(hjust = 0.5), axis.text.x = element_text(angle = 90, size=8))

ggsave("Public_Geographic_Region_all.jpeg",p7,path="outputs")