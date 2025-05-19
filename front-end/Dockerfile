FROM node:23-alpine AS development

WORKDIR /app

COPY package*.json .

RUN npm install

COPY . ./

CMD [ "npm", "start"]
