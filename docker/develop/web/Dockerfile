FROM node:10.14.0-alpine

COPY ./web/package*.json /tmp/

# install node_modules first on a temp directory, after which it is copied to app directory
# otherwise a new docker build will be triggered on each node package version change
# RUN cd /tmp && npm install && mkdir -p /app && cp -a /tmp/node_modules /app/ && npm install -g http-server
RUN cd /tmp && npm install && npm audit fix

#RUN npm install -g yarn
# RUN npm install --save store
#RUN yarn add @caohenghu/vue-colorpicker
RUN npm i lockr

WORKDIR /app

RUN cp -a /tmp/node_modules /app/

COPY ./web/* /app/

EXPOSE 8040

ENTRYPOINT [ "npm", "run", "serve" ]