
---

## III. Labor Market (Tealbook A, Nov 2019, pp. 35–36)

### Cell 12 — Payrolls
| Panel | Series | Ticker | Notes |
|-------|--------|--------|-------|
| Change in total nonfarm payrolls (bar) | All employees, total nonfarm | `PAYEMS` | Monthly diff |
| Change in private payrolls — BLS | All employees, total private | `USPRIV` | Monthly diff |
| Change in private payrolls — ADP | ADP nonfarm private | `ADPMNUSNERSA` | Monthly diff |

### Cell 13 — Unemployment & Underutilization
| Panel | Series | Ticker | Notes |
|-------|--------|--------|-------|
| Unemployment rate | U-3 | `UNRATE` | SA |
| Natural rate | CBO NROU | `NROU` | Quarterly → interpolated monthly |
| Underutilization — U-5 | U-5 rate | `U5RATE` | SA |
| Underutilization — U-3 | Unemployment rate | `UNRATE` | SA |
| Underutilization — part-time econ. reasons | Part-time for economic reasons | `LNS12032194` | SA |

### Cell 14 — Participation & Employment-Population
| Panel | Series | Ticker | Notes |
|-------|--------|--------|-------|
| LFPR (total) | Civilian labor force participation rate | `CIVPART` | SA |
| Emp-pop (total) | Employment-population ratio | `EMRATIO` | SA |
| Emp-pop (prime-age) | Emp-pop ratio, 25–54 | `LNS12300060` | SA |

### Cell 15 — JOLTS & Initial Claims
| Panel | Series | Ticker | Notes |
|-------|--------|--------|-------|
| Hires rate (3-mo MA) | Hires rate, total private | `JTS1000HIR` | SA; 3-mo MA applied in code |
| Job openings rate (3-mo MA) | Job openings rate, total nonfarm | `JTSJOR` | SA; 3-mo MA applied in code |
| Quits rate (3-mo MA) | Quits rate, total nonfarm | `JTSQUR` | SA; 3-mo MA applied in code |
| Initial claims (4-wk MA) | Initial UI claims, 4-week MA | `IC4WSA` | Already 4-wk MA from BLS |

### Cell 16 — Demographics (Race/Ethnicity)
| Panel | Series | Ticker | Notes |
|-------|--------|--------|-------|
| Unemployment — Asian | UR, Asian, 16+ | `LNS14032183` | SA |
| Unemployment — Black | UR, Black, 16+ | `LNS14000006` | SA |
| Unemployment — Hispanic | UR, Hispanic, 16+ | `LNS14000009` | SA |
| Unemployment — White | UR, White, 16+ | `LNS14000003` | SA |
| LFPR — Asian | LFPR, Asian, all ages | `LNU01332183` | NSA — STL seasonal adjustment applied in code; substitutes for 25–54 (unavailable on FRED) |
| LFPR — Black | LFPR, Black, 16+ | `LNS11300006` | SA |
| LFPR — Hispanic | LFPR, Hispanic, 16+ | `LNS11300009` | SA |
| LFPR — White | LFPR, White, 16+ | `LNS11300003` | SA |


---

## IV. Prices & Inflation (Tealbook A, Nov 2019, pp. ~37–40)

### Cell 18 — Headline CPI & PCE + Core PCE Measures
| Panel | Series | Ticker | Notes |
|-------|--------|--------|-------|
| Headline CPI | CPI, all urban consumers | `CPIAUCSL` | SA; YoY % computed in code via `.pct_change(12)` |
| Headline PCE | PCE price index | `PCEPI` | SA; YoY % in code |
| PCE ex. food & energy (standard core) | PCE excl. food & energy | `PCEPILFE` | SA; YoY % in code |
| Trimmed mean PCE | Dallas Fed trimmed mean, 12-month rate | `PCETRIM12M159SFRBDAL` | SA; already in YoY % units |
| Market-based PCE ex. food & energy | Market-based PCE excl. food & energy, chain-type | `DPCXRG3M086SBEA` | SA; YoY % in code |
| Forecast panels (right-hand) | Staff projections | — | **Not replicable; omitted** |

### Cell 19 — Labor Cost Growth
| Panel | Series | Ticker | Notes |
|-------|--------|--------|-------|
| Employment cost index (private) | ECI: wages & salaries, private industry | `ECIWAG` | SA, quarterly; YoY via `.pct_change(4)` |
| Average hourly earnings | AHE, all employees, total private nonfarm | `CES0500000003` | SA, monthly; YoY via `.pct_change(12)` |
| Compensation per hour | Business sector hourly compensation, all workers | `HCOMPBS` | SA, quarterly; YoY via `.pct_change(4)` |
| Forecast panel (right-hand) | Staff projections | — | **Not replicable; omitted** |

### Cell 20 — Oil Prices & Import Price Inflation
| Panel | Series | Ticker | Notes |
|-------|--------|--------|-------|
| Brent crude oil price | Global price of Brent crude, USD/bbl | `POILBREUSDM` | Monthly, IMF via FRED; level |
| PCE energy prices | PCE: energy goods & services, chain-type price index | `DNRGRG3M086SBEA` | SA; YoY % in code |
| Core import prices | Import price index ex. food & fuels | `IREXFDFLS` | NSA; YoY % in code |
| CRB spot commodity index | — | — | **Not on FRED; skipped** |
| Core import prices with tariff effects | Fed staff construct | — | **Not replicable; omitted** |

### Cell 21 — Long-Term Inflation Expectations
| Panel | Series | Ticker | Notes |
|-------|--------|--------|-------|
| 5-to-10yr TIPS compensation | 5yr5yr forward inflation expectation (proxy) | `T5YIFRM` | Monthly, St. Louis Fed; closest public proxy |
| Michigan median next 5–10 yrs | Michigan inflation expectation, 1-yr ahead (proxy) | `MICH` | NSA; 5-to-10yr version not available on FRED — to be replaced when manual data integrated |
| SPF PCE median next 10 yrs | Cleveland Fed 5-yr expected inflation (proxy) | `EXPINF5YR` | SPF 10-yr PCE not a FRED time series — to be replaced when Philadelphia Fed data integrated |

