# Programowanie Aplikacji Sieciowych - Laboratorium 8

**Protokół IMAP (RFC3501)** (Internet Message Access Protocol) to internetowy protokół pocztowy (służący do odbierania poczty z serwera) zaprojektowany jako następca protokołu POP3. W warstwie transportowej IMAP wykorzystuje protokół TCP oraz 2 porty: port niezabezpieczony: 143 i port zabezpieczony: 993.

Podstawowe informacje:
* Klient łączy się z serwerem i odbiera od niego wiadomość powitalną, rozpoczynając tym samym komunikację z serwerem (komenda klienta rozpoczyna komunikację).
* Każda komenda klienta musi rozpoczynać się od identyfikatora, np. `A0001`, `A0002`, ... nazywanego tagiem. Unikalny tag powinien być generowany dla każdej komendy wysyłanej przez klienta.
* Wszystkie komendy klienta i serwera kończą się ciągiem znaków `<CRLF>` (czyli `\r\n`). Nazwy komend możemy pisać małymi lub wielkimi literami. Komendy mogą posiadać parametry, lub mogą nie wymagać żadnych parametrów.
* **Format komendy klienta:** `tag komenda parametry \r\n`
  Przykład: `TAGX LOGIN pasumcs@infumcs.edu P4SInf2017`
* Odpowiedzi od serwera mogą być jednolinijkowe lub zawierać kilka linii, mogą zaczynać się od tagu, znaku `+` lub znaku `*`
* Jeśli odpowiedź jest wielolinijkowa, to wówczas każda linia (oprócz ostatniej) rozpoczyna się od znaku `*`
* Odpowiedź serwera na daną komendę klienta zawiera (w ostatniej linii odpowiedzi) tag wysłany wraz z tą komendą przez klienta, oraz status i wiadomość, zakończone znakami `<CRLF>` (czyli `\r\n`),
* Są 3 możliwe statusy odpowiedzi od serwera: `OK` (oznacza sukces), `NO` (oznacza niepowodzenie) oraz `BAD` (oznacza błąd składni lub błąd komendy),
* Prawidłowa obsługa odpowiedzi od serwera: sprawdzenie każdej linii odpowiedzi (wszystkie linie odpowiedzi zakończone są `\r\n`) - jeśli linia rozpoczyna się od tagu, należy sprawdzić status odpowiedzi (3 możliwe statusy odpowiedzi serwera: `OK`, `NO`, `BAD`),
* **Format odpowiedzi serwera:** `tag status wiadomość \r\n`
  Przykład: `TAGX OK [READ-WRITE] Select completed (0.000 + 0.000 secs).`
* IMAP posiada możliwości manipulowania danymi na serwerze pocztowym:
  * przeszukiwania skrzynki pocztowej,
  * zaznaczania wiadomości jako przeczytane/nieprzeczytane (zmiana atrybutów wiadomości),
  * ściągania wybranych wiadomości (klient POP3 ściąga wszystkie),
  * ściągania części wiadomości, np. tylko załącznika wiadomości,
  * klient może na serwerze usuwać, tworzyć, zmieniać nazwę skrzynkom pocztowym
