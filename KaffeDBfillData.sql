-- Legger inn data
 
-- Bruker(BrukerID, Epostadresse, FulltNavn, Passord)
INSERT INTO Bruker VALUES (1, 'helly@hotmail.no', 'Helly Hansen', 'United8');
INSERT INTO Bruker VALUES (2, 'geirs@gmail.com', 'Geir Olsen', 'Geir12345');
INSERT INTO Bruker VALUES (3, 'admin@admin.com', 'Admin', 'admin');
INSERT INTO Bruker VALUES (4, 'fredrik@gmail.com', 'Fredrik Holm', 'Fredda123');

-- HarSmakt(BrukerID, KaffeNavn, BrenneriID, Poeng, Notat, Dato)
INSERT INTO HarSmakt VALUES (1, 'Vinterkaffe 2022', 1, 10, 'Wow - en odyssé for smaksløkene: sitrusskall, melkesjokolade, aprikos!', '2022-01-23');
INSERT INTO HarSmakt VALUES (1, 'AslakKaffe', 1, 7, 'Fruktig og floral kaffe. Kunne hatt litt sterkere smak', '2022-01-23');
INSERT INTO HarSmakt VALUES (1, 'MatsKaffe', 2, 3, 'Ikke så bra', '2022-01-23');
INSERT INTO HarSmakt VALUES (2, 'AslakKaffe', 1, 9, 'Veldig gooood', '2022-01-23');
INSERT INTO HarSmakt VALUES (2, 'MatsKaffe', 2, 5, 'Ikke så veldig god, midt på treet', '2022-01-23');
INSERT INTO HarSmakt VALUES (4, 'Sommerkaffe 2021', 3, 8,'Veldig god kaffe. Er det et ord som beskriver denne kaffen, så er det floral.', '2022-01-01');
  
-- Kaffe(Navn, BrenneriID, KiloprisNOK, Grad, Notat, Dato, KaffepartiID)
INSERT INTO Kaffe VALUES ('Vinterkaffe 2022', 1, 600, 'Lys', 'En velsmakende og kompleks kaffe for mørketiden', '2022-01-22', 1);
INSERT INTO Kaffe VALUES ('AslakKaffe', 1, 500, 'Middels', 'Fruktig og god kaffe', '2022-02-22', 2);
INSERT INTO Kaffe VALUES ('MatsKaffe', 2, 200, 'Mørk', 'Denne her kan anbefales på det sterkeste!', '2022-03-22', 1);
INSERT INTO Kaffe VALUES ('EskilKaffe', 2, 100, 'Middels', 'Snev av floral. Oppfyller dine drømmer.', '2022-04-22', 2);
INSERT INTO Kaffe VALUES ('Sommerkaffe 2021', 3, 300, 'Lys', 'Lett og luftig sommerkaffe', '2021-05-30', 3);
 
-- Brenneri(BrenneriID, Navn, Sted)
INSERT INTO Brenneri VALUES (1, 'Jacobsen & Svart', 'Trondheim');
INSERT INTO Brenneri VALUES (2, 'Barmuda Brenneri', 'Kolbotn');
INSERT INTO Brenneri VALUES (3, 'Kaffebrenneriet', 'Oslo');
 
-- Kaffeparti(KaffepartiID, Innhostingsaar, KiloprisUSD, ForedlingsmetodeNavn, GaardID)
INSERT INTO Kaffeparti VALUES (1, 2021, 8, 'Bærtørket', 1);
INSERT INTO Kaffeparti VALUES (2, 2021, 10, 'Bærtørket', 2);
INSERT INTO Kaffeparti VALUES (3, 2021, 9, 'Vasket', 3);
 
-- Foredlingsmetode(Navn, Beskrivelse)
INSERT INTO Foredlingsmetode VALUES ('Bærtørket', 'Gir fyldig kaffe med stor munnfølelse');
INSERT INTO Foredlingsmetode VALUES ('Vasket', 'Gir fyldig kaffe med stor munnfølelse');
 
-- Gaard(GaardID, Navn, MeterOverHavet, Region, Land)
INSERT INTO Gaard VALUES (1, 'Nombre de Dios', 1500, 'Santa Ana', 'El Salvador');
INSERT INTO Gaard VALUES (2, 'Farma Farmi', 200, 'Santa Claus', 'Rwanda');
INSERT INTO Gaard VALUES (3, 'El granja', 400, 'Cartagena', 'Colombia');
 
-- Kaffeboenne(Sort, Art) 
INSERT INTO Kaffeboenne VALUES ('Bourbon', 'Coffea arabica');
INSERT INTO Kaffeboenne VALUES ('Typica', 'Coffea arabica');
 
-- Inneholder(KaffepartiID, KaffeboenneSort)
INSERT INTO Inneholder VALUES (1, 'Bourbon');
INSERT INTO Inneholder VALUES (2, 'Bourbon');
INSERT INTO Inneholder VALUES (3, 'Typica');
 
-- DyrkesAv(KaffeboenneSort, GaardID)
INSERT INTO DyrkesAv VALUES ('Bourbon', 1);
INSERT INTO DyrkesAv VALUES ('Bourbon', 2);
INSERT INTO DyrkesAv VALUES ('Typica', 3);
INSERT INTO DyrkesAv VALUES ('Typica', 2);