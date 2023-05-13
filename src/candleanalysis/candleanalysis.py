"""candleanalysis (module)

Python module which provides several patternanalyses functions
for candle stick analysis."""

# Import modules
# --------------
import math
import pandas as pd
import constant


class PatternAnalysis:
    """Patternanalysis (object)

    Klasse zur Analyse von Candlestickls"""

    @staticmethod
    def IsStar(adfRow: pd.DataFrame) -> int:
        """Prüft, ob die aktuelle Cancle ein Star oder Hammer ist.

        Parameter
        ---------
        adfRow : pd.DataFrame
           Dataframe mit einer Zeile, das die aktuelle Candle beinhaltet,
           die überprüft werden soll.

        Return
        ------
        int
            SELL (1) wenn es sich um einen Hammer handelt
            BUY(2)   wenn es sich um einn Star handelt
            0        wenn keine besondere Candle vorliegt"""

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
        # Sollte die Größe der Candle kleiner als
        # ein Pip sein, dann auf 1 Pip setzen
        # ---------------------------------------
        lfBodyDiff = max(abs(adfRow.Open[0] - adfRow.Close[0]), 0.000001)

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

    @staticmethod
    def IsThreeLine(adfRowset: pd.DataFrame) -> int:
        """Überprüft, ob die letzten 4 Candles des übergebenen Roses
        ein three line strike sind.

        Parameter
        ---------
        adfRow : pd.DataFrame
           Dataframe, das vier Zeilen beinhalten muss,
           die überprüft werden sollen.

        Return
        ------
        int
            SELL (-1) wenn es sich um einen Hammer handelt
            BUY (1)   wenn es sich um einn Star handelt
            0         wenn keine besondere Candle vorliegt"""

        # Variablendefinition
        # -------------------
        i: int = 0  # Zählervariable
        liMerkrichtung: int = 0  # Richtung, die die Candles einnehmen
        liRichtung: int = 0  # Richtung, in die die aktuelle Candle zeigt
        lfBody: float = 0.0  # Größe der Candle

        # Überprüfen, ob 4 Candles übergeben wurden
        # Wenn nicht, dann 0 zurück geben
        # -----------------------------------------
        if len(adfRowset) != 4:
            return 0

        # Die vier Candles überprüfen
        # ---------------------------
        for i in range(4):
            # Richtung der aktuellen Candle ermitteln
            # ---------------------------------------
            liRichtung = PatternAnalysis.CandleDirection(adfRowset.iloc[i : i + 1])

            # Wenn noch keine Richtung gemerkt wurde, dann jetzt
            # die Richtung, in die überprüft werden soll ermitteln
            # ----------------------------------------------------
            if liMerkrichtung == 0:
                liMerkrichtung = liRichtung

                # Wenn die erste Candle eine Doji Candle ist,
                # dann kann kein 3 Line Strike ermittelt werden
                # ---------------------------------------------
                if liMerkrichtung == 0:
                    return 0

            # Wenn die zweite oder dritte Candle eine andere Richtung haben
            # als die ursprünglich gemerkte Candle, dann handelt es sich um keinen
            # 3 Line Strike
            # --------------------------------------------------------------------
            if 0 < i < 3 and liRichtung != liMerkrichtung:
                return 0

            # Wenn die vierte Candle in die gleiche Richtung weist, dann
            # handelt es sich auch nicht um einen 3 Line Strike
            # ----------------------------------------------------------
            if i == 3 and liRichtung == liMerkrichtung:
                return 0

            # Die Größe des Körpers der 3. Candle merken
            # ------------------------------------------
            if i == 2:
                lfBody = abs(adfRowset.Close[i] - adfRowset.Open[i])

            # Überprüfen, ob die letzte Candle kleiner ist als die
            # vorletzte Candle. Wenn das so ist, dann ist es ebenfalls
            # kein 3 Line Strike.
            # --------------------------------------------------------
            if i == 3 and abs(adfRowset.Close[i] - adfRowset.Open[i]) < lfBody:
                return 0

        # Wenn bisher nicht abgebrochen wurde, dann die Richtung
        # der letzten Candle zurück geben
        # ------------------------------------------------------
        return liRichtung

    @staticmethod
    def CandleDirection(adfRow: pd.DataFrame) -> int:
        """Überprüft, ob die Cancle aufsteigend oder absteigend ist
        und gibt die Richtung entsprechend zurück.

        Parameter
        ---------
        adfRow : pd.DataFrame
            Dataframe mit einer Candle, die überprüft werden soll.

        Return
        ------
        int
            SELL (-1) bedeutet fallende Candle
            BUY (1)   bedeutet steigende Candle
            0         bedeutet, dass es sich um eine Doji Candle handelt"""

        # Variablendefinition
        # -------------------
        lfBody: float = 0.0

        # Überprüfen, ob eine Zeile übergeben wurde
        # -----------------------------------------
        if len(adfRow) == 0:
            return 0

        # Größe des Body ausrechnen
        # -------------------------
        lfBody = adfRow.Close[0] - adfRow.Open[0]

        # Wenn es sich um eine Doji Candle handelt, 0 zurück geben
        # --------------------------------------------------------
        if lfBody == 0:
            return 0

        # Das Vorzeichen der Candle für 1 verwenden
        # -----------------------------------------
        lfBody = math.copysign(1.0, lfBody)

        # Wert zurück geben
        # -----------------
        return int(lfBody)
