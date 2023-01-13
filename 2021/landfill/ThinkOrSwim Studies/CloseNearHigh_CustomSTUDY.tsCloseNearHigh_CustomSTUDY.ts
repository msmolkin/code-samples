# Whether the day closed within 5% of the intraday high

#Wizard text: Close of period is greater than or equal to
#Wizard input: percent
#Wizard text: % of the intraday high
input delta = 5.0;
def percentChg = (100 - delta) / 100;
input period = AggregationPeriod.DAY;

plot scan = close(period = period) is greater than or equal to high(period = period) * percentChg;
