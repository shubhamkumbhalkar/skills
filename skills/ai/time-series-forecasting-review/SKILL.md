---
name: time-series-forecasting-review
description: Use when building or reviewing a time-series forecasting approach, model, or pipeline (demand, capacity, revenue, metrics). Trigger on "review my forecasting model/pipeline", "is my backtest valid", "why is my forecast wrong in production", or "choose an evaluation metric / baseline for forecasting". Surfaces data leakage, invalid backtesting, missing baselines, seasonality/covariate gaps, wrong metrics, and drift/retraining blind spots.
license: MIT
metadata:
  version: "0.1.0"
  author: Shubham Kumbhalkar
---

# Time-Series Forecasting Review

Review a forecasting approach for the mistakes that make a model look great offline and fail
in production. Forecasting is deceptively easy to get wrong: leakage and bad backtests inflate
offline metrics, and quiet drift erodes them online. Be specific about the failure and the fix.

## How to run

1. Restate the problem: what is forecast, the horizon, the granularity, how often it retrains,
   and what decision the forecast drives (the decision sets how accurate it must be and which
   metric matters). Ask if any are unclear.
2. Walk each area below; for each issue give **Problem**, **Why it matters**, and **Fix**.
3. End with a verdict and the top fixes.

## Areas

**Data leakage (the #1 killer)**
- Are features available at prediction time, or do they leak the future (e.g., using a value
  only known after the forecast date, target-derived features, or post-event revisions)?
- Is normalization/scaling fit on the training window only, not the whole series?
- For lagged features, are lags strictly in the past relative to each forecast point?

**Backtesting & validation**
- Is validation done with time-ordered splits or rolling/expanding-window backtests, NOT random
  k-fold (random folds leak future into past)?
- Does the backtest respect the real forecast gap (predict h steps ahead from information cutoff)?
- Are multiple origins tested (rolling origin) so the metric is not a single lucky window?

**Baselines (are you actually beating anything?)**
- Is the model compared to naive baselines: last value, seasonal-naive, moving average?
- A "good" MAPE means nothing if seasonal-naive beats it. Always report baseline deltas.

**Seasonality, covariates & structure**
- Are seasonality (daily/weekly/yearly), holidays, and known events modeled or provided as covariates?
- Are past-only vs known-future covariates handled correctly (you can use known-future features
  like promotions/holidays at inference; you cannot use unknown-future ones)?
- Intermittent/zero-inflated series handled (they break naive MAPE and many models)?

**Metrics (match the metric to the decision)**
- Is the metric right for the use? MAPE breaks near zeros; use sMAPE/MASE/WAPE or a scaled error.
- If the decision is asymmetric (under- vs over-forecast cost differently), use a quantile/pinball
  loss and forecast the relevant quantile, not just the mean.
- Are prediction intervals produced and calibrated, or only point forecasts?

**Production & drift**
- Is forecast accuracy monitored online against actuals as they arrive, with an alarm on degradation?
- Retraining cadence and trigger defined? Cold-start / new-entity handling?
- Is there a fallback (baseline forecast) when the model is unavailable or clearly off?

**Foundation models (if using one, e.g. TimesFM)**
- Zero-shot vs fine-tuned: is zero-shot actually good enough for this series, benchmarked vs baselines?
- Context length and covariate support match your data? License terms compatible with your use?

## Output format

```
## Forecasting review: <system>  — <Sound | Fix before trusting | Rework>

### Must-fix
1. ...

### Findings
- [Leakage] Problem / Why / Fix
- [Backtesting] Problem / Why / Fix
...

### Solid
- ...
```
