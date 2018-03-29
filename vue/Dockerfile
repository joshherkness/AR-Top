FROM node:alpine

ENV PATH=$PATH:/home/node/.npm-global/bin
ENV NPM_CONFIG_LOGLEVEL info

WORKDIR /app

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY package*.json ./

RUN npm install

# Bundle app source
COPY . .

RUN npm install http-server -g

RUN npm run build

CMD [ "http-server", "dist", "-p", "8081" ]

