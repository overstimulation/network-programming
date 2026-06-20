# Programowanie Aplikacji Sieciowych - Laboratorium 7

**Protokół POP3 (RFC1939)** - protokół internetowy z warstwy aplikacji pozwalający na odbiór poczty elektronicznej ze zdalnego serwera do lokalnego komputera poprzez połączenie TCP/IP. Protokół POP jest protokołem tekstowym, czyli w odróżnieniu od protokołu binarnego, czytelnym dla człowieka. Komunikacja między klientem pocztowym a serwerem odbywa się za pomocą czteroliterowych poleceń. POP3 wykorzystuje 2 porty: port niezabezpieczony: 110, port zabezpieczony: 995. POP3 to protokół obsługi poczty elektronicznej opisujący sposób wymiany informacji między klientem a serwerem. Umożliwia przechowywanie nadchodzących wiadomości na serwerze internetowym do czasu pobrania ich przez program zainstalowany na komputerze użytkownika.

Podstawowe informacje:
* Komendy protokołu POP3 składają się ze słowa **kluczowego** po którym pojawia się jeden bądź więcej **argumentów**. Słowa te wraz z argumentami są drukowalnymi znakami w kodzie ASCII i są oddzielone od siebie pojedynczą spacją.
* Słowa **kluczowe** mają długość trzech lub czterech liter.
* Każdy **argument** może mieć maksymalnie 40 liter długości.
* Odpowiedzi w POP3 składają się ze wskaźnika statusu oraz słowa kluczowego po którym następuje informacja dodatkowa. Wskaźnik statusu może przyjmować jedną z dwóch możliwości : pozytywny (`+OK.`) i negatywny (`-ERR`).
* Zarówno komendy, jak i odpowiedzi protokołu POP3 zakończone są znakiem niedrukowalnym `<CRLF>` (czyli `\r\n`).
* Odpowiedzi na niektóre komendy są dłuższe od jednej linii. W tych przypadkach po przesłaniu pierwszej linii odpowiedzi wysyłane są następne, każda zakończona parą `<CRLF>`. Kiedy zostaną już przesłane wszystkie linie odpowiedzi przesyła się specjalną linię oznaczającą linię ostatnią. Zawiera ona 8 znaków zakończenia (w kodzie dziesiętnym: 046, . - kropkę) i parę `<CRLF>`.
* Sesja POP3 w czasie swego trwania przechodzi przez wiele stanów: autoryzacji, transakcji i aktualizacji.
* Istnieją dwie wersje standardu: POP2 obowiązujący w latach 80-tych i wymagający dodatkowo do wysyłania wiadomości protokołu SMTP, oraz najnowszy POP3, który może być używany niezależnie od SMTP.
* Tak jak w przypadku protokołu SMTP, największą wadą POP3 jest fakt, iż cała komunikacja pomiędzy klientem i serwerem POP3 odbywa się przy pomocy jawnego tekstu. POP3 zawiera mechanizmy autoryzacji, gdzie pomiędzy klientem i serwerem informacje autoryzujące użytkownika w systemie przesyłane są tekstem niezaszyfrowanym informacje autoryzujące użytkownika w systemie. Poufność tych danych jest krytyczna dla systemu.

Najważniejsze komendy protokołu POP3:
* `USER <username>` - wysyła do serwera login (czystym tekstem)
* `PASS <password>` - wysyła do serwera hasło (czystym tekstem)
* `STAT` - wyświetla liczbę wiadomości w skrzynce oraz ich rozmiar w bajtach
* `LIST` - wyświetla liczbę wiadomości w skrzynce oraz ich rozmiar w bajtach a następnie wyświetla po kolei numer każdej wiadomości i jej rozmiar w bajtach
* `RETR <number>` - wyświetla wiadomość o danym numerze, wiadomości numerowane są od 1
* `DELE <number>` - usuwa ze skrzynki wiadomość o danym numerze, wiadomości numerowane są od 1
* `QUIT` - zakończenie komunikacji z serwerem

Przykładowa komunikacja z serwerem POP3 za pomocą klienta telnet:

