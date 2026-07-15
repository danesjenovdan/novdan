# ---
# build stage image
# ---
FROM node:26-alpine AS build

# set current directory
WORKDIR /app

# install dependencies
COPY package.json package-lock.json ./
RUN npm ci

# copy source code
COPY assets ./assets
COPY components ./components
COPY pages ./pages
COPY public ./public
COPY .prettierrc.json eslint.config.js nuxt.config.js ./

# set environment variables
ARG NUXT_API_BASE
ENV NUXT_API_BASE=${NUXT_API_BASE}
ARG NUXT_API_BASE_BROWSER
ENV NUXT_API_BASE_BROWSER=${NUXT_API_BASE_BROWSER}

# set NODE_ENV to production
ENV NODE_ENV=production

# run the build
RUN npm run build

# ---
# actual image
# ---
FROM node:26-alpine

# set current directory
WORKDIR /app

# copy built files
COPY --from=build /app/.output ./

# set NODE_ENV to production
ENV NODE_ENV=production

EXPOSE 3000

CMD ["node", "server/index.mjs"]
