library(chron)
library(date)
library(lubridate)
library(dplyr)
library("zoo")
library(ncdf4)
library(googledrive)
library(tibble)

ss = read.csv(paste('https://docs.google.com/spreadsheets/d/e/2PACX-1vR3aIPa3aSkRk4fQvKkr7pb64tfFh5m3SN1--2cmkKUGjOyqqwi4iC8UeblaMwKdp5iWsv4b5QU715N/pub?gid=0&single=true&output=csv', sep=","), header = F)
# Date1	Date2	Time	V_batt	V_int	V_ext	P_dbar	pH_int	O2_umolkg	temp_SBE	sal_SBE	V_batt_elec	charge_status
#  Plot V_batt P_dbar sal_SBE temp_SBE V_int pH
#  1st cut, just plot P_dbar, sal_SBE, temp_SBE and pH

datetime <- paste(ss$V2, ss$V3, sep = " ")
ss$V6 <- strptime(datetime, "%Y/%m/%d %H:%M:%S")
ss <- ss[order(ss$V1),]
ss <- subset.data.frame(ss, subset = (V2!=0 & V2!= "undefined" & V2!="Date2"), select = V6:V11)
ss <- setNames(ss, c("DateTime", "P_dbar", "pH_int", "O2_umolkg", "temp_SBE", "sal_SBE"))
ss$DateTime <- as.numeric(as.POSIXct(ss$DateTime))
write.csv(ss, file = "/Users/vrowley/Google\ Drive\ File\ Stream/My\ Drive/SCCOOS/GIT/SCCOOS/SeapHOx/erddap/SeapHOx_PoC.csv")
seaphox_zoo <- read.zoo(ss, index = 1, format = "%Y-%m-%d %H:%M:%S", tz = "UTC", index.name = "DateTime")
jpeg(filename = "/Users/vrowley/Google\ Drive\ File\ Stream/My\ Drive/SCCOOS/GIT/SCCOOS/SeapHOx/erddap/SeapHOx_PoC.jpeg", width = 640, height = 480, units = "px", pointsize = 12, quality = 75)
plot.zoo(seaphox_zoo)
dev.off()


newss <- setNames(newss, c("DateTime", "Date1", "Date2", "Time", "V_batt", "V_int", "V_ext", "P_dbar", "pH_int", "O2_umolkg", "temp_SBE", "sal_SBE", "V_batt_elec"))
#ssnames <- subset(newss, V1=="Date1")
#vecnames <- as.vector(ssnames)
orderedss <- newss[order(newss$DateTime),]
goodss <- subset(orderedss, Date2!=0 & Date2!= "undefined" & Date2!="Date2")
goodss <- add_row(goodss, ssnames, .before = 1)

write.csv(newss, file = "/Users/vrowley/Google\ Drive\ File\ Stream/My\ Drive/SCCOOS/GIT/SCCOOS/SeapHOx/erddap/SeapHOx_PoC.csv")

dvals <- unique(ss$V2)
dvals <- dvals[order(dvals)]
tvals <- unique(ss$V3)
tvals <- tvals[order(tvals)]
pvals <- unique(ss$V7)
pvals <- pvals[order(pvals)]
svals <- unique(ss$V11)
svals <- svals[order(svals)]
tempvals <- unique(ss$V10)
tempvals <- tempvals[order(tempvals)]
phvals <- unique(ss$V8)
phvals <- phvals[order(phvals)]


lon1 <- ncdim_def("longitude", "degrees_east", xvals)
lat2 <- ncdim_def("latitude", "degrees_north", yvals)
time <- data$time
time_d <- ncdim_def("time","h",unique(time))
