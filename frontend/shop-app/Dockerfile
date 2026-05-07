# Dockerfile
FROM node:18

WORKDIR /shop-app

# Kopiere nur die notwendigen Dateien
COPY /package.json /package-lock.json ./

# Installiere die Abhängigkeiten
RUN npm install

# Kopiere den Rest des Projekts
COPY . .

# Baue die Anwendung für die Produktion
RUN npm run build

# Starte die Anwendung im Produktionsmodus
CMD ["npm", "run", "preview"]

# Exponiere den Port, auf dem die App läuft
EXPOSE 3000