```text
telnet interia.pl 110
Trying 217.74.65.23...
Connected to interia.pl.
Escape character is '^]'.
+OK 7ba150688b0b94dd
USER pasinf2017@interia.pl
+OK Tell me your password.
PASS P4SInf2017
+OK Welcome aboard! You have 17 messages.
STAT
+OK 17 22846
LIST
+OK Scan list follows:
1 1321
2 1319
3 1319
4 1337
5 1311
6 1255
7 1255
8 1257
9 1255
10 1255
11 1253
12 1255
13 1257
14 1255
15 1311
16 1255
17 2376
.
RETR 8
+OK Message follows
Received: from fmi10.pf.interia.pl (fmi10.pf.interia.pl [127.0.0.1])
        by poczta.interia.pl (INTERIA.PL) with ESMTP id C8761A02A7;
        Thu,  6 Apr 2017 11:15:41 +0200 (CEST)
X-Interia-R: Interia
X-Interia-R-IP: 37.47.6.58
X-Interia-R-Helo: <nazwa>
Received: from nazwa (public-gprs351993.centertel.pl [37.47.6.58])
        by poczta.interia.pl (INTERIA.PL) with ESMTPA;
        Thu,  6 Apr 2017 11:15:41 +0200 (CEST)
From: <pasinf2017@interia.pl>
To: <pawel1470@yahoo.com>
Subject: <testPB>
X-Interia-Antivirus: OK
Message-Id: <20170406091541.C8761A02A7@poczta.interia.pl>
Date: Thu,  6 Apr 2017 11:15:41 +0200 (CEST)
X-IPL-POID: 4
X-IPL-SAS-SPAS: 4.2
X-IPL-SAS-UREP: 0
X-IPL-SAS-UREP-PRIV: 0
X-IPL-Envelope-To: pasinf2017@interia.pl
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed; d=interia.pl;
        s=biztos; t=1491470142;
        bh=47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=;
        h=X-Interia-R:X-Interia-R-IP:X-Interia-R-Helo:From:To:Subject:
         X-Interia-Antivirus:Message-Id:Date:X-IPL-POID:X-IPL-SAS-SPAS:
         X-IPL-SAS-UREP:X-IPL-SAS-UREP-PRIV:X-IPL-Envelope-To;
        b=Ryqyh+MZDsZWQTf6b3apEPAl1Hxgq0S2jV9Crr3kIqR+nfW/JW9pf5XtDVC2tx8e/
         RiSFF20dS6Q+agei2dl2na37nT0F9wd6Hkdi6Us+axuWJWiH4iXA8PFXiBrv+2E9kO
         hNDWJLjuZhBDhCX05iatyp/5H5MY+Jlf/0qmXLKs=
.
QUIT
+OK Done
Connection closed by foreign host.
```

Przykładowy flow protokołu POP3:

*[Element graficzny dostępny w wersji PDF: [lab-07-assignment.pdf](./lab-07-assignment.pdf)]*

## Zadania

**Uwaga:** W poniższych zadaniach zakładamy, iż serwer powinien obsługiwać tylko jednego klienta w danej chwili.

Do wykonania zadań możesz wykorzystać konta pocztowe:
* Serwer `interia.pl`, port `110`, konto: `pas2017@interia.pl` z hasłem `P4SInf2017` (webmail: https://poczta.interia.pl/)
* Serwer `interia.pl`, port `110`, konto: `pasinf2017@interia.pl` z hasłem `P4SInf2017` (webmail: https://poczta.interia.pl/)
* Serwer `212.182.24.27`, port `110`, konto: `pasinf2017@infumcs.edu` z hasłem `P4SInf2017` (webmail: https://212.182.24.27:443)
* Serwer `212.182.24.27`, port `110`, konto: `pasinf@infumcs.edu` z hasłem `P4SInf2017` (webmail: https://212.182.24.27:443)
* Serwer `212.182.24.27`, port `110`, konto: `pasumcs@infumcs.edu` z hasłem `P4SInf2017` (webmail: https://212.182.24.27:443)

1. Wykorzystując protokół telnet, oraz wybrany serwer POP3, sprawdź, ile wiadomości znajduje się w skrzynce.

2. Wykorzystując protokół telnet, oraz wybrany serwer POP3, sprawdź, ile bajtów (w sumie) zajmują wiadomości znajdujące się w skrzynce.

3. Wykorzystując protokół telnet, oraz wybrany serwer POP3, sprawdź, ile bajtów zajmuje każda wiadomość (z osobna) znajdująca się w skrzynce.

4. Wykorzystując protokół telnet, oraz wybrany serwer POP3, wyświetl treść wiadomości o największym rozmiarze.

5. Wykorzystując protokół telnet, oraz wybrany serwer POP3, usuń wiadomość o najmniejszym rozmiarze.

6. Napisz program klienta, który połączy się z wybranym serwerem POP3, a następnie wyświetli informację o tym, ile wiadomości znajduje się w skrzynce.

7. Napisz program klienta, który połączy się z wybranym serwerem POP3, a następnie wyświetli informację o tym, ile bajtów (w sumie) zajmują wiadomości znajdujące się w skrzynce.

8. Napisz program klienta, który połączy się z wybranym serwerem POP3, a następnie wyświetli informację o tym, ile bajtów zajmuje każda wiadomość (z osobna) znajdująca się w skrzynce.

9. Napisz program klienta, który połączy się z wybranym serwerem POP3, a następnie wyświetli treść wiadomości o największym rozmiarze.

10. Napisz program klienta, który połączy się z wybranym serwerem POP3, a następnie wyświetli wszystkie wiadomości znajdujące się w skrzynce.

11. Napisz program klienta, który połączy się z wybranym serwerem POP3, a następnie pobierze z serwera wiadomość z załącznikiem (obrazkiem) i zapisze obrazek na dysk. Nazwa obrazka musi zgadzać się z nazwą załącznika podaną w mailu. Pamiętaj, że do przesyłania załączników binarnych w poczcie elektronicznej wykorzystywane jest kodowanie `Base64`.

12. Napisz program serwera, który działając pod adresem `127.0.0.1` oraz na określonym porcie TCP, będzie serwerem poczty, obsługującym protokół POP3. Nie realizuj faktycznego pobierania e-maili, tylko zasymuluj jego działanie tak, żeby napisany wcześniej klient POP3 mógł pobrać wiadomości. Pamiętaj o obsłudze przypadku, gdy klient poda nie zaimplementowaną przez serwer komendę.