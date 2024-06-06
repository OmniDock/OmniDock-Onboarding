# OmniDock-Onboarding Case Study

## Allgemeine Hinweise
Die technische Seite von OmniDock beschäftigt sich derzeit überwiegend mit der API-Integration zu verschiedenen Marktplätzen und der Aufbereitung/Aggregation der Daten für das Frontend. Um eine erfolgreiche Integration zu erreichen, welche sich auf eine ständig ändernde API der Marktplätze anpassen lässt, sind erweiterbare/ersetzbare API-Wrapper sowie die hauseigenen Datenbankmodelle von besonderer Wichtigkeit. Gepaart mit asynchronen Routinen zum Laden der aktuellsten Daten im Hintergrund können wir das OmniDock-Team und somit auch unsere Kunden bestmöglich unterstützen. Laden, Speichern und Visualisieren sind die ersten Schritte; zum übergeordneten Ziel zählt auch das Übertragen von Daten zum Marktplatz, um eine einheitliche Operating Suite zu kreieren, die so automatisiert wie möglich agieren kann.

## Setup 
Das OmniDock-Onboarding-Repository enthält ein nahezu leeres Django-Projekt. In diesem Projekt befinden sich zwei neu erstellte Apps: "omnidock" und "marketplace". Wir möchten sehen, auf welche Art und Weise du die folgenden Aufgaben löst und inwieweit deine Ansätze auch für andere Marktplätze und/oder Erweiterungen flexibel gestaltet sind. Bitte erstelle dir einen eigenen Git Branch, in dem du deine Ergebnisse teilst.

Verwende für die folgenden Aufgaben, insofern API-Requests notwendig sind, die OTTO API (Sandbox). Wir wollen in dieser "Case Study" Informationen bei OTTO anfragen, diese speichern und über eine API öffentlich zugänglich machen. "Authentifizierung" und "Autorisierung" sind nicht notwendig, alle Endpunkte können öffentlich zugänglich bleiben.

**Disclaimer:** Leider sind Sandbox-Umgebungen oft nicht optimal zur Entwicklung geeignet, weshalb dir hier und da das Schummeln/Kreativsein erlaubt ist falls notwendig. Dir steht es frei, Django Local Memory Caching und SQLite zu verwenden oder PostgreSQL zusammen mit Redis über ein Docker-Setup (Muss absolut nicht sein, uns ist der Python-Code hier deutlich wichtiger als ein Docker-Setup und die Django-Config dazu). Verwende alle Libraries, die du gerne verwenden willst, ich freue mich, neue kennenzulernen! Aufgaben müssen nicht in der Reihenfolge erledigt werden, wie diese hier vorgeschlagen werden. Es gibt kein richtig und falsch, solange die Design-Entscheidungen einen Grund haben.

#### API Credentials für die OTTO Sandbox API 
```
OTTO_SANDBOX_CLIENT_ID=a88b6d8a-c387-4f6c-9c42-c271eef291d4
OTTO_SANDBOX_CLIENT_SECRET=d122d788-755e-48cf-87c4-b0095160be28
```



### Task 1:
Bereite das Django-Projekt in einer Art und Weise vor, sodass andere Personen es lokal auf ihren Computern einfach zum Laufen bringen können.

### Task 2:
Die "omnidock"-App benötigt Modelle und Endpunkte, sodass aggregierte Informationen über Orders und Shipments über API-Endpunkte anfragbar sind. Die OmniDock-Modelle sollten je nach Auswahl natürlich nicht nur OTTO Orders und Shipments und Orders herausgeben, sondern ebenfalls theoretisch in der Lage sein, auf weitere Apps und Datenbankmodelle zuzugreifen. Du kannst es dir vorstellen, als eine Art "Super"-Klasse über andere Modelle aus anderen Apps mit dem gleichen semantischen Hintergrund. Syntaktisch unterscheiden sich die Modelle von Marktplatz zu Marktplatz. **Etwas mehr Kontext zum Verständnis:** In der Praxis haben wir verschiedene Clients, welche in der Zukunft natürlich nur ihre eigenen aggregierten Informationen sehen dürfen. Die Aufspaltung und Trennung wird über zusätzliche Modelle wie Client und ItemMaster geregelt. Ein Client hat verschiedene ItemMaster. ItemMaster-Instanzen haben eine omnidockSku als Attribut hinterlegt. Dies ist die Referenz, welche wir auf verschiedenen Marktplätzen angeben, um nachverfolgen zu können, zu wem welche Orders und welche Shipments (o.ä.) gehört. Für die Case Study ist dies nicht nötig.

Wir würden gerne schlussendlich über die API sehen wollen
- Wie oft sich jedes Produkt verkauft hat und was die Gross Einnahmen dabei waren.
- Welche Orders bereit sind Fulfilled zu werden, bzw. welche Orders bereits fulfilled wurden. Falls ein Fulfillment stattgefunden hat, dann interessiert uns das shipping Date hier zusätzlich.


### Task 3:
Die "otto"-App benötigt die Datenbankmodelle, um Orders und Shipments von OTTO selbst zu speichern. Für das Laden der Informationen von OTTO brauchen wir einen API-Wrapper. In der Praxis verwenden wir zurzeit Celery-Tasks, welche zu Routinen zusammengeschlossen sind und alle x Minuten neue Informationen abfragen. Du musst kein neues Celery-Setup bauen, es reicht, wenn wir eine API-Wrapper-Klasse/Funktionen haben, welche von weiteren Runnable-Klassen (imitierter Celery-Task) aufgerufen werden. Die "Runnable"-Klassen müssen sich ebenfalls um die Abspeicherung der Daten kümmern (Es reicht wenn du die wichtigsten Informationen speicherst, wir brauchen hier nicht alle). In dieser Case Study können die Runnable-Klassen entweder über Management Commands oder einen API-Endpunkt in der otto-App getriggert werden. In der Praxis haben verschiedene Third-Party-APIs verschiedene RateLimits und/oder RateLimit-Mechanismen. Wie können wir für den Fall OTTO dafür Sorge tragen, dass wir RateLimits einhalten, und wie können wir mit welchen Fehlern umgehen? **Note:** Ich vermute, dass die Sandbox API RateLimits nicht so streng nimmt, weshalb ein theoretischer Ansatz hier schon genügt. 

### Task 4:
Eine vollständige Test-Suite ist nicht notwendig. Falls du eine einfache und gute Idee hast, wie man das ganze Setup testen könnte, kannst du das natürlich ausformulieren. Setze eine minimale Postman-Collection auf, sodass lokal mit deinem Django-Projekt interagiert werden kann. Füge bitte nach eigenem Ermessen Logging-Statements in deinen Code ein, sodass der Informationsfluss nachvollziehbar ist.

Für die Sandbox Datenbank sind insgesamt 16 Orders in verschiedenen Fulfilment States hinterlegt. Es existieren weiterhin bereits 6 Shipments zu den Orders. Bei Fragen kannst du dich gerne an Sebastian wenden. 
