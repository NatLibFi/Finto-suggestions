FROM node:10.13.0-alpine

# install simple http server for serving static content
RUN npm install -g http-server

COPY ./web/package*.json /tmp/

RUN cd /tmp && npm install

WORKDIR /app

RUN cp -a /tmp/node_modules /app/

COPY ./web/* /app/

RUN vue-cli-service build ./src/main.js --modern

EXPOSE 8040

ENTRYPOINT [ "http-server", "-p", "8040", "dist" ]