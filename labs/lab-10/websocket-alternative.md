**Uruchom echo-server lokalnie za pomocą dokera**

Użyj tego polecenia, aby uruchomić najnowszy dostępny kontener. Potwierdź, że serwer echo-server jest uruchomiony, wskazując w przeglądarce `http://localhost:10000/.ws`

```bash
docker run --detach -p 10000:8080 jmalloc/echo-server
```

Zobaczysz interfejs, w którym możesz wysłać wiadomość i poprosić o jej potwierdzenie.

*[Element graficzny dostępny w wersji PDF: [websocket-alternative.pdf](./websocket-alternative.pdf)]*

Inaczej - otwarte źródło jego projektu echo-server.

Lub https://www.piesocket.com/blog/echo-websocket-org-alternative -> https://www.piesocket.com/websocket-tester