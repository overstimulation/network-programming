# Programowanie Aplikacji Sieciowych - Laboratorium 6

**Protokół SMTP** - Simple Mail Transfer Protocol (Protokół Prostego Przesyłania Poczty), RFC 2821.
Protokół niezawodnego (gniazda TCP) przesyłania wiadomości tekstowych (e-mail) za pomocą prostych komend tekstowych. W protokole SMTP komendy są ciągami znaków zakończonych znakiem niedrukowalnym `<CRLF>` (czyli `\r\n`).

**Protokół ESMTP** - Extended SMTP (ESMTP) lub Enhanced SMTP jest rozszerzeniem protokołu SMTP powstałym na skutek wielu jego ograniczeń (RFC 1869). Rozszerzenia te to głównie: nowe komendy SMTP: `EHLO`, `AUTH LOGIN` oraz nowe parametry poleceń `MAIL FROM` i `RCPT TO`.

Komenda `AUTH LOGIN` to rozszerzenie protokołu Simple Mail Transfer Protocol o mechanizmy uwierzytelniania. Każda z nich do komunikacji pomiędzy serwerem a klientem stosuje kodowanie Base64, które samo w sobie nie zapewnia bezpieczeństwa danych. Uwierzytelnianie (ang. authentication) to proces polegający na potwierdzeniu zadeklarowanej tożsamości podmiotu biorącego udział w procesie komunikacji. Celem uwierzytelniania jest uzyskanie określonego poziomu pewności, że dany podmiot jest w rzeczywistości tym, za który się podaje. Wprowadzenie tej usługi uniemożliwia wysyłania wiadomości z konta użytkownika przez osoby do tego nieuprawnione. Osoba próbująca wysłać wiadomość jest proszona o podanie loginu i hasła do konta. Aby skorzystać z autoryzacji, klient powinien zamiast standardowego powitania `HELO` użyć `EHLO`, które umożliwi wykorzystanie rozszerzonego zestawu poleceń SMTP. W odpowiedzi serwer SMTP powinien zwrócić w powitaniu ciąg znaków `AUTH`, a po nim dostępne metody uwierzytelniania. Opisany jest w RFC 2554.

Przykładowy flow protokołu SMTP:

*[Element graficzny dostępny w wersji PDF: [lab-06-assignment.pdf](./lab-06-assignment.pdf)]*

Przykładowa komunikacja z serwerem ESMTP za pomocą klienta telnet:

```text
telnet interia.pl 587
Trying 217.74.65.23...
Connected to interia.pl.
Escape character is '^]'.
220 ESMTP INTERIA.PL
EHLO nazwa_komputra
250-poczta.interia.pl
250-PIPELINING
250-SIZE 157286400
250-STARTTLS
250-AUTH PLAIN LOGIN
250-AUTH=PLAIN LOGIN
250-ENHANCEDSTATUSCODES
250 8BITMIME
AUTH LOGIN
334 VXNlcm5hbWU6
nazwa_uzytkownika_zakodowana_base64
334 UGFzc3dvcmQ6
haslo_zakodowane_base64
235 2.7.0 Authentication successful
MAIL FROM: <nadawca@gmail.com>
250 2.1.0 Ok
RCPT TO: <odbiorca@interia.pl>
250 2.1.5 Ok
DATA
354 End data with <CR><LF>.<CR><LF>
To: <odbiorca@interia.pl>
From: <nadawca@gmail.com>
Subject: Mozemy podac temat emaila

Tu wstawiamy tresc wiadomosci
.
250 OK. ID: 1488395c08fea12a
QUIT
221 2.0.0 Bye
Connection closed by foreign host.
```

**MIME** - (ang. Multipurpose Internet Mail Extensions) to standard stosowany przy przesyłaniu poczty elektronicznej (ang. e-mail). MIME definiuje budowę komunikatu poczty elektronicznej. MIME, to inaczej wielozadaniowe rozszerzenie poczty w Internecie, jest standardem pozwalającym przesyłać w sieci Internet wszelkie dane (teksty, grafikę, zdjęcia, dźwięki, muzykę, programy) za pomocą standardowych narzędzi, takich jak poczta, newsy czy WWW. Wbrew swojej nazwie (Mail Extension, czyli rozszerzenie poczty), zastosowanie MIME nie ogranicza się wyłącznie do plików przesyłanych pocztą. Standard ten rozwinął się na tyle, że wprowadzono go także do innych systemów przesyłania danych i obecnie jest to niekwestionowany standard we wszystkich usługach Internetu, których podstawowym zadaniem jest przesyłanie tekstu.

