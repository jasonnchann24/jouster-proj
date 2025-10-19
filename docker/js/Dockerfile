FROM node:22.12-slim

WORKDIR /app

COPY client/package*.json ./

RUN npm install

COPY client/ .

EXPOSE 3000

CMD ["npm", "run", "dev"]