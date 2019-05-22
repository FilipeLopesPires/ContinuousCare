FROM node:12.2.0

WORKDIR /app

COPY ./package.json /app

RUN npm install

COPY . /app

RUN npm run build

ENV HOST 0.0.0.0

EXPOSE 3000

CMD npm start
