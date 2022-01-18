# start with the nodejs image, calling it 'build'
FROM node:14-alpine as build
RUN apk add --update --no-cache python3 make g++

# install node modules
# COPY package.json yarn.lock /
COPY package.json /
RUN yarn

# build assets
COPY . .
EXPOSE 3000

RUN yarn build

CMD ["yarn", "start"]

## change base image
#FROM nginx:alpine
#
## copy built files from the 'build' container into the nginx container
#COPY --from=build dist /usr/share/nginx/html