* Pod względem bezpieczeństwa protokół ten jest opracowany o wiele lepiej niż SMTP i POP3. Co prawda umożliwia przesyłanie całej komunikacji jawnym tekstem, jednak umożliwia także szyfrowanie wiadomości poprzez zastosowanie komendy AUTHENTICATE i podanie mechanizmu zabezpieczenia transakcji. Przykładowo, może to być realizowane w oparciu o system Kerberos.
* Protokół IMAP wykorzystuje flagi jako tokeny określające "stan" wiadomości. Każda wiadomość może posiadać 0 lub więcej flag. Wszystkie flagi systemowe rozpoczynają się od znaku `\`. Flagi zdefiniowane w protokole IMAP:
  * `\Seen` - oznacza, że wiadomość została przeczytana
  * `\Answered` - oznacza, że na tę wiadomość wysłano odpowiedź
  * `\Flagged` - oznacza, że ta wiadomość jest oznaczona, jako ważna (cytując RFC dla IMAP: *Message is "flagged" for urgent/special attention*)
  * `\Deleted` - wiadomość jest oznaczona jako do usunięcia - przeniesiona do kosza
  * `\Draft` - wiadomość jest zapisana jako wersja robocza, jest nieskończona
  * `\Recent` - wiadomość przed chwilą nadeszła (cytując RFC dla IMAP: *Message is "recently" arrived in this mailbox.*)

Komenda protokołu IMAP - `LIST` (wyświetlenie wszystkich dostępnych skrzynek):
```text
A1 LIST "" *
```

Komenda protokołu IMAP - `LIST` (wyświetlenie konkretnej skrzynki/katalogu):
```text
A1 LIST INBOX *
A1 LIST "Archive" *
```

Komenda protokołu IMAP - `CREATE <mailbox>` (utworzenie nowej skrzynki/katalogu):
```text
A1 CREATE INBOX.Archive.2012
A1 CREATE "To Read"
```

Komenda protokołu IMAP - `DELETE <mailbox>` (usunięcie skrzynki/katalogu):
```text
A1 DELETE INBOX.Archive.2012
A1 DELETE "To Read"
```

Komenda protokołu IMAP - `RENAME <oldname> <newname>` (zmiana nazwy skrzynki/katalogu):
```text
A1 RENAME "INBOX.One" "INBOX.Two"
```

Komenda protokołu IMAP - `SELECT <mailbox>` (wybranie konkretnej skrzynki):

Komenda `SELECT` pozwala na wybranie skrzynki, z którą chcemy pracować (sprawdzić wiadomości znajdujące się w niej, ...), na koncie pocztowym mamy różne skrzynki: `Inbox`, `Sent` czy `Trash`, należy wybrać skrzynkę, na której mamy zamiar wykonać pozostałe komendy.
```text
A1 SELECT INBOX
```

Komenda protokołu IMAP - `SEARCH` (pobranie identyfikatorów wiadomości w folderze):

Przykładowe parametry komendy `SEARCH`:
* `SEARCH ALL` - pobranie identyfikatorów wiadomości w folderze, identyfikatory wiadomości to liczby naturalne, wiadomości numerowane są od 1, lub identyfikowane za pomocą `UID`
* `SEARCH NEW` - pobranie identyfikatorów wiadomości, które mają ustawioną flagę oznaczającą, że wiadomość jest nowa,
* `SEARCH BODY <text>` - pobranie identyfikatorów wiadomości, w których treści znajduje się dany tekst
* `SEARCH FROM <email>` - pobranie identyfikatorów wiadomości od danego nadawcy

W odpowiedzi na komendę `SEARCH` serwer zwraca odpowiedź - prawidłowa obsługa odpowiedzi serwera na komendę `SEARCH`: sprawdzamy wszystkie linie odpowiedzi, jeśli znajdziemy taką, która rozpoczyna się od napisu `* SEARCH`, to pobieramy z niej kolejne numery wiadomości, które identyfikują odnalezione wiadomości. Jeśli natomiast takiej linii nie ma, to sprawdzamy kod odpowiedzi. Jeśli jest różny od `OK` to wyświetlamy komunikat błędu.

Komenda protokołu IMAP - `FETCH` (wyświetlenie wiadomości wraz z flagami):
```text
A1 FETCH 1:* (FLAGS)
A1 UID FETCH 1:* (FLAGS)
```

Komenda protokołu IMAP - `FETCH` (pobranie treści wiadomości o numerze 2):
```text
A1 FETCH 2 BODY[TEXT]
```

Komenda protokołu IMAP - `FETCH` (pobranie nagłówków wiadomości o numerze 1):
```text
A1 FETCH 1 BODY[HEADER]
```

Komenda protokołu IMAP - `FETCH` (pobranie całej wiadomości o numerze 1 (treść i nagłówki)):
```text
A1 FETCH 1 BODY[]
```

Komenda protokołu IMAP - `STATUS <mailbox name> <status data>` (sprawdzenie stanu skrzynki):

Gdzie `<status data>` to:
* `MESSAGES` - the number of messages in the mailbox.
* `RECENT` - the number of messages with the `\Recent` flag set.
* `UIDNEXT` - the next unique identifier value of the mailbox.
* `UIDVALIDITY` - the unique identifier validity value of the mailbox.
* `UNSEEN` - the number of messages which do not have the `\Seen` flag set.

Przykład: `TAGX STATUS Inbox (MESSAGES)`

Komenda protokołu IMAP - `EXPUNGE` (usunięcie e-maila):

Wiadomości, dla których została ustawiona flaga `\Deleted` w rzeczywistości są ciągle dostępne w skrzynce (zazwyczaj ustawienie flagi `\Deleted` powoduje przeniesienie wiadomości do innej skrzynki - kosza). Aby fizycznie usunąć wiadomość, należy wykorzystać komendę `EXPUNGE`. Poniższe polecenia oznaczają wiadomość nr 22 jako usuniętą (`A1 STORE 22 +FLAGS \Deleted`) oraz usuwają ją fizycznie ze skrzynki (`A2 EXPUNGE`).

```text
A1 STORE 22 +FLAGS \Deleted
A2 EXPUNGE
```

Komenda protokołu IMAP - `STORE` (ustawianie flag):

Daną flagę można ”włączyć” lub ”wyłączyć”. Przykładowo, poniższe polecenia ustalają flagi każdej wiadomości jako przeczytane (`A1 STORE 1:* +FLAGS \Seen` - nadanie flagi) lub nieprzeczytane (`A2 STORE 1:* -FLAGS \Seen` - zdjęcie, wyłączenie flagi):

```text
A1 STORE 1:* +FLAGS \Seen
A2 STORE 1:* -FLAGS \Seen
```

Komenda protokołu IMAP - `LOGIN <username> <password>` (logowanie do serwera):
```text
A1 LOGIN pasumcs@infumcs.edu P4SInf2017
```

Komenda protokołu IMAP - `LOGOUT` (wylogowanie z serwera):
```text
A1 LOGOUT
```

Komenda protokołu IMAP - `CLOSE` (zamknięcie skrzynki):
```text
A1 CLOSE
```

Przykładowa komunikacja z serwerem IMAP za pomocą klienta telnet (logowanie):

```text
telnet 212.182.24.27 143
Trying 212.182.24.27...
Connected to 212.182.24.27.
Escape character is '^]'.
* OK [CAPABILITY IMAP4rev1 LITERAL+ SASL-IR LOGIN-REFERRALS ID ENABLE IDLE
AUTH=PLAIN AUTH=LOGIN] Dovecot ready.
A1 LOGIN pasumcs@infumcs.edu P4SInf2017
A1 OK [CAPABILITY IMAP4rev1 LITERAL+ SASL-IR
LOGIN-REFERRALS ID ENABLE IDLE SORT SORT=DISPLAY THREAD=REFERENCES
THREAD=REFS THREAD=ORDEREDSUBJECT MULTIAPPEND URL-PARTIAL CATENATE
UNSELECT CHILDREN NAMESPACE UIDPLUS LIST-EXTENDED I18NLEVEL=1 CONDSTORE
QRESYNC ESEARCH ESORT SEARCHRES WITHIN CONTEXT=SEARCH LIST-STATUS BINARY
MOVE SPECIAL-USE QUOTA ACL RIGHTS=texk] Logged in
A2 LOGOUT
* BYE Logging out
A2 OK Logout completed.
Connection closed by foreign host.
```

Przykładowa komunikacja z serwerem IMAP za pomocą klienta telnet:

```text
telnet 212.182.24.27 143
Trying 212.182.24.27...
Connected to 212.182.24.27.
Escape character is '^]'.
* OK [CAPABILITY IMAP4rev1 LITERAL+ SASL-IR LOGIN-REFERRALS ID
ENABLE IDLE AUTH=PLAIN AUTH=LOGIN] Dovecot ready.
A1 LOGIN pasumcs@infumcs.edu P4SInf2017
A1 OK [CAPABILITY IMAP4rev1 LITERAL+ SASL-IR LOGIN-REFERRALS
ID ENABLE IDLE SORT SORT=DISPLAY THREAD=REFERENCES THREAD=REFS
THREAD=ORDEREDSUBJECT MULTIAPPEND URL-PARTIAL CATENATE UNSELECT
CHILDREN NAMESPACE UIDPLUS LIST-EXTENDED I18NLEVEL=1 CONDSTORE
QRESYNC ESEARCH ESORT SEARCHRES WITHIN CONTEXT=SEARCH LIST-STATUS
BINARY MOVE SPECIAL-USE QUOTA ACL RIGHTS=texk] Logged in
A2 SELECT Inbox
* FLAGS (\Answered \Flagged \Deleted \Seen \Draft)
* OK [PERMANENTFLAGS (\Answered \Flagged \Deleted \Seen \Draft \*)] Flags permitted.
* 2 EXISTS
* 0 RECENT
* OK [UIDVALIDITY 1491554744] UIDs valid
* OK [UIDNEXT 3] Predicted next UID
* OK [HIGHESTMODSEQ 5] Highest
A2 OK [READ-WRITE] Select completed (0.000 + 0.000 secs).
A3 SEARCH ALL
* SEARCH 1 2
A3 OK Search completed (0.001 + 0.000 secs).
A4 LIST INBOX *
* LIST (\HasNoChildren) "/" INBOX
A4 OK List completed (0.000 + 0.000 secs).
A5 FETCH 1 BODY[TEXT]
* 1 FETCH (BODY[TEXT] {36}
Test 1 Test 1 Test 1 Test 1 Test 1
)
A5 OK Fetch completed (0.001 + 0.000 secs).
A6 STATUS Inbox (MESSAGES)
* STATUS Inbox (MESSAGES 2)
A6 OK [CLIENTBUG] Status on selected mailbox completed (0.000 + 0.000 secs).
A7 LOGOUT
* BYE Logging out
A7 OK Logout completed.
Connection closed by foreign host.
```

Przykładowy flow protokołu IMAP:

*[Element graficzny dostępny w wersji PDF: [lab-08-assignment.pdf](./lab-08-assignment.pdf)]*

## Zadania

**Uwaga:** W poniższych zadaniach zakładamy, iż serwer powinien obsługiwać tylko jednego klienta w danej chwili.

Do wykonania zadań możesz wykorzystać konta pocztowe:
* Serwer `212.182.24.27`, port `143`, konto: `pasinf2017@infumcs.edu` z hasłem `P4SInf2017` (webmail: https://212.182.24.27:443)
* Serwer `212.182.24.27`, port `143`, konto: `pasinf@infumcs.edu` z hasłem `P4SInf2017` (webmail: https://212.182.24.27:443)
* Serwer `212.182.24.27`, port `143`, konto: `pasumcs@infumcs.edu` z hasłem `P4SInf2017` (webmail: https://212.182.24.27:443)

1. Wykorzystując protokół telnet, oraz serwer IMAP, zaloguj się do skrzynki i sprawdź, ile wiadomości znajduje się w poszczególnych skrzynkach. Pobierz pierwszą dostępną wiadomość, i oznacz ją jako przeczytaną. Wykorzystaj komendę protokołu IMAP - `STORE`.

2. Napisz program klienta, który połączy się z serwerem IMAP, a następnie wyświetli informację o tym, ile wiadomości znajduje się w skrzynce `Inbox`.

3. Napisz program klienta, który połączy się z serwerem IMAP, a następnie wyświetli informację o tym, ile wiadomości znajduje się we wszystkich skrzynkach łącznie.

4. Napisz program klienta, który połączy się z serwerem IMAP, a następnie sprawdzi, czy w skrzynce są nieprzeczytane wiadomości. Jeśli tak, wyświetli treść wszystkich nieprzeczytanych wiadomości oraz oznaczy je jako przeczytane (komenda `STORE` i flagi - `FLAGS`).

5. Napisz program klienta, który połączy się z serwerem IMAP, a następnie fizycznie usunie wybraną wiadomość.

6. Napisz program serwera, który działając pod adresem `127.0.0.1` oraz na określonym porcie TCP, będzie serwerem poczty, obsługującym protokół IMAP. Nie realizuj faktycznego pobierania e-maili, tylko zasymuluj jego działanie tak, żeby napisany wcześniej klient IMAP mógł pobrać wiadomości. Pamiętaj o obsłudze przypadku, gdy klient poda nie zaimplementowaną przez serwer komendę.