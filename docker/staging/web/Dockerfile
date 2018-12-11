FROM node:10.13.0-alpine

# install simple http server for serving static content
RUN npm install -g http-server && npm install -g @vue/cli && npm install @vue/cli-service-global

COPY ./web/package*.json /tmp/

RUN cd /tmp && npm install

WORKDIR /app

RUN cp -a /tmp/node_modules /app/

COPY ./web/. /app/

RUN npm run build:staging

EXPOSE 8040

ENTRYPOINT [ "http-server", "-p", "8040", "dist" ]