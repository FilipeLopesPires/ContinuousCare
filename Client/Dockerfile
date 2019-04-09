FROM node:latest

WORKDIR /app

COPY ./package.json /app

RUN npm install

COPY . /app

RUN git clone https://github.com/euvl/vue-js-modal /app/plugins/vue-js-modal
RUN git clone https://github.com/apexcharts/vue-apexcharts /app/plugins/vue-apexcharts

RUN npm run build

ENV HOST 0.0.0.0

EXPOSE 3000

CMD npm start
