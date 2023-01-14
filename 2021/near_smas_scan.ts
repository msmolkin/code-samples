# near_smas_scan
# Check if price is within 2% of a moving average.
# Or dropped ~20% today and is at the daily VWAP.
# Then I'll look at the plot and see if it's been following this moving average

input price = FundamentalType.CLOSE;
input averageType = AverageType.SIMPLE;
input daily = AggregationPeriod.DAY;

input sma_13_length = 13;
input sma_20_length = 20;
input sma_50_length = 50;
input sma_100_length = 100;
input sma_200_length = 200;

def sma_13 = MovingAverage(averageType, Fundamental(price, period = daily), sma_13_length);
def sma_20 = MovingAverage(averageType, Fundamental(price, period = daily), sma_20_length);
def sma_50 = MovingAverage(averageType, Fundamental(price, period = daily), sma_50_length);
def sma_100 = MovingAverage(averageType, Fundamental(price, period = daily), sma_100_length);
def sma_200 = MovingAverage(averageType, Fundamental(price, period = daily), sma_200_length);

def delta = 0.02;

def near_sma_13 = between(close, sma_13 - delta * sma_13, sma_13 + delta * sma_13);
def near_sma_20 = between(close, sma_20 - delta * sma_20, sma_20 + delta * sma_20);
def near_sma_50 = between(close, sma_50 - delta * sma_50, sma_50 + delta * sma_50);
def near_sma_100 = between(close, sma_100 - delta * sma_100, sma_100 + delta * sma_100);
def near_sma_200 = between(close, sma_200 - delta * sma_200, sma_200 + delta * sma_200);

def amount_traded = volume * vwap;
def daily_vwap = vwap(period = daily);
def near_vwap_daily = between(close, daily_vwap - delta * daily_vwap, daily_vwap + delta * daily_vwap);
def dropped_to_daily_vwap = volume > 100000 and amount_traded > 2000000 and high / close > 1.15 and near_vwap_daily;

plot scan = near_sma_13 or near_sma_20 or near_sma_50 or near_sma_100 or near_sma_200 or dropped_to_daily_vwap;

---

# near_vwap_weekly_scan
# Check if price is within 2% of weekly VWAP and has been 10% higher this week

def weekly_high = high(period = AggregationPeriod.WEEK);
def weekly_vwap = vwap(period = AggregationPeriod.WEEK);
def delta = 0.02;
def threshold = 1.10;

def near_vwap_weekly = between(close, weekly_vwap - delta * weekly_vwap, weekly_vwap + delta * weekly_vwap);
plot scan = near_vwap_weekly and weekly_high >= threshold * close;

---

# near_vwap_monthly_scan
# Check if price is within 2% of monthly VWAP and has been 10% higher this month

def monthly_high = high(period = AggregationPeriod.MONTH);
def monthly_vwap = vwap(period = AggregationPeriod.MONTH);
def delta = 0.02;
def threshold = 1.10;

def near_vwap_monthly = between(close, monthly_vwap - delta * monthly_vwap, monthly_vwap + delta * monthly_vwap);
plot scan = near_vwap_monthly and monthly_high >= threshold * close;