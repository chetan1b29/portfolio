library(fpp2)
library(car)
library(seasonal)
overSeas.df <- read.csv('D:/Chetan-PC/Stats CA2/OverseasTrips.csv')
names(overSeas.df)<- c('quarter', 'trips')
overSeas.ts <- ts(overSeas.df$trips,start=c(2012,1), frequency = 4)
str(overSeas.ts)
print(overSeas.ts)
autoplot(overSeas.ts)
ggseasonplot(overSeas.ts, year.labels = TRUE, year.labels.left = TRUE)+
  ylab("Tousands")+
  ggtitle('Trips in Thousands')
ggsubseriesplot(overSeas.ts)+
  ylab(" Thousands")+
  ggtitle("Seasonal Sbseries Plot: Overseas Trips")
overSeas.decomp<-decompose(overSeas.ts, type='multiplicative')
autoplot(overSeas.decomp)
plot(seas(overSeas.ts))
overSeas.snaive <- snaive(overSeas.ts, h=3)
summary(overSeas.snaive)
autoplot(overSeas.snaive)
checkresiduals(overSeas.snaive)
accuracy(overSeas.snaive)


overSeas.ets<-ets(overSeas.ts, model='MAM', alpha = 0.6)
forecast(overSeas.ets,h=3)
summary(overSeas.ets)
round(accuracy(overSeas.ets),2)
checkresiduals(overSeas.ets)

autoplot(forecast(overSeas.ets, 3))+autolayer(fitted(forecast(overSeas.ets, 3)), series = 'Fitted')

 
overSeas.hw<-hw(overSeas.ts, seasonal = 'multiplicative', h=3)
summary(overSeas.hw)
autoplot(overSeas.hw)+autolayer(fitted(overSeas.hw), series = 'Fitted')

adf.test(overSeas.ts) ##Augmented Dickey Fuller Test
ggtsdisplay(overSeas.ts)
ndiffs(overSeas.ts)
nsdiffs(overSeas.ts)
adf.test(diff(overSeas.ts, differences = 2))
plot(diff(overSeas.ts, differences = 2))
overseas.diff <- diff(overSeas.ts, differences = 2, lag = 4)
ggtsdisplay(overseas.diff)

overseas.arima <- arima(overSeas.ts, order=c(1,1,0), seasonal = c(1,1,0))
summary(overseas.arima)
checkresiduals(overseas.arima)
Box.test(overseas.arima$residuals, type='Ljung-Box')
qqnorm(overseas.arima$residual)
qqline(overseas.arima$residual)

overseas.auto <- auto.arima(overSeas.ts)#, order=c(2,1,0), seasonal = c(0,1,2))
checkresiduals(overseas.auto)
summary(overseas.auto)
round(accuracy(overseas.auto),2)
checkresiduals(overseas.auto)
autoplot(forecast(overseas.auto,h=3))+autolayer(fitted(forecast(overseas.auto,h=3)), series = 'Fitted')
Box.test(overseas.auto$residuals, type='Ljung-Box')
qqnorm(overseas.auto$residual)
qqline(overseas.auto$residual)

overSeas.ts %>% tsCV(forecastfunction = ets(model='MAM'), h=3) -> e
e^2 %>% mean(na.rm=TRUE) %>% sqrt()
