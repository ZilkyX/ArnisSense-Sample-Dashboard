import sqlite3
from pathlib import Path

class DatabaseHandler:
    def __init__(self, db_name="./database/main.db"):
        self.db_path = Path(db_name)
        self.conn = None

        self.connect()

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def create_match(self, data: dict):

        cursor = self.conn.cursor()

        cursor.execute("""
        INSERT INTO Matches (
            Player1Name,
            Player2Name,
            Player1Team,
            Player2Team,
            NumberOfRounds,
            MatchType
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data["player1"],
            data["player2"],
            data["player1_team"],
            data["player2_team"],
            data["rounds"],
            data["match_type"]
        ))

        self.conn.commit()

        return cursor.lastrowid

    def save_round(
        self,
        match_id,
        round_no,
        p1_score,
        p2_score,
        p1_hit,
        p2_hit,
        winner
    ):

        cursor = self.conn.cursor()

        cursor.execute("""
        INSERT OR REPLACE INTO RoundResults (
            MatchID,
            RoundNumber,
            Player1Score,
            Player2Score,
            Player1HitPart,
            Player2HitPart,
            Winner
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            match_id,
            round_no,
            p1_score,
            p2_score,
            p1_hit,
            p2_hit,
            winner
        ))

        self.conn.commit()

    def get_rounds(self, match_id):

        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT *
        FROM RoundResults
        WHERE MatchID = ?
        ORDER BY RoundNumber
        """, (match_id,))

        return cursor.fetchall()

    def get_final_score(self, match_id):

        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT
            SUM(Player1Score) AS P1,
            SUM(Player2Score) AS P2
        FROM RoundResults
        WHERE MatchID = ?
        """, (match_id,))

        return cursor.fetchone()

    def get_matches(self):

        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT *
        FROM Matches
        ORDER BY CreatedAt DESC
        """)

        return cursor.fetchall()

    def delete_match(self, match_id):

        cursor = self.conn.cursor()

        cursor.execute("""
        DELETE FROM Matches
        WHERE MatchID = ?
        """, (match_id,))

        self.conn.commit()

 
    def close(self):
        if self.conn:
            self.conn.close()
