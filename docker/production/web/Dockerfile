FROM node:9.11.1-alpine

# install simple http server for serving static content
RUN npm install -g http-server && npm install -g @vue/cli

COPY ./web/package*.json /tmp/

RUN cd /tmp && npm install

WORKDIR /app

RUN cp -a /tmp/node_modules /app/

RUN ./web/npm run build

COPY ./web/dist/* /app

EXPOSE 8040

ENTRYPOINT [ "http-server", "-p", "8040", "dist" ]