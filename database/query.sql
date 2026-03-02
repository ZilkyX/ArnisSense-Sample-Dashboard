
CREATE TABLE IF NOT EXISTS Matches (
    MatchID INTEGER PRIMARY KEY AUTOINCREMENT,

    Player1Name TEXT NOT NULL,
    Player2Name TEXT NOT NULL,

    Player1Team TEXT,
    Player2Team TEXT,

    NumberOfRounds INTEGER NOT NULL,
    MatchType TEXT,

    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
);



CREATE TABLE IF NOT EXISTS RoundResults (
    RoundID INTEGER PRIMARY KEY AUTOINCREMENT,

    MatchID INTEGER NOT NULL,
    RoundNumber INTEGER NOT NULL,

    Player1Score INTEGER DEFAULT 0,
    Player2Score INTEGER DEFAULT 0,

    Player1HitPart TEXT DEFAULT '',
    Player2HitPart TEXT DEFAULT '',

    Winner INTEGER, -- 1 = Player1, 2 = Player2, 0 = Draw

    FOREIGN KEY (MatchID)
        REFERENCES Matches(MatchID)
        ON DELETE CASCADE
);


CREATE INDEX IF NOT EXISTS idx_round_match
ON RoundResults(MatchID);