Każda przesyłka pocztowa składa się z dwu zasadniczych częsci: nagłówków (coś na kształt „koperty”) i treści przesyłki. Zawartość nagłówków szczegółowo określają następujące dokumenty: RFC822 i RFC1521. Nagłówki oddzielone są od treści listu jedną linią pustą i określają, np. :
* **From:** adres nadawcy
* **To:** adres dobiorcy listu
* **Subject:** temat listu
* **Cc:** adres, na który została wysłana kopia listu

Przesyłki MIME zawierają dodatkowo nagłówek:
* **Mime-Version: 1.0** który identyfikuje wszystkie takie przesyłki
* **Content-Type:** rodzaj zawartości przesyłki
* **Content-Transfer-Encoding:** sposób jej kodowania
* **Content-Length:** długość przesyłki (nie zawsze występuje)
* **Content-description:** opis zawartości przesyłki

Przykładowy nagłówek, Content-Type typu MIME wskazuje typ zawartości wiadomości. Składa się z typu i podtypu. Jest dwuczęściowym identyfikatorem formatu plików w Internecie. Lista popularnych typów: https://pl.wikipedia.org/wiki/Typ_MIME.

Przykład wysyłania e-maila z załącznikiem (plikiem tekstowym) z wykorzystaniem standardu MIME:

```text
telnet interia.pl 587
Trying 217.74.65.23...
Connected to interia.pl.
Escape character is '^]'.
220 ESMTP INTERIA.PL
HELO kasiula
250 poczta.interia.pl
AUTH LOGIN
334 VXNlcm5hbWU6
cGFzMjAxN0BpbnRlcmlhLnBs
334 UGFzc3dvcmQ6
UDRTSW5mMjAxNw==
235 2.7.0 Authentication successful
MAIL FROM: <pas2017@interia.pl>
250 2.1.0 Ok
RCPT TO: <pas2017@interia.pl>
250 2.1.5 Ok
RCPT TO: <katarzyna.mazur@gmail.com>
250 2.1.5 Ok
DATA
354 End data with <CR><LF>.<CR><LF>
From: Nathaniel Borenstein <nsb@bellcore.com>
To: Ned Freed <ned@innosoft.com>
Subject: Sample message
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary=sep
--sep
To
jest
tresc wiadomosci
--sep
Content-Type: text/x-log; name=\"text.log\"
Content-Disposition: attachment; filename=\"text.log\"
Content-Transfer-Encoding: base64
LyoKKiogc2VsZWN0c2VydmVyLmMgLS0gYSBjaGVlenkgbXVsdGlwZXJzb24gY2hh
dCBzZXJ2ZXIKKi8KCiNpbmNsdWRlIDxzdGRpby5oPgojaW5jbHVkZSA8c3RkbGli
Lmg+CiNpbmNsdWRlIDxzdHJpbmcuaD4KI2luY2x1ZGUgPHVuaXN0ZC5oPgojaW5j
bHVkZSA8c3lzL3R5cGVzLmg+CiNpbmNsdWRlIDxzeXMvc29ja2V0Lmg+CiNpbmNs
...
dCBzb3VsZCBuZXZlciBlbmQhCiAgICAKICAgIHJldHVybiAwOwp9Cgo=
--sep--
.
QUIT
```

**E-mail Spoofing**
Informacje na temat wysyłającego email w e-mail (Pole „Od”) może być łatwo sfałszowana. Jest to często stosowana technika przez spam by ukryć pochodzenie ich wiadomości e-mail co mogłoby prowadzić do problemów takich jak błędne przekierowanie wiadomości po jej niedostarczeniu. E-mail adres spoofing jest tworzone na podobnej zasadzie jak pisanie podrabianego powrotnego adresu korzystając z czasu potrzebnego na dostarczenie wiadomości. Tak długo jak list pasuje do protokołu (znaczki, kod pocztowy), protokół SMTP wyśle wiadomość.

