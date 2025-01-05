-- Create tables
-- The NPC table stores non-playable characters with unique IDs, names, and roles.
CREATE TABLE NPC (
    NPC_ID INTEGER PRIMARY KEY AUTOINCREMENT, -- Using integers for IDs improves performance.
    Name TEXT NOT NULL,
    Role TEXT NOT NULL
);

-- The Language table stores languages used in the game, including a difficulty level.
CREATE TABLE Language (
    Language_ID INTEGER PRIMARY KEY AUTOINCREMENT, -- IDs are now integers for efficiency.
    Language_Name TEXT NOT NULL,
    Difficulty_Level INTEGER NOT NULL CHECK(Difficulty_Level > 0) -- Ensures positive difficulty levels.
);

-- The QuestStatus table defines various statuses a quest can have (e.g., Active, Completed).
CREATE TABLE QuestStatus (
    Status_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Status_Name TEXT NOT NULL
);

-- The Dialogue table links NPCs and languages to their dialogue and response options.
CREATE TABLE Dialogue (
    Dialogue_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NPC_ID INTEGER NOT NULL,
    Language_ID INTEGER NOT NULL,
    Text TEXT NOT NULL,
    Response_Options TEXT NOT NULL,
    FOREIGN KEY (NPC_ID) REFERENCES NPC(NPC_ID) ON DELETE CASCADE, -- Ensures related dialogues are removed if the NPC is deleted.
    FOREIGN KEY (Language_ID) REFERENCES Language(Language_ID) ON DELETE CASCADE
);

-- The Achievement table stores achievements players can earn.
CREATE TABLE Achievement (
    Achievement_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Achievement_Name TEXT NOT NULL,
    Description TEXT NOT NULL,
    Points INTEGER NOT NULL CHECK(Points >= 0) -- Points must be non-negative.
);

-- The Player table stores player information, including their progress and achievements.
CREATE TABLE Player (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    age INTEGER NOT NULL CHECK(age >= 0),
    level INTEGER DEFAULT 1 CHECK(level > 0),
    current_level_id INTEGER,
    current_player INTEGER,
    lang INTEGER,
    learning_lang INTEGER
);


-- The Quest table defines quests, their difficulty, and required player levels.
CREATE TABLE Quest (
    Quest_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Quest_Name TEXT NOT NULL,
    Description TEXT NOT NULL,
    Difficulty INTEGER NOT NULL CHECK(Difficulty > 0),
    Status_ID INTEGER NOT NULL,
    Required_Level INTEGER NOT NULL CHECK(Required_Level > 0), -- Players must meet the required level.
    FOREIGN KEY (Status_ID) REFERENCES QuestStatus(Status_ID) ON DELETE CASCADE
);

-- The Player_Quest table tracks which quests are assigned to players, their progress, and completion dates.
CREATE TABLE Player_Quest (
    Player_ID INTEGER NOT NULL,
    Quest_ID INTEGER NOT NULL,
    Status_ID INTEGER NOT NULL, -- Tracks progress (e.g., Assigned, In Progress, Completed).
    Assignment_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Auto-populates with the current date and time.
    Completion_Date TIMESTAMP,
    PRIMARY KEY (Player_ID, Quest_ID),
    FOREIGN KEY (Player_ID) REFERENCES Player(PK_Player_ID) ON DELETE CASCADE,
    FOREIGN KEY (Quest_ID) REFERENCES Quest(Quest_ID) ON DELETE CASCADE,
    FOREIGN KEY (Status_ID) REFERENCES QuestStatus(Status_ID)
);

-- The Response_Option table organizes dialogue response options into individual records.
CREATE TABLE Response_Option (
    Option_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Dialogue_ID INTEGER NOT NULL,
    Option_Text TEXT NOT NULL,
    FOREIGN KEY (Dialogue_ID) REFERENCES Dialogue(Dialogue_ID) ON DELETE CASCADE
);

-- Audit_Log table keeps track of all changes to key tables for traceability.
CREATE TABLE Audit_Log (
    Log_ID INTEGER PRIMARY KEY AUTOINCREMENT, -- Auto-incrementing log ID.
    Table_Name TEXT NOT NULL, -- Name of the table where the change occurred.
    Operation_Type TEXT NOT NULL CHECK(Operation_Type IN ('INSERT', 'UPDATE', 'DELETE')), -- Tracks type of change.
    Changed_Data TEXT NOT NULL, -- Stores details of the change.
    Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Automatically records the change time.
);

-- Add indexes for frequently queried columns to improve query performance.
CREATE INDEX idx_npc_role ON NPC(Role);
CREATE INDEX idx_language_name ON Language(Language_Name);
CREATE INDEX idx_achievement_points ON Achievement(Points);

