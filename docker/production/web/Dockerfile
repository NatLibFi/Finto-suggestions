FROM node:10.13.0-alpine

# install simple http server for serving static content
RUN npm install -g http-server && npm install -g @vue/cli && npm install @vue/cli-service-global

COPY ./web/package*.json /tmp/

RUN cd /tmp && npm install

WORKDIR /app

RUN cp -a /tmp/node_modules /app/

COPY ./web/* /app/

RUN echo "NODE_ENV=development \
VUE_APP_BASE_DOMAIN=${BASE_DOMAIN} \
VUE_APP_GITHUB_CLIENT_ID=${GITHUB_CLIENT_ID}" > /app/.env.production

RUN vue build main.js

EXPOSE 8040

ENTRYPOINT [ "http-server", "-p", "8040", "dist" ]