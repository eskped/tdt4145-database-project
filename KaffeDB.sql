-- sletter eksisterende tabeller

DROP TABLE IF EXISTS Bruker;
DROP TABLE IF EXISTS HarSmakt;
DROP TABLE IF EXISTS Kaffe;
DROP TABLE IF EXISTS Brenneri;
DROP TABLE IF EXISTS Kaffeparti;
DROP TABLE IF EXISTS Foredlingsmetode;
DROP TABLE IF EXISTS Gaard;
DROP TABLE IF EXISTS Kaffeboenne;
DROP TABLE IF EXISTS Inneholder;
DROP TABLE IF EXISTS DyrkesAv;

-- oppretter tabeller

CREATE TABLE Bruker (
        BrukerID INTEGER NOT NULL,
        Epostadresse VARCHAR(30) NOT NULL,
        FulltNavn VARCHAR(30) NOT NULL,
        Passord VARCHAR(30) NOT NULL,
        CONSTRAINT Bruker_PK PRIMARY KEY (BrukerID),
        CONSTRAINT Bruker_U UNIQUE (Epostadresse)
);

CREATE TABLE HarSmakt (
        BrukerID INTEGER NOT NULL,
        KaffeNavn VARCHAR(30) NOT NULL,
        BrenneriID INTEGER NOT NULL,
        Poeng INTEGER NOT NULL,
        Notat VARCHAR(280),
        Dato Date,
        CONSTRAINT HarSmakt_PK PRIMARY KEY (BrukerID, KaffeNavn, BrenneriID),
        CONSTRAINT HarSmakt_CHK CHECK ((Poeng >= 1) AND (Poeng <= 10)),
        CONSTRAINT HarSmakt_FK1 FOREIGN KEY (BrukerID) REFERENCES Bruker(BrukerID)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
        CONSTRAINT HarSmakt_FK2 FOREIGN KEY (KaffeNavn) REFERENCES Kaffe(Navn)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
        CONSTRAINT HarSmakt_FK3 FOREIGN KEY (BrenneriID) REFERENCES Brenneri(BrenneriID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

CREATE TABLE Kaffe (
        Navn VARCHAR(30) NOT NULL,
        BrenneriID INTEGER NOT NULL,
        KiloprisNOK FLOAT,
        Grad VARCHAR(30),
        Notat VARCHAR(280),
        Dato Date,
        KaffepartiID INTEGER NOT NULL,
        CONSTRAINT Kaffe_PK PRIMARY KEY (Navn, BrenneriID),
        CONSTRAINT Kaffe_U UNIQUE (Navn, BrenneriID),
        CONSTRAINT Kaffe_FK1 FOREIGN KEY (BrenneriID) REFERENCES Brenneneri(BrenneriID)
                ON UPDATE CASCADE
                ON DELETE CASCADE,
        CONSTRAINT Kaffe_FK2 FOREIGN KEY (KaffepartiID) REFERENCES Kaffeparti(KaffepartiID)
                ON UPDATE CASCADE
                ON DELETE CASCADE
);

CREATE TABLE Brenneri (
        BrenneriID INTEGER NOT NULL,
        Navn VARCHAR(30) NOT NULL,
        Sted VARCHAR(30) NOT NULL,
        CONSTRAINT Brenneri_PK PRIMARY KEY (BrenneriID),
        CONSTRAINT Brenneri_U UNIQUE (Navn, Sted)
);

CREATE TABLE Kaffeparti (
        KaffepartiID INTEGER NOT NULL,
        Innhostingsaar INTEGER,
        KiloprisUSD FLOAT,
        ForedlingsmetodeNavn VARCHAR(30) NOT NULL,
        GaardID INTEGER NOT NULL,
        CONSTRAINT Kaffeparti_PK PRIMARY KEY (KaffepartiID),
        CONSTRAINT Kaffeparti_FK1 FOREIGN KEY (ForedlingsmetodeNavn) REFERENCES Foredlingsmetode(Navn)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
        CONSTRAINT Kaffeparti_FK2 FOREIGN KEY (GaardID) REFERENCES Gaard(GaardID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

CREATE TABLE Foredlingsmetode (
        Navn VARCHAR(30) NOT NULL,
        Beskrivelse VARCHAR(280),
        CONSTRAINT Foredlingsmetode_PK PRIMARY KEY (Navn)
);

CREATE TABLE Gaard (
        GaardID INTEGER NOT NULL,
        Navn VARCHAR(30) NOT NULL,
        MeterOverHavet INTEGER,
        Region VARCHAR(30) NOT NULL,
        Land VARCHAR(30) NOT NULL,
        CONSTRAINT Gaard_PK PRIMARY KEY (GaardID)
);

CREATE TABLE Kaffeboenne (
        Sort VARCHAR(30) NOT NULL,
        Art VARCHAR(30),
        CONSTRAINT Kaffeboenne_PK PRIMARY KEY (Sort)
);

CREATE TABLE Inneholder (
        KaffepartiID INTEGER NOT NULL,
        KaffeboenneSort VARCHAR(30) NOT NULL,
        CONSTRAINT Inneholder_PK PRIMARY KEY (KaffepartiID, KaffeboenneSort),
        CONSTRAINT Inneholder_FK1 FOREIGN KEY (KaffepartiID) REFERENCES Kaffeparti(KaffepartiID)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
        CONSTRAINT Inneholder_FK2 FOREIGN KEY (KaffeboenneSort) REFERENCES Kaffeboenne(Sort)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

CREATE TABLE DyrkesAv (
        KaffeboenneSort VARCHAR(30) NOT NULL,
        GaardID INTEGER NOT NULL,
        CONSTRAINT DyrkesAv_PK PRIMARY KEY (KaffeboenneSort, GaardID),
        CONSTRAINT DyrkesAv_FK1 FOREIGN KEY (KaffeboenneSort) REFERENCES Kaffeboenne(Sort)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
        CONSTRAINT DyrkesAv_FK2 FOREIGN KEY (GaardID) REFERENCES Gaard(GaardID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);