# ---
# actual image
# ---
FROM node:14-alpine

# install prerequisites for node-gyp
RUN apk add --update --no-cache python3 make g++

# set current directory
WORKDIR /app

# install dependencies
COPY package.json package-lock.json ./
RUN npm ci && npm cache clean --force

# copy all files and run build
COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "start"]
