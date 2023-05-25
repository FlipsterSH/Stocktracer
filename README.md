# Stocktracer
STOCK NEWS WEBSITE


INSTALLMENTS, before running the program:
pip install flask
pip install yfinance



To RUN the program:
Run the command in the python terminal: python app.py
Or click the run button in the app.py file.



The NEWS part og the page describes:
1. How far the indices and stocks are from 50, 100 150 and 200 day moving average. These are only displayed if the current price is within 3% og the moving average.
2. How far the stocks and indices are from their all time hight (ath).
3. Whether or not the indices and volatility index (VIX) are up or down last three months. And a comment on whether or not the markets have been stable last three months.
4. Compares the last three months, with all three month intervals last 30 years. Displays the periods with the highest percent match.

These are the stocks and indices included in the program (specifically for me):
-Apple (AAPL)
-GOOGLE (GOOG)
-Microsoft (MSFT)
-Nasdaq100 index(^NDX)
-SP500 index(SPY)
-Tesla (TSLA)
-Stockmarket volatility index (VIX)