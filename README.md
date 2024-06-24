# OmniDock-Onboarding Case Study

## Allgemeine Hinweise

Die technische Seite von OmniDock beschäftigt sich derzeit überwiegend mit der API-Integration zu verschiedenen Marktplätzen und der Aufbereitung/Aggregation der Daten für das Frontend. Um eine erfolgreiche Integration zu erreichen, welche sich auf eine ständig ändernde API der Marktplätze anpassen lässt, sind erweiterbare/ersetzbare API-Wrapper sowie die hauseigenen Datenbankmodelle von besonderer Wichtigkeit. Gepaart mit asynchronen Routinen zum Laden der aktuellsten Daten im Hintergrund können wir das OmniDock-Team und somit auch unsere Kunden bestmöglich unterstützen. Laden, Speichern und Visualisieren sind die ersten Schritte; zum übergeordneten Ziel zählt auch das Übertragen von Daten zum Marktplatz, um eine einheitliche Operating Suite zu kreieren, die so automatisiert wie möglich agieren kann. 

Zeitaufwand: Nimm dir bitte 3-4 Stunden für die Aufgaben Zeit. Alles was nicht implementiert wurde, kann gerne auch theoretisch als Fließtext hochgeladen werden. Natürlich, je mehr Code vorhanden ist, desto besser können wir deine Programming-Skills einschätzen. Falls du Spaß daran hast, dann kannst du natürlich auch gerne länger daran arbeiten. ChatGPT oä. als Hilfe ist erlaubt. Erfahrungsgemäß stolpert ChatGPT ab und zu über blöde Fehler, der herausgegebene Code sollte in jedem Fall inspiziert werden und auf logische Fehler überprüft werden. 

## Setup 

Das OmniDock-Onboarding-Repository enthält ein nahezu leeres Django-Projekt. In diesem Projekt befinden sich zwei neu erstellte Apps: "omnidock" und "otto". Wir möchten sehen, auf welche Art und Weise du die folgenden Aufgaben löst und inwieweit deine Ansätze auch für andere Marktplätze und/oder Erweiterungen flexibel gestaltet sind. Bitte erstelle dir einen eigenen Git Branch, in dem du deine Ergebnisse teilst.