## Zadania

**Uwaga:** W poniższych zadaniach zakładamy, iż serwer powinien obsługiwać tylko jednego klienta w danej chwili.

Do wykonania zadań możesz wykorzystać konta pocztowe:
* `pas2017@interia.pl` z hasłem `P4SInf2017`
* `pasinf2017@interia.pl` z hasłem `P4SInf2017`

1. Wykorzystując protokół telnet, oraz serwer ESMTP działający pod adresem `interia.pl` na porcie `587` wyślij wiadomość e-mail używając komend protokołu ESMTP.

2. Wykorzystując protokół telnet, oraz serwer ESMTP działający pod adresem `interia.pl` na porcie `587` wyślij wiadomość e-mail do kilku odbiorców używając komend protokołu ESMTP.

3. Wykorzystując protokół telnet, oraz serwer ESMTP działający pod adresem `interia.pl` na porcie `587` wyślij wiadomość spoofed email (z podmienionym adresem nadawcy) używając komend protokołu ESMTP.

4. Wykorzystując protokół telnet, oraz serwer ESMTP działający pod adresem `interia.pl` na porcie `587` wyślij wiadomość e-mail używając komend protokołu ESMTP. Do wiadomości dodaj załącznik - dowolny plik tekstowy (sprawdź format MIME: Multipart i Content-Type). Możesz wykorzystać `openssl` do przekonwertowania pliku: `cat plik | openssl base64`.

5. Wykorzystując protokół telnet, oraz serwer ESMTP działający pod adresem `interia.pl` na porcie `587` wyślij wiadomość e-mail używając komend protokołu ESMTP. Do wiadomości dodaj załącznik - dowolny obrazek (sprawdź format MIME: Multipart i Content-Type). Możesz wykorzystać `openssl` do przekonwertowania obrazka: `cat obrazek | openssl base64`.

6. Napisz program klienta, który połączy się z serwerem ESMTP działającym pod adresem `interia.pl` na porcie `587`, a następnie wyśle wiadomość e-mail używając komend protokołu ESMTP. O adres nadawcy, odbiorcy (odbiorców), temat wiadomości i jej treść zapytaj użytkownika.

7. Napisz program klienta, który połączy się z serwerem ESMTP działającym pod adresem `interia.pl` na porcie `587`, a następnie wyśle wiadomość e-mail używając komend protokołu ESMTP. Do wiadomości dodaj załącznik - dowolny plik tekstowy (sprawdź format MIME: Multipart i Content-Type). Nie wykorzystuj gotowych bibliotek. O adres nadawcy, odbiorcy (odbiorców), temat wiadomości i jej treść zapytaj użytkownika.

8. Napisz program klienta, który połączy się z serwerem ESMTP działającym pod adresem `interia.pl` na porcie `587`, a następnie wyśle wiadomość e-mail używając komend protokołu ESMTP. Do wiadomości dodaj załącznik - dowolny obrazek (sprawdź format MIME: Multipart i Content-Type). Nie wykorzystuj gotowych bibliotek. O adres nadawcy, odbiorcy (odbiorców), temat wiadomości i jej treść zapytaj użytkownika.

9. Napisz program klienta, który połączy się z serwerem ESMTP działającym pod adresem `interia.pl` na porcie `587`, a następnie wyśle wiadomość e-mail używając komend protokołu ESMTP. Treść wiadomości powinna zostać sformatowana za pomocą tagów HTML, przykładowo: `<b>pogrubienie</b>`, `<i>pochylenie</i>`, `<u>podkreślenie</u>` i innych wybranych.

10. Napisz program serwera, który działając pod adresem `127.0.0.1` oraz na określonym porcie TCP, będzie serwerem poczty, obsługującym protokół SMTP. Nie realizuj faktycznego wysyłania e-maila, tylko zasymuluj jego działanie tak, żeby napisany wcześniej klient SMTP myślał, że wiadomość została wysłana. Pamiętaj o obsłudze przypadku, gdy klient poda nie zaimplementowaną przez serwer komendę.