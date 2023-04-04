"""candleanalysis (module)

Python module which provides several patternanalyses functions
for candle stick analysis."""

# Import modules
# --------------
import pandas as pd
import constant


class PatternAnalysis:
    """Klasse zur Analyse von Candlestickls"""

    @staticmethod
    def IsStar(adfRow: pd.DataFrame) -> int:
        """Checks if the current candle is a star or hammer"""

        # Variablen definieren
        # ---------------------
        lfHighDiff: float = 0.0
        lfLowDiff: float = 0.0
        lfBodyDiff: float = 0.0
        lfHighRatio: float = 0.0
        lfLowRatio: float = 0.0
        lfBodydiffmin: float = 0.0001

        #   BUY      SELL
        # ==================
        #
        #    |    H    |
        #  |---|C      |
        #  |---|O      |
        #    |      O|---|
        #    |      C|---|
        #    |    L    |
        #
        # ==================

        # Die Länge der oberen Wig ermitteln
        # -----------------------------------
        lfHighDiff = adfRow.High[0] - max(adfRow.Open[0], adfRow.Close[0])

        # Die Länge der unteren Wig ermitteln
        # ------------------------------------
        lfLowDiff = min(adfRow.Open[0], adfRow.Close[0]) - adfRow.Low[0]

        # Die Länge der Candle ermitteln
        # -------------------------------
        lfBodyDiff = abs(adfRow.Open[0] - adfRow.Close[0])

        # Sollte die Größe der Candle kleiner als ein Pip sein, dann auf 1 Pip setzen
        # ----------------------------------------------------------------------------
        if lfBodyDiff < 0.000001:
            lfBodyDiff = 0.000001

        # print(f"{lfBodyDiff}\t{lfBodyDiff}\t{lfBodyDiff}")

        # Größenfaktor der oberen und unteren Wig zu Candle ermitteln
        # ------------------------------------------------------------
        lfHighRatio = lfHighDiff / lfBodyDiff
        lfLowRatio = lfLowDiff / lfBodyDiff

        # Wenn die obere Wig größer ist als die Candle selbst und die untere
        # Wig kleiner ist als 1/5 der oberen Wig und die Candle größer als
        # ein Pip ist, dann zurück geben, dass es sich um einen Star
        # handelt - sonst ist es ein Hammer.
        # ------------------------------------------------------------------
        if (
            lfHighRatio > 2
            and lfLowDiff < 0.2 * lfHighDiff
            and lfBodyDiff > lfBodydiffmin
            and adfRow.Open[0] > adfRow.Close[0]
        ):  # and open[row]>close[row]):
            # print(f"{adfRow.index[0]}: Sell")
            return constant.SELL
        if (
            lfLowRatio > 2
            and lfHighDiff < 0.2 * lfLowDiff
            and lfBodyDiff > lfBodydiffmin
            and adfRow.Open[0] < adfRow.Close[0]
        ):  # and open[row]<close[row]):
            # print(f"{adfRow.index[0]}: Buy")
            return constant.BUY

        # Andernfalls zurück geben, dass kein Star oder Hammer vorliegt
        # -------------------------------------------------------------
        return 0
