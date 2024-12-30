-- Create tables
CREATE TABLE NPC (
    NPC_ID TEXT PRIMARY KEY,
    Name TEXT,
    Role TEXT
);

CREATE TABLE Dialogue (
    Dialogue_ID TEXT PRIMARY KEY,
    NPC_ID TEXT,
    Language_ID TEXT,
    Text TEXT,
    Response_Options TEXT,
    FOREIGN KEY (NPC_ID) REFERENCES NPC(NPC_ID),
    FOREIGN KEY (Language_ID) REFERENCES Language(Language_ID)
);

CREATE TABLE Language (
    Language_ID TEXT PRIMARY KEY,
    Language_Name TEXT,
    Difficulty_Level INTEGER
);

CREATE TABLE Player (
    PK_Player_ID TEXT PRIMARY KEY,
    Name TEXT,
    Age INTEGER,
    Level INTEGER,
    Experience INTEGER,
    Current_Level_ID TEXT,
    Achievement_ID TEXT,
    FOREIGN KEY (Achievement_ID) REFERENCES Achievement(Achievement_ID)
);

CREATE TABLE Achievement (
    Achievement_ID TEXT PRIMARY KEY,
    Achievement_Name TEXT,
    Description TEXT,
    Points INTEGER
);

CREATE TABLE Quest (
    Quest_ID TEXT PRIMARY KEY,
    Quest_Name TEXT,
    Description TEXT,
    Difficulty INTEGER,
    Status TEXT,
    Required_Level INTEGER
);

-- Populate tables with sample data
INSERT INTO NPC VALUES
('NPC001', 'Guardian', 'Protector'),
('NPC002', 'Merchant', 'Trader');

INSERT INTO Language VALUES
('L001', 'English', 1),
('L002', 'Spanish', 2);

INSERT INTO Dialogue VALUES
('D001', 'NPC001', 'L001', 'Hello, traveler! How can I help you?', 'Ask about the quest|Leave'),
('D002', 'NPC002', 'L002', 'Bienvenido! ¿Qué necesitas?', 'Comprar|Vender');

INSERT INTO Player VALUES
('P001', 'Alice', 25, 5, 1500, NULL, NULL),
('P002', 'Bob', 30, 10, 3000, NULL, NULL);

INSERT INTO Achievement VALUES
('A001', 'First Blood', 'Defeat your first enemy.', 10),
('A002', 'Treasure Hunter', 'Find a hidden treasure.', 20);

INSERT INTO Quest VALUES
('Q001', 'Dragon Slayer', 'Defeat the dragon in the mountains.', 5, 'Active', 10),
('Q002', 'Herbalist', 'Collect 10 medicinal herbs.', 2, 'Completed', 2);
