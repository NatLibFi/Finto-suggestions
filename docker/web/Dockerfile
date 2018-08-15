FROM node:alpine

COPY ./web/package.json /tmp/package.json

# install node_modules first on a temp directory, after which it is copied to app directory
# otherwise a new docker build will be triggered on each node package version change
RUN cd /tmp && npm install && mkdir -p /app && cp -a /tmp/node_modules /app/ && npm install -g http-server

WORKDIR /app

COPY ./web/* /app/

EXPOSE 8040

ENTRYPOINT [ "npm", "run", "serve" ]