Verwende für die folgenden Aufgaben, insofern API-Requests notwendig sind, die  [OTTO Sandbox API](https://api.otto.market/docs). Wir wollen in dieser "Case Study" Informationen bei OTTO anfragen, diese speichern und über eine API öffentlich zugänglich machen. "Authentifizierung" und "Autorisierung" sind nicht notwendig, alle Django Endpunkte können öffentlich zugänglich bleiben.

**Disclaimer:** Leider sind Sandbox-Umgebungen oft nicht optimal zur Entwicklung geeignet, weshalb dir hier und da das Schummeln/Kreativsein erlaubt ist falls notwendig. Dir steht es frei, Django Local Memory Caching und SQLite zu verwenden oder PostgreSQL zusammen mit Redis über ein Docker-Setup (Muss absolut nicht sein, uns ist der Python-Code hier deutlich wichtiger als ein Docker-Setup und die Django-Config dazu). Verwende alle Libraries, die du gerne verwenden willst, ich freue mich, neue kennenzulernen! Aufgaben müssen nicht in der Reihenfolge erledigt werden, wie diese hier vorgeschlagen werden. **Es gibt kein richtig und falsch, solange die Design-Entscheidungen einen Grund haben.** Für die Sandbox Datenbank sind insgesamt 16 Orders in verschiedenen Fulfilment States hinterlegt. Es existieren weiterhin bereits 6 Shipments zu den Orders. Bei Fragen kannst du dich gerne an Sebastian wenden.


### Eventuell sinnvolle Libraries:
- [Dotenv](https://pypi.org/project/python-dotenv/)
- [Django Restframework](https://www.django-rest-framework.org/) (Zusammen mit den Serializern)



### API Credentials für die OTTO Sandbox API 

```
OTTO_SANDBOX_CLIENT_ID=a88b6d8a-c387-4f6c-9c42-c271eef291d4
OTTO_SANDBOX_CLIENT_SECRET=d122d788-755e-48cf-87c4-b0095160be28
```

## Tasks

### Task 1:

Bereite das Django-Projekt in einer Art und Weise vor, sodass andere Personen es lokal auf ihren Computern einfach zum Laufen bringen können. 

### Task 2:

Die "otto"-App benötigt die Datenbankmodelle (Django Modelle), um Orders und Shipments von OTTO selbst zu speichern. Für das Laden der Informationen von OTTO benötigen wir eine API-Wrapper Klasse. In der Praxis werden diese Klassen von Runnable-Klassen (Celery Tasks) asynchron aufgerufen um in verschiedenen Zeitintervallen Informationen zu erfragen. Für die Case Study reicht es, wenn eine Runnable Klasse (imitierter CeleryTask) bspw. "OrderTask" die Informationen abruft und sich ebenfalls um das Abspeichern der Informationen kümmert. Ein triggern der Runnable Klassen kann gerne als Management Command oder als API Endpunkt implementiert werden. 

- **ToDo:**

  - Erstelle notwendige Datenbank Modelle

  - Implementiere eine Python Klasse, welche als API Wrapper für die Otto API fungieren kann. Bevor ein API Request stattfinden kann müssen wir uns logischerweise erst einmal authentifizieren. Anschließend können Daten gelesen werden. 

  - Frage: In der Praxis haben verschiedene Third-Party-APIs verschiedene RateLimits und/oder RateLimit-Mechanismen. Wie können wir für den Fall OTTO dafür Sorge tragen, dass wir RateLimits einhalten, und wie können wir mit welchen Fehlern umgehen? **Note:** Ich vermute, dass die Sandbox API RateLimits nicht so streng nimmt, weshalb ein theoretischer Ansatz hier schon genügt. 

    

### Task 3:

Die "omnidock"-App benötigt Django Datenbank Modelle und REST Endpunkte, sodass **aggregierte** Informationen über **verschiedene** Marktplätze hin weg mittels einem API Endpunkte abfragbar sind. Die Omnidock Modelle selbst dienen zwei primären Gründen. i) Marktplatzspezifische equivalente Modelle sind semantisch ähnlich, unterscheiden sich jedoch in ihrer Syntax von Marktplatz zu Marktplatz. Omnidock Modelle sollen ein einheitliches Interface bieten können um Informationen aus den anderen Apps und Modellen abzufragen. ii) Im Laufe der Zeit werden wir vermehrt strukturierte Informationen an unsere Clienten herausgeben müssen. Hierfür ist es wichtig, dass wir eine eindeutige Sequenze von Orders, Shipments, Returns etc. erstellen können. Sprich jede Order hat eine marktplatzspezifische Order-Id und entsprechend noch eine Omnidock Order-Id (Gerne die DB Id des Modells). 

- **ToDo**:

  - Erstelle die deiner Meinung notwendigen Modelle für die erstellten Otto-Modelle. 

  - Erstelle Django Restframework Endpunkte, sodass man erfragen kann: 

    - Wie oft sich jedes Produkt verkauft hat und was dabei die Gross Einnahmen waren. (Einfache List-View reicht).
    - Welche Orders bereit sind "Fulfilled" zu werden, bzw. welche Orders bereits fulfilled wurden. Falls ein Fulfillment stattgefunden hat, dann interessiert uns hier das shippingDate zusätzlich. 

    

### Task 4:

Eine vollständige Test-Suite ist nicht notwendig. Falls du eine einfache und gute Idee hast, wie man das ganze Setup testen könnte, kannst du das natürlich ausformulieren. Setze eine minimale Postman-Collection auf (oä), sodass lokal mit deinem Django-Projekt interagiert werden kann. Füge bitte nach eigenem Ermessen Logging-Statements in deinen Code ein, sodass der Informationsfluss nachvollziehbar ist.

