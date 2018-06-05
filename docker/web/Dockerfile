FROM node:alpine

ADD ./web/package.json /tmp/package.json

# install node_modules first on a temp directory, after which it is copied to app directory
# otherwise a new docker build will be triggered on each node package version change
RUN cd /tmp && npm install && mkdir -p /app && cp -a /tmp/node_modules /app/

WORKDIR /app
RUN npm install

COPY ./web /app

EXPOSE 8040

CMD [ "npm", "run", "serve" ]
