FROM node:10.14.0-alpine as build-stage

# install simple http server for serving static content
RUN npm install -g @vue/cli && npm install @vue/cli-service-global

COPY ./web/package*.json /tmp/

RUN cd /tmp && npm install && npm audit fix

RUN npm i lockr

WORKDIR /app

RUN cp -a /tmp/node_modules /app/

COPY ./web/. /app/

RUN npm run build:staging

FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html

EXPOSE 8040

ENTRYPOINT ["nginx", "-g", "daemon off;"]